from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize(['f_function.py','f_diagonal.py'])
)

# python setup.py build_ext --inplace
