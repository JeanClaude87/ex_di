from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize('AA_f*.py')
)




# python setup.py build_ext --inplace
