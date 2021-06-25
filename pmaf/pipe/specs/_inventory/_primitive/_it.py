from ._base import SpecificationPrimitiveBase
from pmaf.pipe.agents.mediators._metakit import MediatorTaxonomyMetabase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase
from pmaf.pipe.agents.miners._miner import Miner
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase,DockerBackboneMetabase

class SpecIT(SpecificationPrimitiveBase):
    """Identifiers -> Taxonomy."""
    def __init__(self, mediator, factor, **kwargs):
        if not isinstance(mediator, MediatorTaxonomyMetabase):
            raise TypeError('`mediator` must be instance of MediatorTaxonomyMetabase.')
        if isinstance(factor, FactorBackboneMetabase):
            if not mediator.verify_factor(factor):
                raise ValueError('`factor` is not supported by database.')
        else:
            raise TypeError('`factor` has invalid type.')
        tmp_miner = Miner(mediator=mediator,factor=factor,**kwargs)
        tmp_steps = self.__define_lazy_steps()
        super().__init__(_steps=tmp_steps,_miner=tmp_miner)

    def __define_lazy_steps(self):
        steps_dict = [('verify-input',self.__checkpoint_verify_input, DockerTaxonomyMedium, 'Verify Input.'),
                      ('identifier-to-taxonomy', self.__checkpoint_identifier_to_taxonomy, DockerTaxonomyMedium, 'Retrieve taxonomy by indentifiers.')]
        return steps_dict

    def __checkpoint_verify_input(self,input,*args,**kwargs):
        if not isinstance(input, DockerBackboneMetabase):
            tmp_docker = DockerIdentifierMedium(input,**kwargs)
        else:
            tmp_docker = input
        if self.miner.verify_docker(tmp_docker):
            return tmp_docker, args, kwargs
        else:
            raise ValueError('`docker` is not supported by current specification.')

    def __checkpoint_identifier_to_taxonomy(self,docker,*args,**kwargs):
        taxonomy = next(self.miner.yield_taxonomy_by_identifier(docker, **kwargs))
        return taxonomy, args, kwargs

    @property
    def inlet(self):
        """:class:`.DockerIdentifierMedium`"""
        return DockerIdentifierMedium

    @property
    def outlet(self):
        """:class:`.DockerTaxonomyMedium`"""
        return DockerTaxonomyMedium
