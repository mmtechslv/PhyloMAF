from abc import ABC,abstractmethod

class FileIOBackboneMetabase(ABC):
    @abstractmethod
    def __init__(self, filepath, **kwargs):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def src(self):
        pass