
from __future__ import division
from pysat.formula import CNF
from pysat.solvers import Solver
import random
import math
import statistics
import gc
import matplotlib.pyplot as plt
## Leitura

def random_assump(n):
    list = []
    for i in (range(n+1)):
        if(i == 0):
            continue
        else:
            if(random.choice([True, False])):
                list.append(i)
            else:
                list.append(-i)

    return list

def quantidade_verdade(clauses,s):
    cont = 0
    for clause in clauses:
        d = Solver()
        d.add_clause(clause)
        if(d.solve(s)):
            cont = cont +1
        d.delete()
    return cont


def SASAT(cnf,max_tries, max_temp, min_temp,atual):



    melhor = list(atual) #atual.copy()
    qtd_melhor = quantidade_verdade(cnf.clauses,melhor)
    #print(qtd_melhor)
    cont = 0
    temperatura = max_temp
    melhor_temperatura = temperatura
    datas_temp = [temperatura]
    datas_qtd = [qtd_melhor]

    while(temperatura > min_temp and cont < max_tries):
        #print(cont)
        for i in range(30):

            rand = random.randint(0,cnf.nv -1)
            visinho = list(atual)#atual.copy()
            visinho[rand] = visinho[rand]*-1
            qtd_visinho = quantidade_verdade(cnf.clauses,visinho)
            qtd_atual = quantidade_verdade(cnf.clauses,atual)
            if(qtd_visinho > qtd_atual):
                atual = list(visinho)#visinho.copy()
                qtd_atual =qtd_visinho
                if(qtd_atual>qtd_melhor):
                    melhor = list(visinho)#visinho.copy()
                    melhor_temperatura = temperatura
                    qtd_melhor = qtd_visinho
            else:
                x = random.random()
                #pr = 1 / (1 + math.exp(-1*qtd_visinho/temperatura))
                exx = (0-abs(qtd_visinho-qtd_atual))*12 / temperatura
                #print(x,pr)
                if(x<math.exp(exx)):
                #if(x<pr):
                    atual= list(visinho) #visinho.copy()
                    qtd_atual = qtd_visinho

        temperatura = temperatura*0.80
        #decay = 1/((cont+1) * cnf.nv)
        #temperatura = max_temp* math.pow(math.e,-cont*decay)
        datas_temp.append(temperatura)
        datas_qtd.append(qtd_atual)
        cont = cont +1

    return melhor,datas_temp,datas_qtd


def RS(cnf,atual):
    s_out = list(atual)
    s_out_FO = quantidade_verdade(cnf.clauses,s_out)
    datas = [s_out_FO]
    for i in range(30):
        #print(i)
        rand = random.randint(0,cnf.nv -1)
        s = list(atual)#atual.copy()
        s[rand] = s[rand]*-1
        s_FO = quantidade_verdade(cnf.clauses,s)
        if(s_FO > s_out_FO):
            s_out = list(s)
            s_out_FO = s_FO
        datas.append(s_out_FO)

    return s_out,s_FO,datas



## adiciona as clausulas para solver
#print(cnf.clauses)
#assump = random_assump(cnf.nv)
#print(assump)
#print(s.solve(assump))
#print(s.get_model())

#print( s.solve())
#print("Clause que resolve :",s.get_model())

cnf  = CNF('uf250-01.cnf')
atual = random_assump(cnf.nv)

v_SASAT = []
v_RS = []

for i in range(10):
    s_best,datas_temp,datas_qtd = SASAT(cnf,100,100,0.01,list(atual))
    q = quantidade_verdade(cnf.clauses,s_best)
    v_SASAT.append(q)
    plt.ylabel("clausulas compridas")
    plt.xlabel("temperatura")
    plt.plot(datas_temp[:],datas_qtd[:])
    plt.xlim(plt.xlim()[::1])
    plt.savefig(f'plot_uf250_{i+1}_SASAT')
    plt.clf()

    s_rs,q,data = RS(cnf,list(atual))
    plt.ylabel("clausulas compridas")
    plt.xlabel("i")
    plt.plot([j for j in range(len(data))],data)
    plt.savefig(f'plot_uf250_{i+1}_RS')
    plt.clf()
    v_RS.append(q)
    gc.collect()




print ("SASAT MEDIA :", statistics.mean(v_SASAT) , "  +- ",statistics.stdev(v_SASAT))
print ("RS MEDIA :", statistics.mean(v_RS), " +- ",statistics.stdev(v_RS))
