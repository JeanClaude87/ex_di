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

ff.medie_matrices(directory,names_Corr_files,names_Corr_folds)


if not os.path.exists("../plot/dati_fit"):
	os.makedirs("../plot/dati_fit")
