from pmaf.pipe.specs._metakit import SpecificationPrimitiveMetabase
from pmaf.pipe.specs._base import SpecificationBase
from pmaf.pipe.agents.miners._metakit import MinerBackboneMetabase

class SpecificationPrimitiveBase(SpecificationBase, SpecificationPrimitiveMetabase):
    def __init__(self,_miner, _steps):
        if isinstance(_miner,MinerBackboneMetabase):
            if _miner.state:
                self.__miner = _miner
            else:
                raise ValueError('`_miner` has invalid state.')
        else:
            raise TypeError('`_miner` has invalid type.')
        self.__steps = _steps

    @property
    def miner(self):
        return self.__miner

    @property
    def state(self):
        return self.__miner.state

    @property
    def factor(self):
        return self.__miner.factor

    @property
    def steps(self):
        return self.__steps