import sys
import hashlib
import logging

logger = logging.getLogger(__name__)


class Hasher(object):
    """ Create consistent SHA1 hash of a file.
    """
    def __init__(self):
        super(Hasher, self).__init__()
        self.hashes = {
            'SHA1': hashlib.sha1(),
            'SHA256': hashlib.sha256()
        }

    def _supported_algorithm(self, algorithm):
        if algorithm in self.hashes.keys():
            return True
        return False

    def reset_hashes(self):
        """ Resets all hashes.
        """
        self.__init__()

    def hash_from_path(self, file_path, algorithm='SHA1'):
        """ Open a file with path to file.
        """
        if not self._supported_algorithm(algorithm):
            logger.error("{0} is an unsupported algorithm. Options: {1}"
                         .format(algorithm, self.hashes.keys()))
            return

        if file_path is None:
            logger.error("No file_path provided ...")
            return

        data = None
        try:
            with open(file_path, 'rb') as f:
                data = f.read()

        except Exception as e:
            logger.error("Unable to process file: {0}".format(e))

        if data is not None:
            return self.hash_from_bytes(data, algorithm)

        return None

    def hash_from_bytes(self, data_bytes, algorithm='SHA1'):
        """ Updates internal sha1 value, returns current hexdigest.

            Intended usage is to pass bytes of a file. If this is a local file,
            the process would be similar to what's done in hash_from_path()

            my_hasher = Hasher()
            with open('/path/to/file.ext', 'rb') as f:
                data = f.read()
            hash_val = my_hasher.hash_from_bytes(data)
        """
        if not self._supported_algorithm(algorithm):
            logger.error("{0} is an unsupported algorithm. Options: {1}"
                         .format(algorithm, self.hashes.keys()))
            return

        self.hashes[algorithm].update(data_bytes)

        return self.hashes[algorithm].hexdigest()


if __name__ == '__main__':
    """ Convenience for testing this on CLI. Not intended for actual use.
    """
    try:
        my_hasher = Hasher()
        file_path = sys.argv[1]
        try:
            algo = sys.argv[2]
        except Exception as e:
            algo = 'SHA1'
        hash_val_1 = my_hasher.hash_from_path(file_path, algo)
        print("{0}: {1}".format(algo, hash_val_1))
        my_hasher.reset_hashes()
    except Exception as e:
        logger.exception("Error ...{0}".format(e))
