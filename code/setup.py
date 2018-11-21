from distutils.core import setup
from Cython.Build import cythonize

setup(
	ext_modules = cythonize(['f_function.py'])
)

# python setup.py build_ext --inplace
