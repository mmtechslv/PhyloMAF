from ._base import  SpecificationCompositeBase
from pmaf.pipe.specs._inventory._primitive._ti import SpecTI
from pmaf.pipe.specs._inventory._primitive._is import SpecIS
from pmaf.phylo.builders._metakit import TreeBuilderBackboneMetabase
from pmaf.pipe.agents.dockers._mediums._phy_medium import DockerPhylogenyMedium
from pmaf.pipe.agents.dockers._mediums._seq_medium import DockerSequenceMedium

class SpecTSBP(SpecificationCompositeBase):
    def __init__(self, *args, tree_builder,  **kwargs):
        if not isinstance(tree_builder,TreeBuilderBackboneMetabase):
            raise TypeError('`tree_builder` has invalid type.')
        self.__tree_builder = tree_builder
        self.__outlet = DockerPhylogenyMedium
        tmp_specs = [SpecTI(*args, **kwargs), SpecIS(*args, **kwargs)]
        tmp_steps = [step for spec in tmp_specs for step in spec.steps]
        tmp_steps = tmp_steps + self.__define_lazy_steps()
        super().__init__(_specs=tmp_specs,_steps=tmp_steps)

    def __define_lazy_steps(self):
        steps_dict = [('sequence-to-phylogeny', self.__checkpoint_sequence_to_branched_phylogeny, DockerPhylogenyMedium,'Retrieve aligned sequences from database by identifiers. Followed by de-novo building phylogenetic tree.')]
        return steps_dict

    def __checkpoint_sequence_to_branched_phylogeny(self,docker,*args,**kwargs):
        if isinstance(docker,DockerSequenceMedium):
            if not docker.aligned:
                RuntimeError('`docker` must be alignment.')
        else:
            raise RuntimeError('`docker` must be DockerSequenceMedium.')
        if not docker.singleton:
            raise NotImplementedError

        alignment = docker.to_multiseq()
        builded_tree = self.__tree_builder.build(alignment)

        new_metadata = {'master': {docker.__class__.__name__:docker.wrap_meta()}}
        branched_phylogeny_docker = DockerPhylogenyMedium([builded_tree],name=docker.name,metadata=new_metadata)
        return branched_phylogeny_docker, args, kwargs

    @property
    def outlet(self):
        return DockerPhylogenyMedium





