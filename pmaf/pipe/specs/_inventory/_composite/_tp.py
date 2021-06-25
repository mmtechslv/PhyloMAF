from ._base import  SpecificationCompositeBase
from pmaf.pipe.specs._inventory._primitive._ti import SpecTI
from pmaf.pipe.specs._inventory._primitive._ip import SpecIP
from pmaf.pipe.agents.dockers._mediums._phy_medium import DockerPhylogenyMedium
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium

class SpecTP(SpecificationCompositeBase):
    """Taxonomy - Phylogeny(reference tree)"""
    def __init__(self, *args, **kwargs):
        tmp_specs = [SpecTI(*args, **kwargs), SpecIP(*args, **kwargs)]
        tmp_steps = [step for spec in tmp_specs for step in spec.steps]
        super().__init__(_specs=tmp_specs,_steps=tmp_steps)

    @property
    def inlet(self):
        """:class:`.DockerTaxonomyMedium`"""
        return DockerTaxonomyMedium

    @property
    def outlet(self):
        """:class:`.DockerPhylogenyMedium`"""
        return DockerPhylogenyMedium
