import re
import ast
import os
import sys
import shutil

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import coverage
        import pytest

        if self.pytest_args and len(self.pytest_args) > 0:
            self.test_args.extend(self.pytest_args.strip().split(' '))
            self.test_args.append('tests/')

        cov = coverage.Coverage()
        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.report()
        cov.html_report()
        print("Wrote coverage report to htmlcov directory")
        sys.exit(errno)


do_cythonize = os.getenv('CYTHONIZE', 'false').lower() == 'true'
ext_modules = []
cmdclass = {'test': PyTest}
packages = find_packages(exclude=["tests"])

if do_cythonize:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext

        class MyBuildExt(build_ext):

            def run(self):
                build_ext.run(self)
                build_dir = os.path.realpath(self.build_lib)
                root_dir = os.path.dirname(os.path.realpath(__file__))
                target_dir = build_dir if not self.inplace else root_dir
                self.copy_file('rho_crypto/__init__.py', root_dir, target_dir)

            def copy_file(self, path, source_dir, destination_dir):
                if os.path.exists(os.path.join(source_dir, path)):
                    shutil.copyfile(os.path.join(source_dir, path),
                                    os.path.join(destination_dir, path))

        cmdclass['build_ext'] = MyBuildExt
        ext_modules = cythonize("rho_crypto/*.py")
        packages = []

    except ImportError:
        pass

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('rho_crypto/__init__.py', 'rb') as f:
    __version__ = str(
        ast.literal_eval(
            _version_re.search(f.read().decode('utf-8')).group(1)))

setup(name='rho-crypto',
      version=__version__,
      description="Crypto utilities",
      long_description=open('README.md', 'r').read(),
      maintainer="Rho AI Corporation",
      license="Commercial",
      url="https://bitbucket.org/pitrho/rho-crypto",
      packages=packages,
      include_package_data=True,
      install_requires=['pycryptodome>=3.16.0'],
      ext_modules=ext_modules,
      extras_require={
          'deploy':
          ['Cython>=0.29,<0.30', 'wheel>=0.32,<0.33', 'twine>=1.12,<2'],
          'test':
          ['coverage==4.0a5', 'mock>=1,<2', 'pytest>=4,<5', 'tox>=3,<4']
      },
      cmdclass=cmdclass)
