import numpy as np
import time 
import scipy.special as special
import f_function as ff

def ExactDiagonalization(PATH_now,L,D,Tab_CdC):

	#here LL is the number L is the string
	# EVERYTHING IS IN UNIT OF t
	# t ---> is set to 1


	t0=time.time()
	#.PARAMETERS.......................................boundary conditions
	#...................BC=0 periodic, BC=1 open
	BC		= 0				
	#..................................................disorder parameters
	#...................dis_gen=0 random, dis_gen=1 quasiperiodic
	Dis_gen = 1

	#..................................................Supspace dimension
	LL = int(L)
	DD = float(D)

	NN  = int(LL/2)
	Dim = int(ff.comb(LL, NN))

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
	LinTab = ff.LinTab_Creation(int(LL),Base_Num,Dim)

	#.............................Disorder creation
	Dis_real = ff.Dis_Creation(LL,Dis_gen)

	print(DD*Dis_real)

	#.............................Diagonalization HAM
	HAM   = ff.Ham_Dense_Creation(LL,NN,Dim,DD,Dis_real,BC,Base_Bin,Base_Num,Hop_Bin,LinTab)
	#print HAM

	E,V   = ff.eigval(HAM)	

	#V[Psi0] proiezioni
	#V[:,Psi0] autovettori
	
	#.............................Level statistic
	#e_tre = int(Dim/3)
	#E_tre = E[e_tre:-e_tre]
	#Dim_tre = Dim-2*e_tre

	'''

	levst = ff.levstat(E,Dim)
	m_levst = np.mean(levst)
	
	nomefile_lev = str(PATH_now+'levst.dat')
	with open(nomefile_lev, 'a') as ee:
		ee.write('%f' % m_levst+"\n")

	'''

	#.............................Initial state
	Psi0		= ff.Psi_0(Dim)
	Proj_Psi0   = ff.Proj_Psi0(Psi0,V)
	
	'''

	entropy = -np.sum(Proj_Psi0**2*np.log2(Proj_Psi0**2))

	nomefile_ent = str(PATH_now+'entr-')
	with open(ff.generate_filename(nomefile_ent), 'w') as ee:
		ee.write('%f' % entropy)

	'''
	#.............................Densita
	Base_NumRes = ff.BaseNumRes_creation(Dim,LL,Base_Num)
	Base_Corr	= ff.OUTER_creation(LL,Dim,Base_NumRes)

	Dens		= ff.density(V,Base_NumRes)
	DensDens	= ff.OUTER_creation(LL,Dim,Dens)

	#print(" ... ", Dens)




	'''

	#.............................SzSz Piero & Huse
	SzSz_con_P		= ff.SzSz_con_P(V,Base_Corr,DensDens)	
	SzSz_con_P_Psi0 = ff.SzSz_con_P_Psi0(Proj_Psi0**2,SzSz_con_P)

	SzSz_con_Huse   = ff.SzSz_con_Huse(SzSz_con_P)
	SzSz_con_Huse_t = ff.SzSz_con_Huse_t(SzSz_con_P)

	nomef_NN_P	= str('corr_P-')

	np.savetxt(ff.generate_filename(PATH_now+nomef_NN_P), SzSz_con_P_Psi0, fmt='%.9f')

	nomef_NN_H	= str('corr_H-')
	np.savetxt(ff.generate_filename(PATH_now+nomef_NN_H), SzSz_con_Huse, fmt='%.9f')

	nomef_NN_Ht	= str('corr_H_t-')
	np.savetxt(ff.generate_filename(PATH_now+nomef_NN_Ht), SzSz_con_Huse_t, fmt='%.9f')


	#.............................SzSz DE
	SzSz_DE			= ff.Mat_SzSz_DE(V,Base_Corr,Proj_Psi0**2)
	Sz_DE  			= ff.Mat_Sz_DE(Dens,Proj_Psi0**2)
	SzSz_con_DE		= ff.SzSz_con_DE(Proj_Psi0**2,SzSz_DE,Sz_DE)

	nomef_NN_DE	= str('corr_DE-')
	np.savetxt(ff.generate_filename(PATH_now+nomef_NN_DE), SzSz_con_DE, fmt='%.9f')


	#.............................CiCj
	CdC    = ff.Mat_CdC_Psi0(Tab_CdC,Proj_Psi0**2,Dim,LL,V)

	nomefile_cc = str('corr_c-')
	np.savetxt(ff.generate_filename(PATH_now+nomefile_cc), CdC, fmt='%.9f')

	'''


	#.............................Evolution

	#if 0 linear, 1 log

	Lo_Li = 0 

	t_i		= 0
	t_f		= 1.0
	t_step 	= 0.1

	t_tab = np.arange(t_i,t_f,t_step)


	t_Nstep  = t_tab.shape[0]
#	corr_tab = np.zeros((t_Nstep,LL,LL), dtype=np.float)
	
#	corr_tab = [ff.Corr_Evolution(Proj_Psi0,E,V,t,Base_NumRes,Base_Corr)[2] for t in t_tab]
	
	i=0
	for t in range(t_Nstep):
		corr_tab = ff.Corr_Evolution(Proj_Psi0,E,V,t_tab[t],Base_NumRes,Base_Corr)[0]
		print("t=",t_tab[t])
		print(corr_tab)

		i+=1

	nomef_corr_con_t	= str('corr_con_t-')
	#np.savetxt(ff.generate_filename(PATH_now+nomef_corr_con_t), corr_tab, fmt='%.9f')

	return 1

	






