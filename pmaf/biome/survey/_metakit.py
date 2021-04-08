from abc import abstractmethod
from pmaf.biome._metakit import BiomeFeatureMetabase,BiomeSampleMetabase

class BiomeSurveyBackboneMetabase(BiomeFeatureMetabase, BiomeSampleMetabase):
    @abstractmethod
    def to_assembly(self):
        pass

    @property
    @abstractmethod
    def essentials(self):
        pass

    @property
    @abstractmethod
    def assemblies(self):
        pass

    @property
    @abstractmethod
    def controller(self):
        pass

