import numpy as np
import os.path
import math
import scipy.linalg as _la
from math import factorial
import itertools
import time 
import os
from scipy.sparse import csc_matrix

#..................................counting number of one
POPCOUNT_TABLE16 = [0] * 2**16
for index in range(len(POPCOUNT_TABLE16)):
	POPCOUNT_TABLE16[index] = (index & 1) + POPCOUNT_TABLE16[index >> 1]

def one_count(v):
	return (POPCOUNT_TABLE16[ v        & 0xffff] +
			POPCOUNT_TABLE16[(v >> 16) & 0xffff])


#..................................Binomial
def comb(n, k):
	kk = factorial(n) / factorial(k) / factorial(n - k)
	uga= np.int64(kk)
	return uga


#..................................from configuration to bin number
def TO_bin(xx):
	return int(xx,2)

#..................................from bin number to configuration
def TO_con(x,L):
	x1=np.int64(x)
	L1=np.int64(L)
	return np.binary_repr(x1, width=L1)


#..................................base preparation
def Base_prep(n,k):
	result = []
	for bits in itertools.combinations(range(n), k):
		s = ['0'] * n
		for bit in bits:
			s[bit] = '1'
		result.append(''.join(s))
	return result

def BaseNumRes_creation(Dim,LL,B):
	A=np.zeros((Dim,LL), dtype=np.float)

	for i in range(Dim):
		k=0
		for j in list(B[i]):
			A[i,k] = float(j)-0.5
			k+=1
	return A

#..................................hop. preparation
def Hop_prep(L,BC):
	if BC == 1:
		Hop_dim=L-1
	else:
		Hop_dim=L
	return [TO_con(2**i+2**((i+1)%L),L) for i in range(Hop_dim)]


#..................................................Disorder creation
def Dis_Creation(LL,Dis_gen):

	dis = np.zeros(LL, dtype=np.float)
	for i in range(LL):
		if Dis_gen==0: 
			dis[i] = 2*np.random.random()-1
		else:
			dis[i] = np.cos(2*math.pi*0.721*i/LL)
	return dis


#..................................creation Lin Tables
def LinTab_Creation(LL,Base,di):

	L = np.int64(LL)
	Dim=np.int64(di)

#..........................Table Creation
	MaxSizeLINVEC = sum([2**(i-1) for i in range(1,np.int64(L/2+1))])

	#....creates a table LinTab_L+LinTab_R
	#.....................[  ,  ]+[  ,  ]
	LinTab   = np.zeros((MaxSizeLINVEC+1,4),dtype=int)
	Jold     = JJ=j1=j2=0
	Conf_old = TO_con(0,np.int64(L/2))

#...........................Table Filling
	for i in range(Dim):
		Conf_lx = Base[i][0:np.int64(L/2)]
		Bin_lx  = TO_bin(Conf_lx)
		Conf_rx = Base[i][np.int64(L/2):L]		
		Bin_rx  = TO_bin(Conf_rx)

		if Conf_lx==Conf_old:
			j1 = Jold
		else:
			j1 += j2

		Conf_old = Conf_lx 

		if Jold != j1:	
			JJ = Jold = 0

		j2	= JJ+1
		Jold = j1
		JJ  += 1

		#print Conf_lx, np.int64(Bin_lx), np.int64(j1), Conf_rx, np.int64(Bin_rx), np.int64(j2)

		LinTab[Bin_lx,0]= np.int64(Bin_lx)
		LinTab[Bin_lx,1]= np.int64(j1)
		LinTab[Bin_rx,2]= np.int64(Bin_rx)
		LinTab[Bin_rx,3]= np.int64(j2)

#	print LinTab
	return LinTab

#..................................Lin Look for complete state
def LinLook(vec,LL,arr):

	Vec  = TO_con(vec,LL)
	v1	 = Vec[0:np.int64(LL/2)]
	v2	 = Vec[np.int64(LL/2):LL]
	ind1 = TO_bin(v1)
	ind2 = TO_bin(v2)
	return arr[ind1,1]+arr[ind2,3]-1

#..................................Lin Look for RIGHT state
def LinLook_LL(vec,arr):
	ind=TO_bin(vec)
	return arr[ind+1,1]


#..................................Lin Look for RIGHT state
def LinLook_RR(vec,arr):
	ind=TO_bin(vec)
	return arr[ind+1,3]


#..................................................Hamiltonian Creation
def Ham_Dense_Creation(LL,NN,Dim,D,Dis_real,BC,Base_Bin,Base_Num,Hop_Bin,LinTab):

	t=1.
	# tutto in unita di t!!

	ham = np.zeros((Dim,Dim), dtype=np.float)

	if BC == 1:
		Hop_dim=LL-1
	else:
		Hop_dim=LL

	for i in range(Dim):
		n_int = 0.0
		n_dis = 0.0
		bra = LinLook(Base_Bin[i],LL,LinTab)

		for j in range(Hop_dim):
			xx  = Base_Bin[i]^Hop_Bin[j]
			ket = LinLook(xx,LL,LinTab)
			
			if one_count(xx) == NN:
				ham[bra,ket] = t/2
			uu = Base_Bin[i] & Hop_Bin[j]
			
			if one_count(uu) == 1:
				n_int -= 0.25
			else: 
				n_int += 0.25

			n_ones = Base_Bin[i] & np.int64(2**(LL-j-1)) 
			if n_ones != 0:
				n_dis += 0.5*Dis_real[j]
			else:
				n_dis -= 0.5*Dis_real[j]

		ham[bra,bra] = t*(0*n_int + D*n_dis)

	return ham


#..................................................Hamiltonian Creation
def Ham_Sparse_Creation(LL,NN,Dim,D,Dis_real,BC,Base_Bin,Base_Num,Hop_Bin,LinTab):

	t=1.
	# tutto in unita di t!!

	ham_ind1 = []
	ham_ind2 = []
	ham_val  = []


	if BC == 1:
		Hop_dim=LL-1
	else:
		Hop_dim=LL

	for i in range(Dim):
		n_int = 0.0
		n_dis = 0.0
		bra = LinLook(Base_Bin[i],LL,LinTab)

		for j in range(Hop_dim):
			xx  = Base_Bin[i]^Hop_Bin[j]
			ket = LinLook(xx,LL,LinTab)
			
			if one_count(xx) == NN:

				ham_ind1.append( bra )
				ham_ind2.append( ket )
				ham_val.append(  t/2 )

			uu = Base_Bin[i] & Hop_Bin[j]

			if one_count(uu) == 1:
				n_int -= 0.25
			else: 
				n_int += 0.25

			n_ones = Base_Bin[i] & np.int64(2**(LL-j-1)) 
			if n_ones != 0:
				n_dis += 0.5*Dis_real[j]
			else:
				n_dis -= 0.5*Dis_real[j]

		ham_ind1.append( bra )
		ham_ind2.append( bra )
		ham_val.append(  t*(0*n_int + D*n_dis) )

	ham = csc_matrix((ham_val, (ham_ind1,ham_ind2)), shape=(Dim,Dim), dtype=np.double)

	return ham


#..................................................Hamiltonian Dense Diagonalization
def eigval(A):
	E = _la.eigh(A)
	return E

#..................................................Hamiltonian Dense Diagonalization
def levstat(E,Dim):
	gap=E[1:]-E[:-1]
	B = np.zeros(Dim-2, dtype=np.float)
	for i in range(Dim-2):
		B[i]=np.minimum(gap[i+1],gap[i])/np.maximum(gap[i+1],gap[i])	
	return B

#..................................................Hamiltonian Sparse Diagonalization
def eigsh(A,n):
	E = _la.sparse.linalg.eigsh(A, n)
	return E

#..................................................Initial state
def Psi_0(Dim):
	n = np.random.randnp.int64(0,Dim-1)
	#n = 0
	return n

def Proj_Psi0(a,V):
	return V[a]


#..................................................Traslations MEAN
def Trasl_Mean(A):
	a = A.shape
	B = np.zeros((a[1],a[1]), dtype=np.float)
	for i in range(a[1]):
		B[i] = np.roll(A[i],-i)
	return np.mean(B, axis=0)

#..................................................dens
def density(V,Base_NumRes):
	den   = np.dot(np.transpose(V**2),Base_NumRes)
	#equivalente a fare:
	#dens = np.einsum('jn,jn,ji -> ni', V, V, Base_NumRes)
	return den

def density_t(Pro,V,BDens):
	den = np.einsum('i,ij,jk-> k', Pro, V, BDens)

	#np.dot(np.transpose(V**2),Base_NumRes)
	return den

#..................................................NiNj
def OUTER_creation(L,Dim,A):
	B = np.zeros((Dim,L,L), dtype=np.float)
	for i in range(Dim):
		B[i] = np.outer(A[i],A[i])
	return B

def SzSz_con_P(A,B,C):
	SzSz=np.einsum('il,ijk -> ljk', A**2, B)
	uga =SzSz-C
	return uga

def SzSz_con_P_Psi0(A,B):
	uga=np.einsum('i,ijk -> jk', A, B)
	return uga

def SzSz_con_Huse(A):
	L    = A.shape[0]
	uga_mat= np.einsum('ijk -> jk', np.absolute(A))
	uga  = uga_mat/L
	return uga

def SzSz_con_Huse_t(A):
	L    = A.shape[0]
	Aabs = np.absolute(A)
	Alog = np.log(Aabs)
	uga_mat  = np.einsum('ijk -> jk', Alog)
	uga  = uga_mat/L
	return uga

def Mat_SzSz_DE(A,B,C):
	#NN -> A V, B Base_Corr, C Proj_Psi0
	corr_zero=np.einsum('l,il,ijk -> jk',C, A**2, B)
	return corr_zero

def Mat_Sz_DE(A,B):
	#NN -> A Dens B Proj_Psi0
	corr_zero=np.einsum('i,ij -> j',B, A)
	return corr_zero

def SzSz_con_DE(A,B,C):
	#A proiezioni, B SzSz, C Sz
	Sz2=np.outer(C,C)
	uga=B-Sz2
	return uga

def SPARSE_SzSz_con_DE(psi_t,Base_Corr,Base_NumRes):

	#mean SzSz
	SzSz = np.einsum('i, ijk -> jk', np.abs(psi_t)**2, Base_Corr)

	#mean Sz
	Dens = np.dot(np.transpose(np.abs(psi_t)**2),Base_NumRes)
	Sz2  = np.outer(Dens,Dens)

	#connected correlations
	SzSz_con = SzSz - Sz2

	return SzSz_con


#..................................................CdiCj

def prep_tab(L):
	Dim = comb(L, np.int64(L/2))

	Base_Num = Base_prep(L,np.int64(L/2))
	Base_Bin = [int(Base_Num [i],2) for i in range(Dim)]
	LinTab   = LinTab_Creation(L,Base_Num,Dim)

	CdC_Tab  = CdC_tabCreation (L,np.int64(L/2),Dim,Base_Num,Base_Bin,LinTab)

	return CdC_Tab

def CdC_tabCreation (LL,NN,Dim,Base_Num,Base_Bin,LinTab):
	dimCiCj =  comb(LL-2, NN-1)
	CdC_Tab  =  np.zeros((LL,LL,dimCiCj,2), dtype=int)
	
	for i in range(LL):
		for j in range(LL):

			xx = np.zeros((dimCiCj,2), dtype=int)
			x0 = 0

			for l in range(Dim):

				a = Base_Num[l][0:i] 
				b = Base_Num[l][i+1:LL]
				c = ''.join([a,'1',b])
				a = c[0:j] 
				b = c[j+1:LL]
				d = ''.join([a,'0',b])
				if (one_count(int(d,2)) == NN and int(d,2) != Base_Bin[l]):
					bra = LinLook(Base_Bin[l],LL,LinTab)
					ket = LinLook(int(d,2),LL,LinTab)
				
					xx[x0,0] = np.int64(bra)
					xx[x0,1] = np.int64(ket)
					x0 += 1
				
			CdC_Tab[i,j] = xx

	return CdC_Tab

def Mat_CdC_i(UU1,LL,V,l):

	CC = np.zeros((LL,LL),dtype=float)

	for i in range(LL):
		for j in range(i,LL):
			uu = UU1[i,j]
			CC[j,i] = CC[i,j] = np.inner(V[uu[:,0],l],V[uu[:,1],l])
	np.fill_diagonal(CC, 0.25)
	return CC

def Mat_CdC_Psi0(UU1,Proj_Psi0,Dim,LL,V):

	CC = np.empty((Dim,LL,LL),dtype=float)

	for l in range(Dim):
		for i in range(LL):
			for j in range(i,LL):
				uu = UU1[i,j]
				CC[l,j,i] = CC[l,i,j] = np.inner(V[uu[:,0],l],V[uu[:,1],l])
				#print Dim, l, i, j, np.inner(V[uu[:,0],l],V[uu[:,1],l])
		np.fill_diagonal(CC[l], 0.25)
		
		CC[l] *= Proj_Psi0[l]

	CC1 = np.einsum('ijk -> jk', CC)

	return CC1

def generate_filename(basename):
	local_time = str(np.int64(round(time.time() * 1000)))
	xx = basename + local_time + ".dat"
	if os.path.isfile(xx):
		time.sleep(1)
		return generate_filename(basename)
	return xx

#..................................................Entropy

#..................................................Time - Evolution

def Corr_Evolution(Proj_Psi0,E,V,t,Base_NumRes,Base_Corr):
	Pro_t0 = Proj_Psi0 
	#c'era un V di troppo::: np.einsum('i,ki-> k', Proj_Psi0, V)

	Pro_t  = np.outer(Pro_t0*np.exp(1j*E*t),Pro_t0*np.exp(-1j*E*t))

	coef 	   = np.real(np.einsum('nm,jn,jm -> j', Pro_t, V, V))

	dens_t 	   = np.real(np.einsum('j,ji -> i',   coef, Base_NumRes))
	corr_t 	   = np.real(np.einsum('j,jli -> li', coef, Base_Corr))
	corr_con_t = np.real(corr_t - np.outer(dens_t,dens_t))

	corr_con_t_AVER = Trasl_Mean(corr_con_t)

	return dens_t,corr_t,corr_con_t_AVER


#..................................................Print_MATRIX
def print_matrix(H):

	#print('matrix to print')

	if isinstance(H, csc_matrix):
		print_h = csc_matrix.todense(H)
		print(print_h)
	else:
		print(H)

	return 0

def split(container, count):
	"""
	Simple function splitting a container into equal length chunks.
	Order is not preserved but this is potentially an advantage depending on
	the use case.
	"""
	return [container[_i::count] for _i in range(count)]

	