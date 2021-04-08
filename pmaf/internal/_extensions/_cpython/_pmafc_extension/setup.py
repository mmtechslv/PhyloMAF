from distutils.core import setup, Extension
from Cython.Build import cythonize

ext_type = Extension("PMAFCEXT",
                     sources=["./_source/c_parser.c",
                              "./_source/c_hmerizer.c"])

setup(name="PMAFCEXT",
      description="Python interface for PhyloMAF C Extension.",
      author="Farid MUSA",
      author_email="mmtechslv@gmail.com",
      ext_modules = [ext_type])

#python setup.py build_ext --inplace
