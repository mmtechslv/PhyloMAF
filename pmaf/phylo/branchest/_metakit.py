from abc import ABC,abstractmethod

class BranchEstimatorBackboneMetabase(ABC):
    """ """
    @abstractmethod
    def estimate(self,multiseq,tree,**kwargs):
        """

        Parameters
        ----------
        multiseq :
            
        tree :
            
        **kwargs :
            

        Returns
        -------

        """
        pass