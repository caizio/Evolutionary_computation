import math
import random
import copy

class PSO:
    def __init__(self,N=100,d=2,left = -100,right = 100,vMax = 10,w = 1, c1 = 1.4,c2 = 1.4) -> None:
        self.N = N #群体数量
        self.d = d #个体维度
        self.left = left
        self.right = right
        self.vMax = vMax
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.indiBest = []
        self.groupBest = 0
    def target(self,x,flag = 2) -> float:
        if flag == 0:
            return 20 + x[0] * x[0] + x[1] * x[1] - 10 * (math.cos(2* 3.14 * x[0]) + math.cos(2 * 3.14 * x[1]))
        elif flag == 1:
            sum = 0.0
            for xi in x:
                sum += xi ** 2 
            return sum
        elif flag == 2:
            sum = 0.0
            for xi in x:
                sum += (xi - 10) ** 2
            return sum
    def groupTarget(self,group)->list:
        indiBest_target = []
        for i in range(self.N):
            temp = self.target(group[i])
            indiBest_target.append(temp)
        return indiBest_target
    def init_group(self)->list:
        group = []
        for i in range(self.N):
            indi = []
            for j in range(self.d):
                rand = random.uniform(self.left,self.right)
                indi.append(rand)
            group.append(indi)
        return group
    def init_v(self)->list:
        # 初始化群体速度
        v = []
        for i in range(self.N):
            v_indi = []
            angle = random.random() * 2 * math.pi
            v1 = 1 * math.cos(angle)
            v2 = 1 * math.sin(angle)
            v_indi.append(v1)
            v_indi.append(v2)
            v.append(v_indi)
        return v 
    def update(self,group,v,indiBest,indiBest_target,bestKey,maxCycle=10000)->list:
        # Vt+1 = wvt+c1r1(Pi-Xt)+c2r2(Pg-xt)
        # Xt+1=Xt+Vt+1
        for z in range(maxCycle):
            for i in range(self.N):
                for d in range(self.d):
                    r1 = 0.6; r2 = 0.4
                    v[i][d] = self.w * v[i][d] + self.c1 * r1 * (indiBest[i][d] - group[i][d]) + self.c2 * r2 * (indiBest[bestKey][d] - group[i][d])
                    group[i][d]+=v[i][d]  
                tmp = self.target(group[i])
                if tmp < indiBest_target[i]:
                    indiBest[i] = copy.deepcopy(group[i])
                    indiBest_target[i] = tmp
                    if indiBest_target[i] < indiBest_target[bestKey]:
                        bestKey = i
                        print(z,indiBest[bestKey],indiBest_target[bestKey])

if __name__ == "__main__":
    pso = PSO()
    group = pso.init_group()    #初始化群体的初始值
    v = pso.init_v()            #初始化群体的速度
    indiBest = copy.deepcopy(group)            #初始化群体的最优个体为群体的初始值
    bestKey = 0                 #记录群体最优的下标
    indiBest_target = []
    min = 999999.0
    for i in range(pso.N):      #初始化群体的最优值
        temp = pso.target(indiBest[i])
        indiBest_target.append(temp)
        if temp < min:
            min = temp
            bestKey = i
    pso.update(group,v,indiBest,indiBest_target,bestKey,maxCycle=10000)
   