from abc import ABC,abstractmethod

class BranchEstimatorBackboneMetabase(ABC):
    ''' '''
    @abstractmethod
    def estimate(self,multiseq,tree,**kwargs):
        '''

        Args:
          multiseq: 
          tree: 
          **kwargs: 

        Returns:

        '''
        pass