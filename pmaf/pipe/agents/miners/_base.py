from ._metakit import MinerBackboneMetabase
from pmaf.pipe.agents.mediators._metakit import MediatorBackboneMetabase,MediatorAccessionMetabase,MediatorTaxonomyMetabase,MediatorSequenceMetabase,MediatorPhylogenyMetabase
from pmaf.pipe.agents.dockers._metakit import DockerAccessionMetabase,DockerIdentifierMetabase,DockerPhylogenyMetabase,DockerTaxonomyMetabase,DockerSequenceMetabase,DockerBackboneMetabase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase

class MinerBase(MinerBackboneMetabase):
    ''' '''
    def __init__(self,mediator,factor,**kwargs):
        if not isinstance(mediator, MediatorBackboneMetabase):
            raise TypeError('`mediator` has invalid type.')
        if not isinstance(factor, FactorBackboneMetabase):
            raise TypeError('`factor` has invalid type.')
        self.__mediator = mediator
        self.__factor = factor

    def __repr__(self):
        class_name = self.__class__.__name__
        state = 'Active' if self.__mediator.state == 1 else 'Inactive'
        mediator  = self.__mediator.__class__.__name__
        factor = self.__factor.__class__.__name__
        repr_str = "<{}:[{}] Mediator:[{}], Factor:[{}]>".format(class_name, state, mediator,factor)
        return repr_str

    def verify_docker(self, docker):
        '''

        Args:
          docker: 

        Returns:

        '''
        if isinstance(docker,DockerBackboneMetabase):
            compatibility_tests = [isinstance(docker,DockerAccessionMetabase) and isinstance(self.__mediator,MediatorAccessionMetabase),
                                   isinstance(docker,DockerPhylogenyMetabase) and isinstance(self.__mediator,MediatorPhylogenyMetabase),
                                   isinstance(docker,DockerSequenceMetabase) and isinstance(self.__mediator,MediatorSequenceMetabase),
                                   isinstance(docker,DockerTaxonomyMetabase) and isinstance(self.__mediator,MediatorTaxonomyMetabase),
                                   isinstance(docker,DockerIdentifierMetabase)]
            return any(compatibility_tests)
        else:
            raise TypeError('`docker` has invalid type.')

    @property
    def factor(self):
        ''' '''
        return self.__factor

    @property
    def mediator(self):
        ''' '''
        return self.__mediator

    @property
    def state(self):
        ''' '''
        return self.__mediator.state

