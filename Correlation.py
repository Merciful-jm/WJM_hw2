import numpy as np
import time
import matplotlib.pyplot as plt
#function used for block diagonalization

#calculate total spin for one state
def sum_str(str_state):
    list_state = list(str_state)
    sum_state = 0
    for i in list_state:
        sum_state = sum_state + int(i)
    return sum_state    

#flip state
def flip(a_spin_state, i, j, a_dict):
    b_spin_state = list(a_spin_state)#for change str ,we change its class to list
    b_spin_state[i] = a_spin_state[j]
    b_spin_state[j] = a_spin_state[i]
    b_spin_state=''.join(b_spin_state)
    b = a_dict[b_spin_state]
    return b

#find degenerate ground state, sub_degeneracy
def find_ground_state_index(eig):
    min_eig = np.min(eig)
    eig_min_index = []
    for e_index,e in enumerate(eig):
        if abs(e-min_eig) < 0.01*abs(min_eig):
            eig_min_index.append(e_index)
    sub_degeneracy = len(eig_min_index)
    return eig_min_index,sub_degeneracy

import matplotlib.pyplot as plt

start_time = time.time()
#for num in range(3,15):
#N=num
N = 14
cor_all = []
correlation_i = 0
for m in range(N):
    correlation_j = m
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
        H_all_sub.append(H_sub)

       #calculate subspace correlation operator
        Si_dot_Sj = np.zeros(shape=(M,M))
        for a_sub_state, a_sub in a_sub_dict.items():
            if a_sub_state[correlation_i] == a_sub_state[correlation_j]:
                Si_dot_Sj[a_sub,a_sub] = 0.25
            else:
                Si_dot_Sj[a_sub,a_sub] = -0.25
                b_sub = flip(a_sub_state, correlation_i, correlation_j, a_sub_dict)
                Si_dot_Sj[a_sub, b_sub] = 0.5
        #print('spin cor operator\n',spin_cor_operator)
        sub_information = []

        #sub enegy and vector
        e_sub, v_sub = np.linalg.eig(H_sub)
        #sub ground enegy
        sub_information.append(min(e_sub))
        #sub degeneracy
        sub_information.append(find_ground_state_index(e_sub)[1])

        #sub correlation function
        sub_cor = 0
        for d in find_ground_state_index(e_sub)[0]:
            sub_cor = sub_cor + np.matrix(v_sub[:,d]) * Si_dot_Sj * np.matrix(v_sub[:,d]).T
        sub_information.append(sub_cor[0,0])
        information.append(sub_information)


    information = np.array(information) 
    cor = 0
    degeneracy = 0
    for x in find_ground_state_index(information[:,0])[0]:
        degeneracy = degeneracy + information[x,1]
        cor = cor + information[x,2]
    cor = cor / degeneracy
    cor_all.append(cor.real)
print('cor',cor_all)
end_time = time.time()
print('program time:{:.3f} s.'.format(end_time-start_time))

plt.plot(range(1,len(cor_all)+1),cor_all,'b',label='calculate')
plt.title('{} spin Si Sj correlatin'.format(N))
plt.savefig('{} all spin.png'.format(N))
plt.show()