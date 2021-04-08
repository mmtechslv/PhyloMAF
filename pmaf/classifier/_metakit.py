from abc import ABC,abstractmethod

class ClassifierBackboneMetabase(ABC):
    @property
    @abstractmethod
    def state(self):
        pass

    @abstractmethod
    def classify(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def database(self):
        pass




