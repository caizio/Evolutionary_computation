import numpy as np
import random
import math
class Tar():
    def __init__(self):
        self.X =[]
    def u(self, X):
        alfa = 5
        k = 100
        m = 4
        if X > alfa:
            return k * (X - alfa) ** m
        elif X >= -alfa and X <= alfa:
            return 0
        else:
            return k * (-X - alfa) ** m
    def y(self, X):
        return 1 + (X + 1) / 4
    def target_function(self, X, flag=16):
        a = 0
        # -100，100   min 0
        if flag == 0:
            for i in X:
                a = a + i ** 2
        # -10,10  min 0
        if flag == 1:
            ji = 1
            for i in X:
                a += abs(i) + ji * abs(i)
        # -100,100 min 0
        if flag == 2:
            for i in range(len(X)):
                for j in range(i):
                    a += X[j]
                a = a ** 2
        # -100,100 min 0
        if flag == 3:
            for i in X:
                if a < abs(i):
                    a = abs(i)
                else:
                    pass
        # -30,30 f(1,1,1,,1) min 0
        if flag == 4:
            for i in range(len(X)):
                if i + 1 >= len(X):
                    pass
                else:
                    a += 100 * (X[i + 1] - X[i] ** 2) ** 2 + (X[i] - 1) ** 2
        # -100,100 min 0
        if flag == 5:
            for i in X:
                a += int(i + 0.5) ** 2
        # -100,100 min 0
        if flag == 6:
            for i in range(len(X)):
                a += (i + 1) * X[i] ** 4
            a += random.uniform(0, 1)
        # -500,500  f(420,9687) min -418.9829*len(X)
        if flag == 7:  # 不收敛至结果
            for i in range(len(X)):
                a += -X[i] * math.sin(math.sqrt(abs(X[i])))
        # -5.12,5.12  min 0
        if flag == 8:
            for i in range(len(X)):
                a += X[i] ** 2 - 10 * math.cos(2 * math.pi * X[i]) + 10
        # -32，32 min 0
        if flag == 9:  # 不收敛
            c = 0
            d = 0
            for i in range(len(X)):
                c += X[i] ** 2
                d += math.cos(2 * math.pi * X[i])
            a = -1 * 20 * math.exp(-1 * 0.2 * math.sqrt(c / len(X))) - math.exp(d / len(X)) + 20 - math.e
        # -600,600 min 0
        if flag == 10:
            c = 0
            d = 1
            for i in range(len(X)):
                c += X[i] ** 2
                d += d * math.cos(X[i] / math.sqrt(i + 1))
            a = c / 4000 - d + 1
        # min -1 -1 -1 -1 -1 ,0  书上 1 1 1 1 1 1，0
        if flag == 11:
            sumy = 0
            sumu = 0
            for i in range(len(X) - 1):
                sumy += (self.y(X[i]) - 1) ** 2 * (1 + 10 * math.sin(math.pi * self.y(X[i + 1])) ** 2)
            for i in range(len(X)):
                sumu += self.u(X[i])
            a = math.pi * (10 * math.sin(math.pi * self.y(X[0])) ** 2 + (self.y(X[len(X) - 1]) - 1) ** 2 + sumy) / len(
                X) + sumu
        # -50,50 f(1,1,1,1) min 0
        if flag == 12:
            sumu = 0
            sumx = 0
            for i in range(len(X)):
                sumu += self.u(X[i])
            for i in range(len(X) - 1):
                sumx += (X[i] - 1) ** 2 * (1 + math.sin(3 * math.pi * X[i + 1]) ** 2) + (X[i] - 1) ** 2 * (
                            1 + math.sin(2 * math.pi * X[len(X) - 1]) ** 2)
            a = 0.1 * (math.sin(3 * math.pi * X[0]) ** 2 + sumx) + sumu
        # -65.536,65.536 f(-32,-32) min 1 ,维度为2
        if flag == 13:
            aij = np.zeros((2, 25))
            d = [-32, -16, 0, 16, 32]
            for i in range(2):
                for j in range(25):
                    if i == 0:
                        aij[i][j] = d[j % 5]
                    else:
                        e = j / 5
                        aij[i][j] = d[int(e)]
            f = 0
            g = 0
            for j in range(25):
                for i in range(2):
                    g += (X[i] - aij[i][j]) ** 6
                f += 1 / (j + g)
            a = (f + 1 / 500) ** (-1)
        # -5，5 f(0.1928,0.1908,0.1231,0.1358) min 0.0003075
        if flag == 14:  # 不收敛
            ai = [0.1957, 0.1947, 0.1735, 0.1600, 0.0844, 0.0627, 0.0456, 0.0342, 0.0323, 0.0235, 0.0246]
            bi = [0.25, 0.5, 1, 2, 4, 6, 8, 10, 12, 14, 16]
            for i in range(11):
                a += (ai[i] - (X[0] * (bi[i] ** 2 + bi[i] * X[1])) / (bi[i] + bi[i] * X[2] + X[3])) ** 2
        # -5,5 f(0.08983,-0.7126)=f(0.08983,0.7126) min -1.0316285
        if flag == 15:
            a = 4 * X[0] ** 2 - 2.1 * X[0] ** 4 + X[0] ** 6 / 3 + X[0] * X[1] - 4 * X[1] ** 2 + 4 * X[1] ** 4
        # -5,10 f(-3.142,12.275) f(-3.142,2.275) f(9.425,2.425) min 0.398
        if flag == 16:
            a = (X[1] - 5.1 * X[0] ** 2 / (4 * math.pi ** 2) + 5 * X[0] / math.pi - 6) ** 2 + 10 * (
                        1 - 1 / (8 * math.pi)) * math.cos(X[0]) + 10
        # 0,1 f(0.114,0.556,0.852) min -3.86
        if flag == 17:  # n=3
            aH = np.array([[3, 10, 30], [0.1, 10, 35], [3, 10, 30], [0.1, 10, 35]])
            cH = np.array([1, 1.2, 3, 3.2])
            pH = np.array([[0.3689, 0.117, 0.2673], [0.4699, 0.4387, 0.747],
                           [0.1091, 0.8732, 0.5547], [0.03815, 0.5743, 0.8828]])
            for i in range(0, 4):
                a = a - cH[i] * np.exp(-(np.sum(aH[i] * ((X - pH[i]) ** 2))))
            return a

        if flag == 18:  # n=6
            aH = np.array([[10, 3, 17, 3.5, 1.7, 8], [0.05, 10, 17, 0.1, 8, 14], [3, 3.5, 1.7, 10, 17, 8],
                           [17, 8, 0.05, 10, 0.1, 14]])
            cH = np.array([1, 1.2, 3, 3.2])
            pH = np.array(
                [[0.1312, 0.1696, 0.5569, 0.0124, 0.8283, 0.5886], [0.2329, 0.413, 0.8307, 0.3736, 0.1004, 0.9991],
                 [0.2348, 0.1415, 0.3522, 0.2883, 0.3047, 0.6650], [0.4047, 0.8828, 0.8732, 0.5743, 0.1091, 0.0381]])
            for i in range(0, 4):
                a = a - cH[i] * np.exp(-(np.sum(aH[i] * ((X - pH[i]) ** 2))))
            return a
        return a
if __name__ == '__main__':
    ta = Tar()
    X=[1,1,1,1,1,4]
    result=ta.target_function(X)
    print(result)