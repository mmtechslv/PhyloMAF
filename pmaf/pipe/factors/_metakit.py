from abc import ABC,abstractmethod

class FactorBackboneMetabase(ABC):
    @property
    @abstractmethod
    def factors(self):
        pass

    @property
    @abstractmethod
    def externals(self):
        pass
