import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
from pmaf.classifier.dhnb._metakit import DhnbClassifierDatasetMetabase

class ClassifierDataset(EssentialBackboneBase, EssentialFeatureMetabase):
    def __init__(self,dataset,**kwargs):
        super().__init__(**kwargs)
        if isinstance(dataset, ClassifierDatasetMetabase):
            self.__dataset = dataset
        else:
            raise TypeError('`dataset` has unsupported type.')

    def _remove_features_by_id(self, ids, **kwargs):
        pass

    def _merge_features_by_map(self, map_dict, done=False, **kwargs):
        pass

    def copy(self):
        return type(self)(dataset=self.__dataset, metadata = self.metadata)

    def get_subset(self, ids=None, *args, **kwargs):
        pass

    def _export(self, *args,  **kwargs):
        pass

    def export(self, *args,  **kwargs):
        pass


    @property
    def data(self):
        return self.__dataset

    @property
    def xrid(self):
        return self.__dataset.xrid