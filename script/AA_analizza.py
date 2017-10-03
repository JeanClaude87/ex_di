from mpi4py import MPI
import numpy as np
from glob import glob
import re
import time
import os as os


import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import AA_functions as ff

names_Corr_files = ['corr_c','corr_H'   ,'corr_H_t'   ,'corr_DE','corr_DE_t','corr_P']
names_Corr_folds = ['SpSm'  ,'SzSz_Huse','SzSz_Huse_t','SzSz_DE','SzSz_DE_t','SzSz_P']


directory = glob('../dati/*/*/')

if not os.path.exists("../strange_files/"):
		os.makedirs("../strange_files/")

if not os.path.exists("../plot/dati_fit"):
	os.makedirs("../plot/dati_fit")

print len(directory)

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

for i,j in enumerate(directory):

	if i%size!=rank: continue

	numCO   = len(names_Corr_files)
	ff.medie_matrices(j,names_Corr_files,names_Corr_folds,numCO)





