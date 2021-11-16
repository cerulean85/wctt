import numpy as np

class ZHMath:

    def min_max_normalization(self, mat):
        max_n = max(mat)
        min_n = min(mat)
        result = [(1 - ((n - min_n) / (max_n - min_n))) for n in mat]
        return result

    def zh_normalization(self, limit_count, mat):
        # max_n = max(mat)
        result = [
            0.0 if n >= limit_count
            else (limit_count - n)/(limit_count - 1)
            for n in mat
        ]
        return result

    def sigmoid_normalization(self, mat):
        mat = np.array(mat)
        result = 1 / (1 + np.exp(mat))
        return result.tolist()

    def ReLU(self, x):
        return max(0, x)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        # return np.tanh(x)
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

# if __name__ == "__main__":
#     x = [1, 2, 3, 4, 5]
#     zhm = ZHMath()
#     zlist = zhm.sigmoid_normalization(x)
#     print(zlist)



