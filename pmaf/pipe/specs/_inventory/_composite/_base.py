from pmaf.pipe.specs._metakit import SpecificationCompositeMetabase,SpecificationBackboneMetabase
from pmaf.pipe.specs._base import SpecificationBase

class SpecificationCompositeBase(SpecificationBase,SpecificationCompositeMetabase):
    """"""
    def __init__(self, _specs,_steps):
        if not all([isinstance(spec,SpecificationBackboneMetabase) for spec in _specs]):
            raise TypeError('`_specs` contain element with invalid type.')
        tmp_factors = set([spec.factor for spec in _specs])
        if len(tmp_factors)!=1:
            raise RuntimeError('Composite specification may contain only one factor.')
        self.__specs = _specs
        self.__factor = tmp_factors.pop()
        self.__steps =_steps

    def verify_docker(self, docker):
        return self.__specs[0].verify_docker(docker)

    @property
    def specs(self):
        """List of joined and ordered :term:`specs<spec>`"""
        return self.__specs

    @property
    def state(self):
        return all([spec.state for spec in self.__specs])

    @property
    def factor(self):
        return self.__factor

    @property
    def steps(self):
        return self.__steps

