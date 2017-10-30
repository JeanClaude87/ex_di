import numpy as np
import math
import scipy.linalg as _la
import scipy.special as special
from math import factorial
import time 
from datetime import datetime
import time
import re
import os as os
from glob import glob
from numpy import inf
import re


#..................................................Traslations MEAN
def Trasl_Mean(A):
	a = A.shape
	B = np.zeros((a[1],a[1]), dtype=np.float)
	for i in range(a[1]):
		B[i] = np.roll(A[i],-i)
	return np.mean(B, axis=0)

#..................................................FileName_abstime
def generate_filename(basename):
	unix_timestamp = int(time.time())
	local_time = str(int(round(time.time() * 1000)))
	xx = basename + local_time + ".dat"
	if os.path.isfile(xx):
		time.sleep(1)
		return generate_filename(basename)
	return xx		


#..................................................MEAN of FILES
def medie_matrices(i,namesCO,namesFO,numCO):
	string = re.split('/|_', i)
	L = string[-4]
	D = string[-2]
	L_int = int(L)

	for k in range(numCO):


		path_dir = "../medie/"+namesFO[k]+"/L_"+L
		if not os.path.exists(path_dir):
			os.makedirs(path_dir)

		path_dir2 = "../plot/dati_fit/"+namesFO[k]+"/plot"
		if not os.path.exists(path_dir2):
			os.makedirs(path_dir2)

		if namesCO[k]=='corr_DE_t':
			ciao = 'corr_DE'
		else:
			ciao = namesCO[k]

		files = glob(i + ciao + '-*')

		Nrel  = len(files)


		DataFrame = np.zeros((Nrel,L_int), dtype=np.float)
		print L, D, Nrel, namesCO[k]

		if namesCO[k]=="corr_DE_t":
			for j in range(Nrel):
				try:
					data = np.loadtxt(files[j], dtype=np.float)		
				except ValueError:
					print files[j]
					os.rename(files[j], "../strange_files/"+re.split('/', files[j])[-1])
				else:
					data_trs = Trasl_Mean(np.log(np.absolute(data)))
					data_trs[data_trs == -inf] = -25
					DataFrame[j] = data_trs 

		elif namesCO[k]=="corr_c":
			for j in range(Nrel):
				try:
					data = np.loadtxt(files[j], dtype=np.float)		
				except ValueError:
					print files[j]
					os.rename(files[j], "../strange_files/"+re.split('/', files[j])[-1])
				else:
					data_trs = Trasl_Mean(np.absolute(data))
					DataFrame[j] = data_trs

		else:
			for j in range(Nrel):
				try:
					data = np.loadtxt(files[j], dtype=np.float)		
				except ValueError:
					print files[j]
					os.rename(files[j], "../strange_files/"+re.split('/', files[j])[-1])

				else:
					data_trs = Trasl_Mean(data)
					data_trs[data_trs == -inf] = -25
					DataFrame[j] = data_trs

		#print [DataFrame]
		mean0 = np.mean(DataFrame, axis=0)
		mean  = np.append(mean0,mean0[0])
		#print mean0
		std0  = np.std(DataFrame, axis=0)
		std   = np.append(std0,std0[0])

		data_row = [range(L_int+1),mean,std]			
		data_exp = map(list, zip(*data_row))
		
		nomefile = "../medie/"+namesFO[k]+"/L_"+L+"/D_"+D+".dat"
		np.savetxt(nomefile, data_exp, fmt='%.9f')


	return 1


