import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.special
from mpmath import *
import random
import time

# mp.dps = 20


# print(mp.quad(lambda x: mp.exp(-x**2), [-mp.inf, mp.inf]) ** 2)

# pi = mp.quad(lambda x: mp.exp(-x**2), [-mp.inf, mp.inf]) ** 2

# print(pi > 3.1415926535)

# print(mp.mpf(2) ** mp.mpf('0.5'))

# print(mp.mpf('4'))
# print(mp)



n = 1_000_000





debut = time.time()
def find_the_mode (n):
    for m in range(1,n+1):
        if math.log(1+1/m)*n <= math.log(1+m):
            return(m)
    raise Exception('Problème calcul du mode')

m = find_the_mode(n)



mp.dps = 10*(math.log(n) + 10)


def W (n):
    beta = mp.ln(n) -mp.ln(mp.ln(n))
    for i in range (15): # je reste à 15 pour l'instant : ça fait 5 000 décimales de précision donc c'est pas ça qui coince en théorie
        beta = beta*(1+mp.ln(n/beta))/(1+beta)
    return(beta)




def compute_B_n_tilde (n):
    return((3/(2*mp.sqrt(n)))*(mp.power(n/W(n),n+1/2))*mp.exp(n/W(n)-n-1))


def g_int (m,n):
    return(mp.power(m,n)/mp.factorial(m))

def g_function (x,m,n):
    g_m = g_int (m,n)
    B_n_tilde = compute_B_n_tilde(n)
    facteur = mp.exp(1-g_m*(mp.absmax(x)-mp.mpf('0.5'))/(mp.exp(1)*B_n_tilde))
    if facteur < 1 : 
        return(g_m*facteur)
    else:
        return(g_m)


def tirer_Y (n,m):
    g_m = g_int (m,n)
    B_n_tilde = compute_B_n_tilde(n)
    bern = random.random()
    if bern < 2/(g_m/(mp.exp(1)*B_n_tilde)+4) : #on est dans l'un des deux cotés
        dg = random.randint(1,2)
        expdistribution = mp.mpf('-1')*mp.log(random.random())*mp.exp(1)*B_n_tilde/g_m
        if dg == 1 : return(m + 0.5 + mp.exp(1)*B_n_tilde/g_m - expdistribution)
        else : return(m -0.5 - mp.exp(1)*B_n_tilde/g_m - expdistribution)
    else:
        return(m + (1 - 2*random.random())*(mp.mpf('0.5') + mp.exp(1)*B_n_tilde/g_m))
            
Y = tirer_Y(n,m)
X = round(Y)














def remplissage_urnes (k,n): 
    urnes = []
    t = 0
    for i in range (k):
        urnes.append([])
    for i in range (n):
        gtavant = time.time()
        u = random.randint(0,k-1)
        gtapres = time.time()
        t+= (gtapres - gtavant)
        urnes[u].append(i)
    partition = []
    for i in range (k):
        if urnes[i] != []:
            partition.append(urnes[i])
    print(t)
    return(partition)



b = True
while b :
    Y = tirer_Y(n,m)
    X = round(Y)
    if random.random()*g_function(Y,m,n) < g_int(X,n):
        k = X
        b = False



print(k)

apres_k = time.time()

print(apres_k - debut)

partition = remplissage_urnes(k,n)
print(partition[0])
print(len(partition))

fin = time.time()


print(fin - apres_k)