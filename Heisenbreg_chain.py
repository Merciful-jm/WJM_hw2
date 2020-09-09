# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:40:45 2020
@author: Jiaming Wang
"""
import numpy as np
import time
#import matplotlib.pyplot as plt

def sum_str(str_state):# To calculate the Summer of up-state.
    list_state = list(str_state)
    sum_state = 0
    for i in list_state:
        sum_state = sum_state + int(i)
    return sum_state 


def flip(a_spin_state, i, j, a_dict):
    b_spin_state = list(a_spin_state)#for change str ,we change its class to list
    b_spin_state[i] = a_spin_state[j]
    b_spin_state[j] = a_spin_state[i]
    b_spin_state=''.join(b_spin_state)
    b = a_dict[b_spin_state]
    return b

start_time = time.time()
N = 14
a_dict = {}
H_all_sub = []
all_sub_dict = []
#define dict state and state_num
for i in range(2**N):
    i_binary = bin(i)[2:]#binary change
    for zero in range(N-len(i_binary)):
        i_binary = '0'+i_binary
    a_dict[i_binary] = i

#block
information = []
for n in range(N+1):
    #calculate n=2 matrix，a total of 2S+1，S=N/2，N+1 total spin，range of n is 0-N
    #n = 2
    a_sub = 0
    a_sub_dict = {}
    #creat subspace dict
    for a_spin_state, a in a_dict.items():
        if sum_str(a_spin_state) == n:
            a_sub_dict[a_spin_state] = a_sub
            a_sub =a_sub + 1
    #subspace dim
    M = a_sub
    #save subspace dict
    all_sub_dict.append(a_sub_dict)
    #calculate subspace Hamiltonian
    H_sub = np.zeros(shape=(M, M))
    for a_sub_state, a_sub in a_sub_dict.items():  #cycle dict for state and num of state
        for i in range(N):#open N-1
            j = (i+1) % N#periodic boundary
            #j = i+1#open boundary
            if a_sub_state[i]==a_sub_state[j]:
                H_sub[a_sub, a_sub]= H_sub[a_sub, a_sub] + 0.25
            else:
                H_sub[a_sub, a_sub]= H_sub[a_sub, a_sub] - 0.25
                b_sub = flip(a_sub_state, i, j, a_sub_dict)
                H_sub[a_sub, b_sub]=0.5
    #save subspace hamiltonian
    e, v = np.linalg.eig(H_sub)
    # print(v)
    H_all_sub.append(H_sub)
end_time = time.time()
print('program time:{:.3f} s.'.format(end_time-start_time))