from setuptools import setup, find_packages
from Cython.Build import cythonize
from distutils.extension import Extension
from setuptools.command.build_ext import build_ext as _build_ext
import os

USE_CYTHON = os.environ.get("USE_CYTHON", False)
ext = ".pyx" if USE_CYTHON else ".c"

cython_root = "pmaf/internal/_extensions/_cython/"
cpython_root = "pmaf/internal/_extensions/_cpython/"


class build_ext(_build_ext):
    def finalize_options(self):
        super().finalize_options()
        build_py = self.get_finalized_command("build_py")
        self.inplace = True


ext_modules = [
    Extension(
        "pmaf.internal._extensions.PMAFCEXT",
        sources=[
            cpython_root + "_pmafc_extension/_source/c_parser.c",
            cpython_root + "_pmafc_extension/_source/c_hmerizer.c",
        ],
        include_dirs=[cpython_root + "_pmafc_extension/_source"],
    ),
] + cythonize(
    Extension(
        "pmaf.internal._extensions.cython_functions",
        [cython_root + "_source/cython_functions" + ext],
    ),
    compiler_directives={"language_level": "3"},
)


print(ext_modules)
cmdclass = {"build_ext": build_ext}

setup(
    name="PhyloMAF",
    version="1.0",
    packages=find_packages(),
    url="https://github.com/mmtechslv/PhyloMAF",
    license="BSD-3-Clause",
    author="Farid Musa",
    author_email="farid.musa.h@gmail.com",
    install_requires=[
        "execnet",
        "biom-format",
        "Cython",
        "fuzzywuzzy",
        "pandas",
        "dateparser",
        "numpy",
        "pytest",
        "urllib3",
        "ete3",
        "tables",
        "biopython",
        "scikit-bio",
    ],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    description="Phylogenetic Microbiome Analysis Framework",
)
