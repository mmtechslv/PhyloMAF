import os
from org.opentreeoflife.taxa import Taxonomy

from org.opentreeoflife.smasher import UnionTaxonomy
all_ott = Taxonomy.getTaxonomy('/home/mmtechslv/akasha/DGRPy/ext/ott/', 'all')


metazoa = all_ott.taxon('Metazoa', 'life')
insecta = all_ott.taxon('Insecta', 'life')

metazoa.prune()
insecta.prune()

all_ott.check()

all_ott.dump('/home/mmtechslv/akasha/DGRPy/ext/ott/new/', '|')
all_ott.dumpNewick('/home/mmtechslv/akasha/DGRPy/ext/ott/new/tree.tre')
