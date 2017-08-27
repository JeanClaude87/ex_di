#!/usr/bin/python
import numpy as np
import f_diagonal as diagonal
import f_function as ff
import os
import sys

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

directory = 'L_'+str(LL)+'/D_'+str(DD)
if not os.path.exists(LOCAL+os.sep+directory):
	os.makedirs(LOCAL+os.sep+directory)


nomefile = str('CdC-L_'+str(LL)+'.npy')
Tab_CdC  = np.load(LOCAL+os.sep+nomefile)

PATH_now = LOCAL+os.sep+directory+os.sep
		

diagonal.ExactDiagonalization(PATH_now,LL,DD,2.0,n_rea,1,Tab_CdC)