#!/usr/bin/python
import numpy as np
import f_diagonal as diagonal
import f_function as ff
import os
import sys
from time import gmtime, strftime
import time

LOCAL = os.path.abspath('.')

# LL = #1
LL = sys.argv[1]
#print 'L', LL, type(LL)

# DD = #2
DD = sys.argv[2]
#print 'DD', DD, type(DD)

# numb_rep = #3
n_rea = sys.argv[3]
#print 'n', n_rea, type(n_rea)

directory = '../dati/L_'+str(LL)+'/D_'+str(DD)
if not os.path.exists(LOCAL+os.sep+directory):
	os.makedirs(LOCAL+os.sep+directory)



PATH_now = LOCAL+os.sep+directory+os.sep

nomefile = str('CdC-L_'+str(LL)+'.npy')
Tab_CdC  = np.load(LOCAL+os.sep+nomefile)
orario = strftime("%Y-%m-%d %H:%M:%S", gmtime())

with open('../fatti.dat', 'a') as ee:
	ee.write('\niniziato	L '+str(LL)+' D '+str(DD)+' nr '+str(n_rea)+'		alle ore '+str(orario))


start = time.time()

diagonal.ExactDiagonalization(PATH_now,LL,DD,2.0,Tab_CdC)

end = time.time()
tempotras = (end - start)
with open('../fatti.dat', 'a') as ee:
	ee.write('\n	finito	L '+str(LL)+' D '+str(DD)+' nr '+str(n_rea)+'	tempo '+str(tempotras))

