from abc import ABC,abstractmethod

class MultiSequenceAlignerBackboneMetabase(ABC):
    """ """
    @abstractmethod
    def align(self,input,**kwargs):
        """

        Parameters
        ----------
        input :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def last_alignment(self):
        """ """
        pass

    @property
    @abstractmethod
    def last_std_out(self):
        """ """
        pass

    @property
    @abstractmethod
    def last_std_error(self):
        """ """
        pass

    @property
    @abstractmethod
    def aligner(self):
        """ """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

