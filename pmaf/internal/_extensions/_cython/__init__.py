#!/usr/bin/env python3

from .cython_functions import generate_lineages_from_taxa_list as rapid_lineage_generator
from .cython_functions import generate_taxa_list_for_ott as rapid_ott_taxonomy_reader