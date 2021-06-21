from abc import ABC,abstractmethod

class MarkerBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def embed_specs(self, method, input, outlet, name, description):
        """

        Parameters
        ----------
        method :
            
        input :
            
        outlet :
            
        name :
            
        description :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def next(self):
        """ """
        pass

    @abstractmethod
    def compute(self):
        """ """
        pass

    @property
    @abstractmethod
    def tasks(self):
        """ """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

    @property
    @abstractmethod
    def metadata(self):
        """ """
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
    def input(self):
        """ """
        pass

    @property
    @abstractmethod
    def output(self):
        """ """
        pass

    @property
    @abstractmethod
    def upcoming(self):
        """ """
        pass



