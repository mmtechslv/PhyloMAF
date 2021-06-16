import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from ._metakit import BiomeSurveyBackboneMetabase
from pmaf.biome.essentials._metakit import EssentialBackboneMetabase
from pmaf.biome.essentials._frequency import FrequencyTable
from pmaf.biome.essentials._samplemeta import SampleMetadata
from pmaf.biome.essentials._taxonomy import RepTaxonomy
from pmaf.biome.assembly._assembly import BiomeAssembly
from pmaf.biome._base import BiomeBackboneBase
from pmaf.biome.essentials._controller import EssentialsController
from collections import defaultdict
from ._shared import (
    mergeRepTaxonmy,
    mergeFrequencyTable,
    mergeSampleMetadata,
    parse_assembly_maps,
)
import numpy as np
import pandas as pd
from typing import Union, Sequence, Any, Optional, Tuple, List, Dict
from pmaf.internal._typing import GenericIdentifier, AggFunc


class BiomeSurvey(BiomeBackboneBase, BiomeSurveyBackboneMetabase):
    """Assembly-like Survey class for merging instances of :class:`~pmaf.biome.assembly._assembly.BiomeAssembly`"""

    _SUPPORTED_ESSENTIALS = (RepTaxonomy, FrequencyTable, SampleMetadata)

    def __init__(
        self,
        assembiles: Optional[Sequence[BiomeAssembly]] = None,
        *args: Any,
        aggfunc: Union[
            AggFunc,
            Tuple[AggFunc, AggFunc],
            Dict[
                Union[str, int],
                Union[AggFunc, Dict[Union[EssentialBackboneMetabase, None], AggFunc]],
            ],
        ] = "mean",
        groupby: Union[str, Tuple[str, str], Dict[Union[int, str], str]] = "label",
        **kwargs: Any
    ):
        """This class performs merging/pooling of _multiple independent studies
        or instances of :class:`~pmaf.biome.essentials.EssentialBackboneBase` (essentials) into single
        instance of :class:`~pmaf.biome.survey._assembly.BiomeAssembly` -like class :class:`~pmaf.biome.survey._survey.BiomeSurvey`.

        Args:
            assembiles: *essentials* to pool.
            *args: Unpacked *essentials* to pool. (Convenience)
            aggfunc: Aggregation method. Parameter take _multiple variations of
                aggregation approach. If `str` or `Callable` then `aggfunc` will be
                applied to both axes(feature and sample) and any *essentials*
                regardless of its type. To apply aggregation for each axis separately
                use `tuple` (for example,  *aggfunc=('sum', 'mean'))* where first
                aggregation method refers to feature axis and second to sample axis.
                To apply more complex aggregation use Dict type, where keys refer to axis
                like *0/feature* for feature axis or *1/sample* for sample axis. Values
                of the dictionary can refer to two approaches. First is when values are
                simply `str` or `Callable`, which is similar to using `tuple`. Second,
                is when using values with type `Dict` where dictionary values are
                `str` or `Callable` refer to aggregating function and keys are types or
                class of *essentials* (must have base abstract class :class:`~pmaf.biome.essentials._metakit.EssentialBackboneMetabase` ).
                Using this method each type of *essential* will be processed differently
                among instances of *assemblies*. Lastly, when using approach like
                Dict[axis, Dict[*essential-type*,*agg-func*]] using `None` for one of
                *essential-type* keys will assume that it refers to all *remaining-types*.
            groupby: Grouping method. Parameters take _multiple variations
                similar to `aggfunc`. Variations are same as `aggfunc` with exception
                that values can be either `label` for both feature-axis or sample-axis
                like *groupby='label'* or *groupby=(`label`, `label`)* , or *taxonomy*
                for feature-axis only. Grouping by *taxonomy* will merge features with
                same consensus lineage.
            **kwargs: Compatibility
        """
        if kwargs.get("_copyself", None) is not None:
            copy_data = kwargs.pop("_copyself")
            tmp_assembiles = copy_data["_assemblies"]
            new_essentials = copy_data["_essentials"]
            new_metadata = {}
        else:
            if assembiles is not None:
                if isinstance(assembiles, (tuple, list)):
                    tmp_assembiles = assembiles
                else:
                    tmp_assembiles = [assembiles]
            else:
                tmp_assembiles = []
            if len(args) > 0:
                for arg in args:
                    tmp_assembiles.append(arg)
            if len(tmp_assembiles) == 0:
                raise ValueError("No assemblies were provided.")

            if isinstance(aggfunc, str):
                tmp_aggfuncs = {
                    essential_type: {0: aggfunc, 1: aggfunc}
                    for essential_type in self._SUPPORTED_ESSENTIALS
                }
            elif isinstance(aggfunc, tuple):
                if len(aggfunc) != 2:
                    raise ValueError("`aggfunc` when tuple must have length of 2.")
                tmp_aggfuncs = {
                    essential_type: {0: aggfunc[0], 1: aggfunc[1]}
                    for essential_type in self._SUPPORTED_ESSENTIALS
                }
            elif isinstance(aggfunc, dict):
                if not (
                    sum([k in [0, "feature"] for k in aggfunc.keys()]) == 1
                    and sum([k in [1, "sample"] for k in aggfunc.keys()]) == 1
                ):
                    raise ValueError(
                        "When `aggfunc` have type Dict then it's keys must can be "
                        "either feature/0 or sample/1."
                    )
                # Following two lines provide valid feature key aka. fkey and
                # valid sample key aka. skey to access correct Dict values of `aggfunc`
                fkey = 0 if 0 in aggfunc.keys() else "feature"
                skey = 1 if 1 in aggfunc.keys() else "sample"
                if all([isinstance(v, str) or callable(v) for v in aggfunc.values()]):
                    tmp_aggfuncs = {
                        essential_type: {0: aggfunc[fkey], 1: aggfunc[skey]}
                        for essential_type in self._SUPPORTED_ESSENTIALS
                    }
                elif all(
                    [
                        issubclass(k, EssentialBackboneMetabase)
                        for edict in aggfunc.values()
                        for k in edict.keys()
                        if k is not None
                    ]
                ):
                    tmp_aggfuncs = defaultdict(dict)
                    if None not in aggfunc[fkey].keys():
                        raise ValueError(
                            "`aggfunc` must contain None key in <feature> values."
                        )
                    for essential_type in self._SUPPORTED_ESSENTIALS:
                        tmp_aggfuncs[essential_type].update({0: aggfunc[fkey][None]})
                    if None not in aggfunc[skey].keys():
                        raise ValueError(
                            "`aggfunc` must contain None key in <sample> values."
                        )
                    for essential_type in self._SUPPORTED_ESSENTIALS:
                        tmp_aggfuncs[essential_type].update({1: aggfunc[skey][None]})
                    for essential_type, func in aggfunc[fkey].items():
                        if essential_type is not None:
                            tmp_aggfuncs[essential_type].update({0: func})
                    for essential_type, func in aggfunc[skey].items():
                        if essential_type is not None:
                            tmp_aggfuncs[essential_type].update({1: func})
                    if not all(
                        [
                            isinstance(func, str) or callable(func)
                            for fdict in tmp_aggfuncs.values()
                            for func in fdict.values()
                        ]
                    ):
                        raise ValueError(
                            "`aggfunc` when dict must have values either "
                            "callables/func-names or dicts with keys as essential types "
                            "and value as callables or func-names"
                        )
                else:
                    raise ValueError(
                        "`aggfunc` when dict must have values either "
                        "callables/func-names or dicts with keys as essential types "
                        "and value as callables or func-names"
                    )
            else:
                raise TypeError("`aggfunc` has invalid type.")
            if isinstance(groupby, str):
                feature_groupby = groupby
                sample_groupby = groupby
            elif isinstance(groupby, tuple):
                if len(groupby) != 2:
                    raise ValueError("`groupby` when tuple must have length of 2.")
                feature_groupby = groupby[0]
                sample_groupby = groupby[1]
            elif isinstance(groupby, dict):
                if not (
                    sum([k in [0, "feature"] for k in groupby.keys()]) == 1
                    and sum([k in [1, "sample"] for k in groupby.keys()]) == 1
                ):
                    raise ValueError(
                        "`groupby` when dict must feature or 0 and sample or 1"
                    )
                feature_groupby = groupby[0 if 0 in groupby.keys() else "feature"]
                sample_groupby = groupby[1 if 1 in groupby.keys() else "sample"]
            else:
                raise TypeError("`groupby` has invalid type.")

            if feature_groupby == "taxonomy" and sample_groupby in ["index", "label"]:
                must_have_essentials = (RepTaxonomy,)
            else:
                must_have_essentials = (object,)

            ## APPROVE VALID ESSENTIALS AND MAKE ASSEMBLY MAP

            assembly_map = defaultdict(None)
            for label, asmbly in enumerate(tmp_assembiles):
                if not all(
                    [
                        any(
                            [
                                isinstance(essential, must_type)
                                for essential in asmbly.essentials
                            ]
                        )
                        for must_type in must_have_essentials
                    ]
                ):
                    raise ValueError(
                        "Assembly {} does not satisfy merging requirements."
                    )
                assembly_map[label] = asmbly

            ## Parse Assemblies and distribute into groups with indices
            features_map, samples_map = parse_assembly_maps(
                feature_groupby, sample_groupby, assembly_map
            )
            ## TRANSFORM MAKE ASSEMBLY MAP TO ESSENTIAL MAP

            essentials_map = defaultdict(dict)
            for label, asmbly in assembly_map.items():
                for essential in asmbly.essentials:
                    if isinstance(essential, self._SUPPORTED_ESSENTIALS):
                        essentials_map[type(essential)].update({label: essential})

            essentials_map = dict(essentials_map)
            new_essentials = []
            if RepTaxonomy in essentials_map.keys():
                new_essentials.append(
                    mergeRepTaxonmy(
                        feature_groupby, features_map, essentials_map, tmp_aggfuncs
                    )
                )
            if FrequencyTable in essentials_map.keys():
                new_essentials.append(
                    mergeFrequencyTable(
                        feature_groupby,
                        sample_groupby,
                        features_map,
                        samples_map,
                        essentials_map,
                        tmp_aggfuncs,
                    )
                )
            if SampleMetadata in essentials_map.keys():
                new_essentials.append(
                    mergeSampleMetadata(
                        sample_groupby, samples_map, essentials_map, tmp_aggfuncs
                    )
                )

            new_metadata = {
                "groupby": {
                    "feature": feature_groupby,
                    "sample": sample_groupby,
                    "agg": {"aggfunc": aggfunc, "aggmap": tmp_aggfuncs},
                }
            }
        tmp_controller = EssentialsController(**kwargs)
        for essential in new_essentials:
            tmp_controller.insert_essential(essential)

        self.__assembiles = tmp_assembiles
        self.__controller = tmp_controller
        tmp_metadata = {**kwargs.pop("metadata", {}), **new_metadata}
        super().__init__(metadata=tmp_metadata, **kwargs)

    def __getattr__(self, attribute: str) -> EssentialBackboneMetabase:
        """Provides attribute lookup for installed *essentials*.

        Args:
            attribute: Class name of the *essential*.

        Returns:
            Instance of :class:`~pmaf.biome.essentials._base.EssentialBackboneBase`

        """
        for essential in self.__controller.essentials:
            if attribute == type(essential).__name__:
                return essential
        super().__getattribute__(attribute)

    def __dir__(self):
        """Provides list of installed *essential* class names for built-in :func:`dir` method()"""
        return sorted(
            dir(type(self))
            + [type(essential).__name__ for essential in self.__controller.essentials]
        )

    def _repr_appendage__(self):
        """Helper for `__repr__` method of class :class:`~pmaf.biome.BiomeBackboneBase`"""
        return {}

    def copy(self) -> "BiomeSurvey":
        """Copy of the instance."""
        copied_essentials = [
            essential.copy() for essential in self.__controller.essentials
        ]
        refs_assemblies = self.__assembiles
        return type(self)(
            _copyself={
                "_assemblies": refs_assemblies,
                "_essentials": copied_essentials,
            },
            name=self.name,
            metadata=self.metadata,
        )

    def to_assembly(self) -> BiomeAssembly:
        """Converts to the :class:`~pmaf.biome.assembly._assembly.BiomeAssembly` instance."""
        return BiomeAssembly(
            self.__controller.essentials,
            copy=True,
            name=self.name,
            metadata=self.metadata,
        )

    @property
    def essentials(self) -> List[EssentialBackboneMetabase]:
        """List of *essentials*"""
        return self.__controller.essentials

    @property
    def assemblies(self) -> Tuple[BiomeAssembly]:
        """Tuple of surveyed assemblies"""
        return tuple(self.__assembiles)

    @property
    def xrid(self) -> GenericIdentifier:
        """Feature identifiers"""
        return pd.Index(
            self.__controller.xrid
            if self.__controller.xrid is not None
            else np.array([], dtype=object)
        )

    @property
    def xsid(self) -> GenericIdentifier:
        """Sample identifiers"""
        return pd.Index(
            self.__controller.xsid
            if self.__controller.xsid is not None
            else np.array([], dtype=object)
        )

    @property
    def controller(self) -> EssentialsController:
        """:class:`~pmaf.biome.essentials._controller.EssentialsController` of *essentials*"""
        return self.__controller
