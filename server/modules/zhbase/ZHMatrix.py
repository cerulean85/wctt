import math

import numpy as np
from scipy import linalg

"""
텐서 관련 링크
https://ghebook.blogspot.com/2011/06/tensor.html
"""

class ZHMatrix:

    def matmul(self, m1, m2):
        return np.matmul(m1, m2)

    def norm(self, target, ord):
        return linalg.norm(target, ord)

    def eigen_decomposition(self, m):
        """고유값 분해"""
        eigen_value, eigen_vector = np.linalg.eig(m)
        return eigen_value, eigen_vector

    def pseudo_inverse(self, m):
        """유사역행렬. 무어-펜로즈"""
        return linalg.pinv(m)


if __name__ == '__main__':

    mat = ZHMatrix()

    # 1

    A = [[1, 2, -1],
         [2, 7, 4],
         [0, 4, -1]]

    b = [1, 0, 1.2]
    print(mat.matmul(A, b))

    A = [[1, 2, -1],
         [2, 7, 4],
         [0, 4, -1]]

    B = [[1, 2, 3, 4],
         [-1, 2, 3, 1],
         [3, -2, 5, 9]]
    print(mat.matmul(A, B))

    b = [1, 0, 1.2]
    print(mat.norm(b, 1))
    print(mat.norm(b, 2))

    A = [[4, 2],
         [3, 5]]
    print(mat.eigen_decomposition(A))

    A = [[1, 1],
         [0, 0],
         [0, 0]]
    print(mat.pseudo_inverse(A))

    x = [1, 2, 3]
    w = [-1, 0, 1]
    b = 1
    result = mat.matmul(w, x) + b
    print(max(0, result))
    exit()




    x = np.array(x)
    print(x)
    print(x.T)

    print(result)
    print(max(0, result))
    exit()


    print(mat.pseudo_inverse(A))

    # print(mat.eigen_decomposition([ [4,2], [3,5] ]))


    exit()
    A = [[1, 2, -1],
         [2, 7, 4],
         [0, 4, -1]]

    B = [[1, 2, 3, 4],
         [-1, 2, 3, 1],
         [3, -2, 5, 9]]

    print(np.matmul(A, B))