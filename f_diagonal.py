import numpy as np
import time 
import scipy.special as special
import f_function as ff


def ExactDiagonalization(PATH_now,LL,DD,VV,n_r,rank,Tab_CdC):

	t0=time.time()
	#.PARAMETERS.......................................boundary conditions
	#...................BC=0 periodic, BC=1 open
	BC		= 0				
	#..................................................hopping & interactions
	t		= -1.
	#V		= 2.
	#..................................................disorder parameters
	#...................dis_gen=0 random, dis_gen=1 quasiperiodic
	Dis_gen = 1
	#..................................................Supspace dimension
	NN  = int(LL/2)
	Dim = int(special.binom(LL,NN))

	#..................................................Base creation
	Base_Num = ff.Base_prep(LL,NN)
	Base_Bin = [int(Base_Num [i],2) for i in range(Dim)]

	#..................................................Hopping creation
	if BC == 1:
		Hop_dim=LL-1
	else:
		Hop_dim=LL

	Hop_Num = ff.Hop_prep(LL,BC)
	Hop_Bin = [int(Hop_Num[i],2) for i in range(Hop_dim)]

	#..................................................Lin Tab creation
	LinTab = ff.LinTab_Creation(LL,Base_Num,Dim)

	#.............................Disorder creation
	Dis_real = ff.Dis_Creation(DD,LL,Dis_gen,rank)


	#.............................Diagonalization HAM
	HAM   = ff.Ham_Dense_Creation(LL,NN,Dim,t,VV,Dis_real,BC,Base_Bin,Base_Num,Hop_Bin,LinTab)
	E,V   = ff.eigval(HAM)	

	#V[Psi0] proiezioni
	#V[:,Psi0] autovettori

	#.............................Initial state
	Psi0		= ff.Psi_0(Dim,Base_Bin,LL,LinTab)
	Proj_Psi0   = ff.Proj_Psi0(Psi0,V)


	entropy = -np.sum(Proj_Psi0*np.log2(Proj_Psi0))

	nomefile_ent = str(PATH_now+'entr-'+str(n_r)+'.dat')
	with open(nomefile_ent, 'w') as ee:
		ee.write('%f' % entropy)

	#.............................Densita
	Base_NumRes = ff.BaseNumRes_creation(Dim,LL,Base_Num)
	Base_Corr	= ff.OUTER_creation(LL,Dim,Base_NumRes)

	Dens		= np.dot(np.transpose(V**2),Base_NumRes)
	DensDens	= ff.OUTER_creation(LL,Dim,Dens)

	#.............................NN
	NN_Conn	   = ff.Mat_CorrConn_Psi0(V,Base_Corr,Proj_Psi0,DensDens)
	NN_Conn_tr = ff.Trasl_Mean(NN_Conn)

	nomefile_NN = str('corr_n-'+str(n_r)+'.dat')
	np.savetxt(PATH_now+nomefile_NN, NN_Conn_tr, fmt='%.9f')

#	nomefile_NN1 = str('corr_n1-'+str(n_r)+'.dat')
#	np.savetxt(PATH_now+nomefile_NN1, NN_Conn, fmt='%.9f')


	#.............................CiCj
#	CdC    = ff.Mat_CdC_Psi0(Tab_CdC,Proj_Psi0,Dim,LL,V)
#	CdC_tr = ff.Trasl_Mean(CdC)

#	nomefile_cc = str('corr_c-'+str(n_r)+'.dat')
#	np.savetxt(PATH_now+nomefile_cc, CdC_tr, fmt='%.9f')

	return 1







