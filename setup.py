from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext

cython_root = "internal/_extensions/_cython/"
cpython_root = "internal/_extensions/_cpython/"

ext_modules = [
    cythonize(
        cython_root + "_source/cython_functions.pyx",
        compiler_directives={"language_level": "3"},
    ),
    Extension(
        "PMAFCEXT",
        sources=[
            cpython_root + "_pmafc_extension/_source/c_parser.c",
            cpython_root + "_pmafc_extension/_source/c_hmerizer.c",
        ],
        include_dirs=[cpython_root + "_pmafc_extension/_source"],
    ),
]

cmdclass = {"build_ext": build_ext}

setup(
    name="PhyloMAF",
    version="1.0",
    packages=[
        "pmaf",
        "pmaf.pipe",
        "pmaf.biome",
        "pmaf.phylo",
        "pmaf.remote",
        "pmaf.database",
        "pmaf.sequence",
        "pmaf.alignment",
    ],
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
        "pytables",
        "biopython",
        "scikit-bio",
    ],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    description="Phylogenetic Microbiome Analysis Framework",
)
