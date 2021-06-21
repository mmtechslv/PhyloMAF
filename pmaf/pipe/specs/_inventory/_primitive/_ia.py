from ._base import SpecificationPrimitiveBase
from pmaf.pipe.agents.mediators._metakit import MediatorAccessionMetabase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase
from pmaf.pipe.agents.miners._miner import Miner
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._acs_medium import DockerAccessionMedium
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase,DockerBackboneMetabase

class SpecIA(SpecificationPrimitiveBase):
    """ """
    def __init__(self, mediator, factor, **kwargs):
        if not isinstance(mediator, MediatorAccessionMetabase):
            raise TypeError('`mediator` must be instance of MediatorAccessionMetabase.')
        if isinstance(factor, FactorBackboneMetabase):
            if not mediator.verify_factor(factor):
                raise ValueError('`factor` is not supported by database.')
        else:
            raise TypeError('`factor` has invalid type.')
        tmp_miner = Miner(mediator=mediator,factor=factor,**kwargs)
        tmp_steps = self.__define_lazy_steps()
        super().__init__(_steps=tmp_steps,_miner=tmp_miner)

    def __define_lazy_steps(self):
        steps_dict = [('verify-input',self.__checkpoint_verify_input, DockerIdentifierMedium, 'Verify Input.'),
                      ('identifier-to-accession', self.__checkpoint_identifier_to_accession, DockerAccessionMedium, 'Retrieve accessions by identifiers.')]
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

    def __checkpoint_identifier_to_accession(self,docker,*args,**kwargs):
        accessions = next(self.miner.yield_accession_by_identifier(docker, **kwargs))
        return accessions, args, kwargs

    def verify_docker(self, docker):
        """

        Parameters
        ----------
        docker :
            

        Returns
        -------

        """
        return self.miner.verify_docker(docker) and isinstance(docker, DockerIdentifierMetabase)

    @property
    def inlet(self):
        """ """
        return DockerIdentifierMedium

    @property
    def outlet(self):
        """ """
        return DockerAccessionMedium
