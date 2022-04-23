from ._base import SpecificationCompositeBase
from pmaf.pipe.specs._inventory._primitive._ti import SpecTI
from pmaf.pipe.specs._inventory._primitive._ip import SpecIP
from pmaf.pipe.specs._inventory._primitive._is import SpecIS
from pmaf.phylo.branchest._metakit import BranchEstimatorBackboneMetabase
from pmaf.pipe.agents.dockers._mediums._phy_medium import DockerPhylogenyMedium
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium
import numpy as np


class SpecTSPBP(SpecificationCompositeBase):
    """Taxonomy -> Phylogeny/Topology + Sequence Alignments -> Branched
    Phylogeny."""

    def __init__(self, *args, branch_estimator, **kwargs):
        if not isinstance(branch_estimator, BranchEstimatorBackboneMetabase):
            raise TypeError("`branch_estimator` has invalid type.")
        self.__branch_estimator = branch_estimator
        self.__outlet = DockerPhylogenyMedium
        tdi_spec = SpecTI(*args, **kwargs)
        self.__ids_spec = SpecIS(*args, **kwargs)
        self.__idp_spec = SpecIP(*args, **kwargs)
        tmp_specs = [tdi_spec, self.__ids_spec, self.__idp_spec]
        tmp_steps = tdi_spec.steps + self.__define_lazy_steps()
        super().__init__(_specs=tmp_specs, _steps=tmp_steps)

    def __define_lazy_steps(self):
        steps_dict = [
            (
                "identifier-to-phylogeny-sequence-to-phylogeny",
                self.__checkpoint_identifier_to_branched_phylogeny,
                DockerPhylogenyMedium,
                "Retrieve phylogeny and sequences from database by identifiers. Followed by branch estimation to produce branched phylogeny..",
            )
        ]
        return steps_dict

    def __checkpoint_identifier_to_branched_phylogeny(self, docker, *args, **kwargs):
        alignment_docker = self.__ids_spec.fetch(docker, *args, **kwargs)
        phylogeny_docker = self.__idp_spec.fetch(docker, *args, **kwargs)
        if not phylogeny_docker.singleton:
            raise NotImplementedError
        tmp_branched_phylos = dict.fromkeys(phylogeny_docker.index, None)
        for ix, phylo in phylogeny_docker.get_iterator(exclude_missing=True):
            tmp_phylo = phylo.copy()
            tip_ids = np.asarray(list(map(int, tmp_phylo.tip_names)))
            tip_seqs = alignment_docker.to_multiseq(tip_ids)
            tmp_phylo.unroot()
            branched_tree = self.__branch_estimator.estimate(tip_seqs, tmp_phylo)
            tmp_branched_phylos[ix] = branched_tree

        new_metadata = {
            "master": {
                phylogeny_docker.__class__.__name__: phylogeny_docker.wrap_meta(),
                alignment_docker.__class__.__name__: alignment_docker.wrap_meta(),
            }
        }
        branched_phylogeny_docker = DockerPhylogenyMedium(
            tmp_branched_phylos, name=docker.name, metadata=new_metadata
        )
        return branched_phylogeny_docker, args, kwargs

    @property
    def outlet(self):
        """:class:`.DockerPhylogenyMedium`"""
        return DockerPhylogenyMedium

    @property
    def inlet(self):
        """:class:`.DockerTaxonomyMedium`"""
        return DockerTaxonomyMedium
