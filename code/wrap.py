#!/usr/bin/python
import numpy as np
import f_function as ff
import os
import sys
from time import gmtime, strftime
import time
from mpi4py import MPI
from random import randint

from scipy.sparse import linalg
from scipy.sparse import csc_matrix

COMM = MPI.COMM_WORLD

LOCAL = os.path.abspath('.')

# LL = #1
LL = sys.argv[1]

# DD = #2
DD = sys.argv[2]

# numb_rep = #3
n_rea = sys.argv[3]


directory = '../dati_0/L_'+str(LL)+'/D_'+str(DD)
if not os.path.exists(LOCAL+os.sep+directory):
	os.makedirs(LOCAL+os.sep+directory)


PATH_now = LOCAL+os.sep+directory+os.sep

nomefile = str('CdC-L_'+str(LL)+'.npy')


orario = strftime("%Y-%m-%d %H:%M:%S", gmtime())

with open('../fatti.dat', 'a') as ee:
	ee.write('\niniziato	L '+str(LL)+' D '+str(DD)+' nr '+str(n_rea)+'		alle ore '+str(orario))


start = time.time()

#diagonal.ExactDiagonalization(PATH_now,LL,DD)


#.PARAMETERS.......................................boundary conditions
#...................BC=0 periodic, BC=1 open
BC		= 0				
#..................................................disorder parameters
#...................dis_gen=0 random, dis_gen=1 quasiperiodic
Dis_gen = 0

#..................................................Supspace dimension
LL = int(LL)
DD = float(DD)

NN  = int(LL/2)
Dim = int(ff.comb(LL, NN))

if COMM.rank == 0:
    
	start = time.time()
	print('t0', start)

	#..................................................Base creation
	Base_Num       = ff.Base_prep(LL,NN)
	Base_Bin       = [int(Base_Num [i],2) for i in range(Dim)]
	Base_NumRes    = ff.BaseNumRes_creation(Dim,LL,Base_Num)
	Base_Corr      = ff.OUTER_creation(LL,Dim,Base_NumRes)
	Dis_real = ff.Dis_Creation(LL,Dis_gen)

else:

	Base_Num    = None
	Base_Bin    = None
	Base_NumRes = None
	Dis_real	= None

COMM.Barrier()

Base_Bin        = COMM.bcast(Base_Bin,	  root=0)
Base_Num        = COMM.bcast(Base_Num,    root=0)
Base_NumRes     = COMM.bcast(Base_NumRes, root=0)
Dis_real        = COMM.bcast(Dis_real,	  root=0)

	#..................................................Hopping creation
if BC == 1:
	Hop_dim=LL-1
else:
	Hop_dim=LL

Hop_Num = ff.Hop_prep(LL,BC)
Hop_Bin = [int(Hop_Num[i],2) for i in range(Hop_dim)]

#..................................................Lin Tab creation
LinTab = ff.LinTab_Creation(int(LL),Base_Num,Dim)

########################################
########################################
########################################
#################..MPI..################
########################################
########################################
########################################

t=1.
	# tutto in unita di t!!

if COMM.rank == 0:
    
	start1 = time.time()
	print('inizia ham', start1-start)

if COMM.rank == 0:
	jobs = list(range(Dim))
	jobs = ff.split(jobs, COMM.size)
else:
	jobs = None

COMM.Barrier()

jobs = COMM.scatter(jobs, root=0)

ham_ind1 = []
ham_ind2 = []
ham_val  = []

for i in jobs:

	n_int = 0.0
	n_dis = 0.0
	bra = ff.LinLook(Base_Bin[i],LL,LinTab)

	for j in range(Hop_dim):
		xx  = Base_Bin[i]^Hop_Bin[j]
		ket = ff.LinLook(xx,LL,LinTab)
		
		if ff.one_count(xx) == NN:

			ham_ind1.append( bra )
			ham_ind2.append( ket )
			ham_val.append(  t/2 )

		uu = Base_Bin[i] & Hop_Bin[j]

		if ff.one_count(uu) == 1:
			n_int -= 0.25
		else: 
			n_int += 0.25

		n_ones = Base_Bin[i] & int(2**(LL-j-1)) 
		if n_ones != 0:
			n_dis += 0.5*Dis_real[j]
		else:
			n_dis -= 0.5*Dis_real[j]

	ham_ind1.append( bra )
	ham_ind2.append( bra )
	ham_val.append(  t*(0*n_int + DD*n_dis) )

COMM.Barrier()

ham_ind1_0 = MPI.COMM_WORLD.gather( ham_ind1, root=0)
ham_ind2_0 = MPI.COMM_WORLD.gather( ham_ind2, root=0)
ham_val_0  = MPI.COMM_WORLD.gather( ham_val,  root=0)

COMM.Barrier()

if COMM.rank == 0:

	X1 = [item for sublist in ham_ind1_0 for item in sublist]
	Y1 = [item for sublist in ham_ind2_0 for item in sublist]
	A1 = [item for sublist in ham_val_0  for item in sublist]
    
	start2 = time.time()
	print('sparsa ham', start2-start1)

	ham = csc_matrix((A1, (X1,Y1)), shape=(Dim,Dim), dtype=np.double)

	psi_0   = np.zeros(Dim, dtype=np.float)
	psi_0[randint(0, Dim-1)] = 1

	dt       = 0.1
	step_num = 500
	t_i 	 = 0
	t_f 	 = dt*step_num

	A        = -1.0J*ham

	start3 = time.time()
	print('inizip evoluzione', start3-start2)

	psit     = linalg.expm_multiply(A, psi_0, start=t_i, stop=t_f, num=step_num+1, endpoint=True)

	start4 = time.time()
	print('psit', start4-start3)

	corr     = np.zeros((step_num,LL), dtype=np.float)
	
	for i in range(step_num):

		pro = psit[i]

		con_SzSz = ff.SPARSE_SzSz_con_DE(pro,Base_Corr,Base_NumRes)
		media    = ff.Trasl_Mean(con_SzSz)

		corr[i] = media

	nome_c_sp	= str('corr_DE-sp-')
	np.savetxt(ff.generate_filename(PATH_now+nome_c_sp), corr, fmt='%.9f')

	start4 = time.time()
	print('corr', start4-start3)

########################################
########################################
########################################
########################################
########################################
########################################


end = time.time()
tempotras = (end - start)
with open('../fatti.dat', 'a') as ee:
	ee.write('\n	finito	L '+str(LL)+' D '+str(DD)+' nr '+str(n_rea)+'	tempo '+str(tempotras))



filenameRM='../uga-L_'+str(LL)+'-D_'+str(DD)+'-nr_'+str(n_rea)+'.inp'
if os.path.exists(filenameRM):
    os.remove(filenameRM)





