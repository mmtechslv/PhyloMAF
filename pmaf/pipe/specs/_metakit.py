from abc import ABC, abstractmethod

class SpecificationBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def __init__(self,*args,**kwargs):
        pass

    @abstractmethod
    def verify_docker(self, docker):
        """

        Parameters
        ----------
        docker :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def fetch(self, data):
        """

        Parameters
        ----------
        data :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def inlet(self):
        """ """
        pass

    @property
    @abstractmethod
    def outlet(self):
        """ """
        pass

    @property
    @abstractmethod
    def state(self):
        """ """
        pass

    @property
    @abstractmethod
    def factor(self):
        """ """
        pass

    @property
    @abstractmethod
    def steps(self):
        """ """
        pass


class SpecificationPrimitiveMetabase(SpecificationBackboneMetabase):
    """ """
    @property
    @abstractmethod
    def miner(self):
        """ """
        pass


class SpecificationCompositeMetabase(SpecificationBackboneMetabase):
    """ """

    @property
    @abstractmethod
    def specs(self):
        """ """
        pass