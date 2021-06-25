from ._base import SpecificationPrimitiveBase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase
from pmaf.pipe.agents.miners._miner import Miner
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium
from pmaf.pipe.agents.dockers._metakit import DockerTaxonomyMetabase,DockerBackboneMetabase
from pmaf.pipe.agents.mediators._metakit import MediatorTaxonomyMetabase

class SpecTI(SpecificationPrimitiveBase):
    """Taxonomy -> Identifier."""
    def __init__(self, mediator, factor, **kwargs):
        if not isinstance(mediator,MediatorTaxonomyMetabase):
            raise TypeError('`mediator` must be instance of MediatorTaxonomyMetabase.')
        if isinstance(factor,FactorBackboneMetabase):
            if not mediator.verify_factor(factor):
                raise ValueError('`factor` is not supported by database.')
        else:
            raise TypeError('`factor` has invalid type.')
        tmp_miner = Miner(mediator=mediator,factor=factor,**kwargs)
        tmp_steps = self.__define_lazy_steps()
        super().__init__(_steps=tmp_steps,_miner=tmp_miner)

    def __define_lazy_steps(self):
        steps_dict = [('verify-input',self.__checkpoint_verify_input, DockerTaxonomyMedium, 'Verify Input.'),
                      ('taxonomy-to-identifier', self.__checkpoint_taxonomy_to_identifier, DockerIdentifierMedium, 'Retrieve identifiers by taxonomy.')]
        return steps_dict

    def __checkpoint_verify_input(self,input,*args,**kwargs):
        if not isinstance(input, DockerBackboneMetabase):
           tmp_docker =  DockerTaxonomyMedium(input,**kwargs)
        else:
            tmp_docker = input
        if self.miner.verify_docker(tmp_docker):
            return tmp_docker, args, kwargs
        else:
            raise ValueError('`docker` is not supported by current specification.')

    def __checkpoint_taxonomy_to_identifier(self,docker,*args,**kwargs):
        identifiers = next(self.miner.yield_identifier_by_docker(docker, **kwargs))
        return identifiers, args, kwargs

    def verify_docker(self, docker):
        return self.miner.verify_docker(docker) and isinstance(docker, DockerTaxonomyMetabase)

    @property
    def inlet(self):
        """:class:`.DockerTaxonomyMedium`"""
        return DockerTaxonomyMedium

    @property
    def outlet(self):
        """:class:`.DockerIdentifierMedium`"""
        return DockerIdentifierMedium
