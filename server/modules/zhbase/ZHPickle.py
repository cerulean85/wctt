import pickle
import gzip


class ZHPickle:

    def save(self, filename, data, compress=False):

        if not compress:
            with open(filename, "wb") as f:
                pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

        else:
            with gzip.open(filename, "wb") as f:
                pickle.dump(data, f)

    def load(self, filename, compress=False):

        if not compress:
            with open(filename, "rb") as f:
                data = pickle.load(f)
            return data

        else:
            with gzip.open(filename, "rb") as f:
                data = pickle.load(f)
            return data
