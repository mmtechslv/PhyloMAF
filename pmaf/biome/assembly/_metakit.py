from abc import abstractmethod
from pmaf.biome._metakit import BiomeFeatureMetabase, BiomeSampleMetabase


class BiomeAssemblyBackboneMetabase(BiomeFeatureMetabase, BiomeSampleMetabase):
    @abstractmethod
    def export(self, output_dir, *args, **kwargs):
        pass

    @abstractmethod
    def get_subset(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_essentials(self, *args):
        pass

    @abstractmethod
    def to_otu_table(self, *args, **kwargs):
        pass

    @abstractmethod
    def write_otu_table(self, output_fp, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def essentials(self):
        pass

    @property
    @abstractmethod
    def controller(self):
        pass
