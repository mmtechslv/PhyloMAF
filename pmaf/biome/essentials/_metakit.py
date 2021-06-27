from abc import ABC, abstractmethod
from pmaf.biome._metakit import (
    BiomeBackboneMetabase,
    BiomeFeatureMetabase,
    BiomeSampleMetabase,
)


class EssentialBackboneMetabase(BiomeBackboneMetabase):
    def _repr_appendage__(self):
        return {}

    @abstractmethod
    def export(self, output_fp, *args, **kwargs):
        pass

    @abstractmethod
    def get_subset(self, *args, **kwargs):
        pass

    @abstractmethod
    def _buckle(self):
        pass

    @abstractmethod
    def _unbuckle(self):
        pass

    @abstractmethod
    def _mount_controller(self, controller):
        pass

    @abstractmethod
    def _ratify_action(self, method, value, **kwargs):
        pass

    @property
    @abstractmethod
    def is_mounted(self):
        pass

    @property
    @abstractmethod
    def controller(self):
        pass

    @property
    @abstractmethod
    def is_buckled(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass


class EssentialFeatureMetabase(BiomeFeatureMetabase, EssentialBackboneMetabase):
    @abstractmethod
    def _remove_features_by_id(self, ids, **kwargs):
        pass

    @abstractmethod
    def _merge_features_by_map(self, map_dict, **kwargs):
        pass


class EssentialSampleMetabase(BiomeSampleMetabase, EssentialBackboneMetabase):
    @abstractmethod
    def _remove_samples_by_id(self, ids, **kwargs):
        pass

    @abstractmethod
    def _merge_samples_by_map(self, map_dict, **kwargs):
        pass


class EssentialControllerBackboneMetabse(ABC):
    @abstractmethod
    def insert_essential(self, essential):
        pass

    @abstractmethod
    def verify_essential(self, essential):
        pass

    @abstractmethod
    def reflect_action(self, source, method, value, **kwargs):
        pass

    @property
    @abstractmethod
    def essentials(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @property
    @abstractmethod
    def count(self):
        pass

    @property
    @abstractmethod
    def xrid(self):
        pass

    @property
    @abstractmethod
    def xsid(self):
        pass
