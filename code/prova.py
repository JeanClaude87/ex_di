#!/usr/bin/python
import numpy as np
import f_diagonal as diagonal
import f_function as ff
import os 
from time import gmtime, strftime
import time

LOCAL = os.path.abspath('.')
np.set_printoptions(precision=4)

#....................................LUNGHEZZA
L_i = 8
L_f = 8
L_D = 2

L_n = int(1+(L_f-L_i)/L_D)

#print L_i, L_f, L_n
L_tab = [int(L_i+j*L_D) for j in range(L_n)]
'''
for L in L_tab:

	nomefile = 'CdC-L_'+str(L)+'.npy'
	if not os.path.isfile(LOCAL+os.sep+nomefile):
		CdC_Tab = ff.prep_tab(L)
		np.save(LOCAL+os.sep+nomefile, CdC_Tab)
'''
#....................................DISORDINE
D_i = 5
D_f = 5
D_D = 1

D_n = int(1+(D_f-D_i)/D_D)

#print D_i, D_f, D_n
D_tab = [D_i+j*D_D for j in range(D_n)]


#....................................VAI CON DIO


PATH_now = LOCAL

NN_RR = [1]


n0=0
for i in L_tab:

	#nomefile = str('CdC-L_'+str(i)+'.npy')
	#Tab_CdC = np.load(LOCAL+os.sep+nomefile)

	for j in D_tab:
		directory = 'DATA_0/L_'+str(i)+'/D_'+str(j)
		PATH_now = LOCAL+os.sep+directory+os.sep
		if not os.path.exists(PATH_now):
			os.makedirs(PATH_now)		
		
		for n in range(NN_RR[n0]):
			data = [i,j,n+1]







			AA=time.clock()
			diagonal.ExactDiagonalization(PATH_now,data[0],data[1])#,Tab_CdC)
			print(time.clock()-AA)
			#def 	 ExactDiagonalization(PATH_now,   L,     D,    Tab_CdC):			

	n0 += 1






