import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from ._metakit import BiomeSurveyBackboneMetabase
from pmaf.biome.essentials._metakit import EssentialBackboneMetabase
from pmaf.biome.essentials._composite._frequency import FrequencyTable
from pmaf.biome.essentials._sample._samplemeta import SampleMetadata
from pmaf.biome.essentials._feature._taxonomy import RepTaxonomy
from pmaf.biome.assembly._assembly import BiomeAssembly
from pmaf.biome._base import BiomeBackboneBase
from pmaf.biome.essentials._controller import EssentialsController
from collections import defaultdict
from ._shared import mergeRepTaxonmy,mergeFrequencyTable,mergeSampleMetadata,parse_assembly_maps
import numpy as np
import pandas as pd

class BiomeSurvey(BiomeBackboneBase, BiomeSurveyBackboneMetabase):
    VALID_ESSENTIALS = (RepTaxonomy, FrequencyTable, SampleMetadata)
    def __init__(self, assembiles=None, *args, aggfunc='mean', groupby = 'label', **kwargs):
        if kwargs.get('_copyself',None) is not None:
            copy_data = kwargs.pop('_copyself')
            tmp_assembiles = copy_data['_assemblies']
            new_essentials = copy_data['_essentials']
            new_metadata = {}
        else:
            if assembiles is not None:
                if isinstance(assembiles,(tuple,list)):
                    tmp_assembiles = assembiles
                else:
                    tmp_assembiles = [assembiles]
            else:
                tmp_assembiles = []
            if len(args)>0:
                for arg in args:
                    tmp_assembiles.append(arg)
            if len(tmp_assembiles)==0:
                raise ValueError('No assemblies were provided.')

            if isinstance(aggfunc, str):
                tmp_aggfuncs = {essential_type: {0: aggfunc, 1: aggfunc} for essential_type in self.VALID_ESSENTIALS}
            elif isinstance(aggfunc, tuple):
                if len(aggfunc) == 2:
                    tmp_aggfuncs = {essential_type: {0: aggfunc[0], 1: aggfunc[1]} for essential_type in self.VALID_ESSENTIALS}
                else:
                    raise ValueError('`aggfunc` when tuple must have length of 2.')
            elif isinstance(aggfunc, dict):
                if (sum([k in [0, 'feature'] for k in aggfunc.keys()]) == 1 and sum([k in [1, 'sample'] for k in aggfunc.keys()]) == 1):
                    fkey = 0 if 0 in aggfunc.keys() else 'feature'
                    skey = 1 if 1 in aggfunc.keys() else 'sample'
                    if all([isinstance(v, str) or callable(v) for v in aggfunc.values()]):
                        tmp_aggfuncs = {essential_type: {0: aggfunc[fkey], 1: aggfunc[skey]} for essential_type in self.VALID_ESSENTIALS}
                    elif all([issubclass(k, EssentialBackboneMetabase) for edict in aggfunc.values() for k in edict.keys() if k is not None]):
                        tmp_aggfuncs = defaultdict(dict)
                        if None in aggfunc[fkey].keys():
                            for essential_type in self.VALID_ESSENTIALS:
                                tmp_aggfuncs[essential_type].update({0: aggfunc[fkey][None]})
                        else:
                            raise ValueError('`aggfunc` must contain None key in <feature> values.')
                        if None in aggfunc[skey].keys():
                            for essential_type in self.VALID_ESSENTIALS:
                                tmp_aggfuncs[essential_type].update({1: aggfunc[skey][None]})
                        else:
                            raise ValueError('`aggfunc` must contain None key in <sample> values.')
                        for essential_type, func in aggfunc[fkey].items():
                            if essential_type is not None:
                                tmp_aggfuncs[essential_type].update({0: func})
                        for essential_type, func in aggfunc[skey].items():
                            if essential_type is not None:
                                tmp_aggfuncs[essential_type].update({1: func})
                        if not all([isinstance(func, str) or callable(func) for fdict in tmp_aggfuncs.values() for func in fdict.values()]):
                            raise ValueError('`aggfunc` when dict must have values either callables/func-names or dicts with keys as essential types and value as callables or func-names')
                    else:
                        raise ValueError('`aggfunc` when dict must have values either callables/func-names or dicts with keys as essential types and value as callables or func-names')
                else:
                    raise ValueError('`aggfunc` when dict must feature or 0 and sample or 1')
            else:
                raise TypeError('`aggfunc` has invalid type.')

            if isinstance(groupby, str):
                feature_groupby = groupby
                sample_groupby = groupby
            elif isinstance(groupby, tuple):
                if len(groupby) == 2:
                    feature_groupby = groupby[0]
                    sample_groupby = groupby[1]
                else:
                    raise ValueError('`groupby` when tuple must have length of 2.')
            elif isinstance(groupby, dict):
                if (sum([k in [0, 'fegroupby'] for k in groupby.keys()]) == 1 and sum([k in [1, 'sample'] for k in groupby.keys()]) == 1):
                    feature_groupby = groupby[0 if 0 in groupby.keys() else 'feature']
                    sample_groupby = groupby[1 if 1 in groupby.keys() else 'sample']
                else:
                    raise ValueError('`groupby` when dict must feature or 0 and sample or 1')
            else:
                raise TypeError('`groupby` has invalid type.')

            if feature_groupby == 'taxonomy' and sample_groupby in ['index','label']:
                must_have_essentials = (RepTaxonomy,)
            else:
                must_have_essentials = (object,)

            ## APPROVE VALID ESSENTIALS AND MAKE ASSEMBLY MAP

            assembly_map = defaultdict(None)
            for label, asmbly in enumerate(tmp_assembiles):
                if all([any([isinstance(essential, must_type) for essential in asmbly.essentials]) for must_type in must_have_essentials]):
                    assembly_map[label] = asmbly
                else:
                    raise ValueError('Assembly {} does not satisfy merging requirements.')

            ## Parse Assemblies and distribute into groups with indices
            features_map, samples_map = parse_assembly_maps(feature_groupby,sample_groupby,assembly_map)
            ## TRANSFORM MAKE ASSEMBLY MAP TO ESSENTIAL MAP

            essentials_map = defaultdict(dict)
            for label, asmbly in assembly_map.items():
                for essential in asmbly.essentials:
                    if isinstance(essential, self.VALID_ESSENTIALS):
                        essentials_map[type(essential)].update({label: essential})

            essentials_map = dict(essentials_map)
            new_essentials = []
            if RepTaxonomy in essentials_map.keys():
                new_essentials.append(mergeRepTaxonmy(feature_groupby,features_map,essentials_map,tmp_aggfuncs))
            if FrequencyTable in essentials_map.keys():
                new_essentials.append(mergeFrequencyTable(feature_groupby, sample_groupby, features_map, samples_map, essentials_map,tmp_aggfuncs))
            if SampleMetadata in essentials_map.keys():
                new_essentials.append(mergeSampleMetadata(sample_groupby,samples_map,essentials_map,tmp_aggfuncs))

            new_metadata = {'groupby':{'feature':feature_groupby,'sample':sample_groupby,'agg':{'aggfunc':aggfunc,'aggmap':tmp_aggfuncs}}}
        tmp_controller = EssentialsController(**kwargs)
        for essential in new_essentials:
            tmp_controller.insert_essential(essential)

        self.__assembiles = tmp_assembiles
        self.__controller = tmp_controller
        tmp_metadata = {**kwargs.pop('metadata',{}),**new_metadata}
        super().__init__(metadata=tmp_metadata,**kwargs)


    def __getattr__(self, attribute):
        for essential in self.__controller.essentials:
            if attribute == type(essential).__name__:
                return essential
        super().__getattribute__(attribute)

    def __dir__(self):
        return sorted(dir(type(self)) + [type(essential).__name__ for essential in self.__controller.essentials])

    def _repr_appendage__(self):
        return {}

    def copy(self):
        copied_essentials = [essential.copy() for essential in  self.__controller.essentials]
        refs_assemblies = self.__assembiles
        return type(self)(_copyself={'_assemblies':refs_assemblies,'_essentials':copied_essentials},name=self.name,metadata=self.metadata)

    def to_assembly(self):
        return BiomeAssembly(self.__controller.essentials, copy=True, name=self.name, metadata=self.metadata)

    @property
    def essentials(self):
        return self.__controller.essentials

    @property
    def assemblies(self):
        return self.__assembiles

    @property
    def xrid(self):
        return pd.Index(self.__controller.xrid if self.__controller.xrid is not None else np.array([],dtype=object))

    @property
    def xsid(self):
        return pd.Index(self.__controller.xsid if self.__controller.xsid is not None else np.array([],dtype=object))

    @property
    def controller(self):
        return self.__controller




