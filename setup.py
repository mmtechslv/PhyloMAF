from setuptools import setup

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
    description="Phylogenetic Microbiome Analysis Framework",
)
## Cython and Cpython extension must be compiled
