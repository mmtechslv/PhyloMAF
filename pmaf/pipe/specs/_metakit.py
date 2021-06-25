from abc import ABC, abstractmethod
from pmaf.pipe.agents.dockers._base import DockerBase


class SpecificationBackboneMetabase(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def verify_docker(self, docker: DockerBase) -> bool:
        """Verifies/validates the compatibility of the :term:`docker` with
        current :term:`spec`

        Parameters
        ----------
        docker
            Docker to verify

        Returns
        -------
            True of compatible :term:`docker` or False if not.
        """
        pass

    @abstractmethod
    def fetch(self, data):
        pass

    @property
    @abstractmethod
    def inlet(self):
        pass

    @property
    @abstractmethod
    def outlet(self):
        pass

    @property
    @abstractmethod
    def state(self):
        """State of the :term:`spec`"""
        pass

    @property
    @abstractmethod
    def factor(self):
        """Assigned :mod:`Factor<pmaf.pipe.factors>`"""
        pass

    @property
    @abstractmethod
    def steps(self):
        """Pipeline steps that specify current :term:`spec`"""
        pass


class SpecificationPrimitiveMetabase(SpecificationBackboneMetabase):
    @property
    @abstractmethod
    def miner(self):
        pass


class SpecificationCompositeMetabase(SpecificationBackboneMetabase):
    @property
    @abstractmethod
    def specs(self):
        pass
