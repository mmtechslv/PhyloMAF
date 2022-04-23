from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(
        "./source/cython_functions.pyx", compiler_directives={"language_level": "3"}
    )
)
