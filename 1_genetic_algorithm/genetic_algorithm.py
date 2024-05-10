import random

class genetic_algorithm:
    def __init__(self,d=10,n=100,pc=0.5,pm=0.1,lb=-99,rb=99) -> None:
        # n为群体的规模，d为个体的大小,pc为交叉概率，pm为变异概率
        self.d = d
        self.n = n
        self.pc = pc
        self.pm = pm
        self.lb = lb
        self.rb = rb
    def create_group(self) -> list:
        group = []
        for i in range(self.n):
            indi = self.__initIndividual()
            group.append(indi)
        return group
    def __initIndividual(self) -> list:
        data_uncode = []
        for i in range(self.d):
            rand = random.uniform(self.lb,self.rb)
            data_uncode.append(rand)
        return data_uncode
    def code(self,data) -> str:
        # 对个体进行编码，编码格式XXXXX，第一位是符号位（0是正数，1是负数），二三位是整数部分，四五位是小数部分
        result = ""
        for item in data:
            c = ""
            if item >= self.rb+1 or item <= self.lb-1:
                return "error"
            if item >= 0:
                c = "0"
            else:
                c = "1"
            a = str(int(abs(item * 100)))
            if len(a) == 3:
                a = "0" + a
            elif len(a) == 1:
                a = "000" + a
            elif len(a) == 2:
                a = '00' + a
            c = c + str(a)
            result = result + c;
        return result
    def group_code(self,group_decode)->list:
        group_code = []
        for item in group_decode:
            group_code.append(self.code(item))
        return group_code
    def decode(self,data) -> list:
        result = []
        n = int(len(data) / 5)
        for i in range(n):
            a = int(data[i*5+1:i*5+5])
            a = a / 100.0
            b = 1
            if(data[i*5] == "1"):
                b = -1
            result.append(b * a)
        return result
    def group_decode(self,group_code) -> list:
        group_decode = []
        for item in group_code:
            group_decode.append(self.decode(item))
        return group_decode
    def group_loss(self,group_decode) ->list:
        # 计算群体中所有个体的目标函数
        group_loss = []
        for i in group_decode:
            group_loss.append(self.loss(i))
        return group_loss
    def loss(self,data_decode,flag = 1) -> int:
        if flag == 0:
        # 计算一个个体的目标函数，f=sum（xi）
            sum = 0
            for item in data_decode:
                sum = sum + item * item
            return sum
        elif flag == 1:
            sum = 0
            for item in data_decode:
                sum = sum + (item - 10) * (item - 10)
            return sum        
    def group_fitness(self,group_loss) ->list:
        # 计算群体中每一个个体的fitness
        min_loss = min(group_loss)
        n = len(group_loss)
        for i in range(n):
            group_loss[i] = 1 / (min_loss + 1 + group_loss[i])
        return group_loss
    def roulette_selection(self,group_fitness):
        # 轮盘选择
        n = len(group_fitness)
        # 归一化处理，并转化为累加概率
        sum = 0
        for item in group_fitness:
            sum += item
        group_p = []
        p = 0
        for item in group_fitness:
            p += item / sum
            group_p.append(p)
        # 按照概率选择个体
        index = []
        for i in range(n):
            rand = random.random()
            for j in range(n):
                if rand < group_p[j]:
                    index.append(j)
                    break
        return index
    def index_to_decode(self,group_decode,index)->list:
        # 按照选表选择decode
        n = len(group_decode)
        group = []
        for i in range(n):
            group.append(group_decode[index[i]])
        return group
    def cross_over(self,data_code)->list:
        # 交叉
        rand = random.random()
        if rand < self.pc:
            rand1 = random.randint(0,self.n-1)
            rand2 = random.randint(0,self.n-1)
            cross_site = random.randint(0,5 * self.d-1)
            temp = data_code[rand1][cross_site:]
            data_code[rand1] = data_code[rand1][0:cross_site] + data_code[rand2][cross_site:]
            data_code[rand2] = data_code[rand2][0:cross_site] + temp
        return data_code
    def mutation(self,data_code)->list:
        # 变异
        for i in range(0,self.n):
            rand = random.random()
            if rand < self.pm:
                rand2 = random.randint(0,5*self.d-1)
                if rand2 % 5 == 0:
                    ran3  = random.randint(0,1)
                    data_code[i] = data_code[i][0:rand2] + str(ran3) + data_code[i][rand2+1:]
                else:
                    ran4 = random.randint(0,9)
                    data_code[i] = data_code[i][0:rand2] + str(ran4) + data_code[i][rand2+1:]
        return data_code
    def min_loss(self,data_decode):
        # 计算群体中目标函数最小的个体
        min = self.loss(data_decode[0])
        indi_decode = []
        for indi in data_decode:
            indi_decode = indi
            k = self.loss(indi)
            if k < min:
                min = k    
        return min,indi_decode    
if __name__ == "__main__":
    # -----设定参数-----
    ga = genetic_algorithm(d = 5, n = 1000)
    # -----初始化群体-----
    group_init = ga.create_group()
    group_code = ga.group_code(group_init)
    group_decode = ga.group_decode(group_code)
    # print(group_decode)
    # -----选择-----
    group_loss = ga.group_loss(group_decode)
    group_fitness = ga.group_fitness(group_loss)
    choose = ga.roulette_selection(group_loss)
    group_decode = ga.index_to_decode(group_decode,choose)
    group_code = ga.group_code(group_decode)
    # print(group_decode)
    # -----交叉-----    
    group_code = ga.cross_over(group_code)
    group_decode = ga.group_decode(group_code)
    # print(group_decode)
    # -----变异-----
    group_code = ga.mutation(group_code)
    group_decode = ga.group_decode(group_code)
    # print(group_decode)