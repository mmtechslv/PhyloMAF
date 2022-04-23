from abc import ABC, abstractmethod


class TreeBuilderBackboneMetabase(ABC):
    @abstractmethod
    def build(self, multiseq, **kwargs):
        pass
