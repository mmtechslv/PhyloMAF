r"""
PhyloMAF  (:mod:`pmaf`)
=======================

.. rubric:: Phylogenetic Microbiome Analysis Framework

.. currentmodule:: pmaf

PhyloMAF is a novel comprehensive microbiome data analysis tool based
on Python programming language. With memory efficient and extensible design, PhyloMAF
have wide range of applications including but not limited to: post OTU picking
microbiome data analysis, microbiome data meta-analysis, taxonomy based reference
phylogenetic tree pruning and reconstruction, cross database data validation,
primer design by taxonomic ranks, heterogeneous data retrieval from different
databases including remote mega-databases like NCBI or Ensembl.

.. rubric:: Currently available packages and modules

.. toctree::
   :maxdepth: 1

   pmaf.alignment
   pmaf.biome
   pmaf.database
   pmaf.internal
   pmaf.phylo
   pmaf.pipe
   pmaf.remote
   pmaf.sequence


"""

import warnings as __warnings_
import tables as __tables_
import sys as __sys_
import os as __os_

if __sys_.platform == 'win32':
    __sep_ = ';'
else:
    __sep_ = ':'

__os_.environ['PATH'] += __sep_ + __sys_.prefix
__os_.environ['PATH'] += __sep_ + __sys_.prefix + '/bin'


__warnings_.filterwarnings(action='ignore', category=__tables_.NaturalNameWarning,module='tables')
__warnings_.filterwarnings(action='ignore', category=__tables_.PerformanceWarning,module='tables')

from . import database
from . import biome
from . import alignment
from . import phylo
from . import pipe
from . import remote
from . import sequence

__all__ = ['database','biome','alignment','phylo','pipe','remote','sequence']
