from pmaf.pipe.factors._base import FactorBase
from pmaf.pipe.specs._metakit import SpecificationPrimitiveMetabase
from pmaf.pipe.specs._base import SpecificationBase
from pmaf.pipe.agents.miners._metakit import MinerBackboneMetabase


class SpecificationPrimitiveBase(SpecificationBase, SpecificationPrimitiveMetabase):
    """Base class for primitive :term:`specs<spec>`"""

    def __init__(self, _miner, _steps):
        if isinstance(_miner, MinerBackboneMetabase):
            if _miner.state:
                self.__miner = _miner
            else:
                raise ValueError("`_miner` has invalid state.")
        else:
            raise TypeError("`_miner` has invalid type.")
        self.__steps = _steps

    def verify_docker(self, docker):
        return self.miner.verify_docker(docker) and isinstance(docker, self.inlet)

    @property
    def miner(self) -> MinerBackboneMetabase:
        """Miner assigned to :term:`spec` instance."""
        return self.__miner

    @property
    def state(self) -> bool:
        return self.__miner.state

    @property
    def factor(self) -> FactorBase:
        return self.__miner.factor

    @property
    def steps(self) -> list:
        return self.__steps
