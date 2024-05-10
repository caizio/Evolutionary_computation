import genetic_algorithm as g

ga = g.genetic_algorithm(d = 10, n = 100)
# -----初始化群体-----
group_init = ga.create_group()
group_code = ga.group_code(group_init)
group_decode = ga.group_decode(group_code)
 
for i in range(100000):
    # -----选择-----
    group_loss = ga.group_loss(group_decode)
    group_fitness = ga.group_fitness(group_loss)
    choose = ga.roulette_selection(group_loss)
    group_decode = ga.index_to_decode(group_decode,choose)
    group_code = ga.group_code(group_decode)
    # -----交叉-----    
    group_code = ga.cross_over(group_code)
    # -----变异-----
    group_code = ga.mutation(group_code)
    group_decode = ga.group_decode(group_code)
    min,indi_decode = ga.min_loss(group_decode)
    print(min)
    if min < 0.01:
        print(str(i),end= ":")
        print(indi_decode)
        break
    

