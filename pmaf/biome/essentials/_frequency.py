import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from pmaf.biome.essentials._metakit import (
    EssentialFeatureMetabase,
    EssentialSampleMetabase,
)
from pmaf.biome.essentials._base import EssentialBackboneBase
from collections import defaultdict
from os import path
import pandas as pd
import numpy as np
import biom
from typing import Union, Sequence, Tuple, Callable, Any, Optional
from pmaf.internal._typing import AnyGenericIdentifier, Mapper


class FrequencyTable(
    EssentialBackboneBase, EssentialFeatureMetabase, EssentialSampleMetabase
):
    """An essential class for handling frequency data."""

    def __init__(
        self,
        frequency: Union[pd.DataFrame, str],
        skipcols: Union[Sequence[Union[str, int]], str, int] = None,
        allow_nan: bool = False,
        **kwargs
    ):
        """Constructor for :class:`.FrequencyTable`

        Parameters
        ----------
        frequency
            Data containing frequency data.
        skipcols
             Columns to skip when processing data.
        allow_nan
            Allow NA/NaN values or raise an error.
        kwargs
            Remaining parameters passed to :func:`~pandas.read_csv` or :mod:`biom` loader
        """
        self.__internal_frequency = None
        tmp_skipcols = np.asarray([])
        tmp_metadata = kwargs.pop("metadata", {})
        if skipcols is not None:
            if isinstance(skipcols, (str, int)):
                tmp_skipcols = np.asarray([skipcols])
            elif isinstance(skipcols, (list, tuple)):
                if not isinstance(skipcols[0], (str, int)):
                    tmp_skipcols = np.asarray(skipcols)
                else:
                    raise TypeError(
                        "`skipcols` can be int/str or list-like of int/str."
                    )
            else:
                raise TypeError("`skipcols` can be int/str or list-like of int/str.")
        if isinstance(frequency, pd.DataFrame):
            if all(frequency.shape):
                tmp_frequency = frequency
            else:
                raise ValueError("Provided `frequency` Datafame is invalid.")
        elif isinstance(frequency, str):
            if path.isfile(frequency):
                raise FileNotFoundError("Provided `frequency` file path is invalid.")
            file_extension = path.splitext(frequency)[-1].lower()
            if file_extension in [".csv", ".tsv"]:
                tmp_frequency = pd.read_csv(frequency, **kwargs)
            elif file_extension in [".biom", ".biome"]:
                tmp_frequency, new_metadata = self.__load_biom(frequency, **kwargs)
                tmp_metadata.update({"biom": new_metadata})
            else:
                raise NotImplementedError("File type is not supported.")
        else:
            raise TypeError("Provided `frequency` has invalid type.")
        if skipcols is not None:
            if np.issubdtype(tmp_skipcols.dtype, np.number):
                if tmp_frequency.columns.isin(tmp_skipcols).any():
                    tmp_frequency.drop(columns=tmp_skipcols, inplace=True)
                else:
                    tmp_frequency.drop(
                        columns=tmp_frequency.columns[tmp_skipcols], inplace=True
                    )
            else:
                tmp_frequency.drop(columns=tmp_skipcols, inplace=True)
        tmp_dtypes = list(set(tmp_frequency.dtypes.values))
        if len(tmp_dtypes) == 1 and pd.api.types.is_numeric_dtype(tmp_dtypes[0]):
            self.__init_frequency_table(tmp_frequency)
        else:
            if not allow_nan:
                raise ValueError(
                    "Provided `frequency` must have numeric dtypes. "
                    "Use `allow_nan` to allow missing values."
                )
            if len(tmp_dtypes) == 1 and pd.api.types.is_numeric_dtype(tmp_dtypes[0]):
                self.__init_frequency_table(tmp_frequency)
            elif len(tmp_dtypes) == 2:
                tmp_dtypes_cond = [
                    (dt == object) or (pd.api.types.is_numeric_dtype(dt))
                    for dt in tmp_dtypes
                ]
                if all(tmp_dtypes_cond) and tmp_frequency.isnull().values.any():
                    self.__init_frequency_table(tmp_frequency)
                else:
                    raise ValueError(
                        "Provided `frequency` may contain numeric values or NAs."
                    )
            else:
                raise ValueError("Provided `frequency` has zero or too many dtypes.")

        super().__init__(metadata=tmp_metadata, **kwargs)

    @classmethod
    def from_biom(cls, filepath: str, **kwargs) -> "FrequencyTable":
        """Factory method to construct a :class:`.FrequencyTable` from
        :mod:`biom` file.

        Parameters
        ----------
        filepath
            Path to :mod:`biom` file
        kwargs
            Compatibility

        Returns
        -------
            Instance of class:`.FrequencyTable`
        """
        frequency_frame, new_metadata = cls.__load_biom(filepath, **kwargs)
        tmp_metadata = kwargs.pop("metadata", {})
        tmp_metadata.update({"biom": new_metadata})
        return cls(frequency=frequency_frame, metadata=tmp_metadata, **kwargs)

    @classmethod
    def from_csv(cls, filepath: str, **kwargs) -> "FrequencyTable":
        """Factory method to construct a :class:`.FrequencyTable` from CSV
        file.

        Parameters
        ----------
        filepath
            Path to .csv file.
        kwargs
            Compatibility

        Returns
        -------
            Instance of class:`.FrequencyTable`
        """
        tmp_frequency = pd.read_csv(filepath, **kwargs)
        tmp_metadata = kwargs.pop("metadata", {})
        tmp_metadata.update({"filepath": path.abspath(filepath)})
        return cls(frequency=tmp_frequency, metadata=tmp_metadata, **kwargs)

    @classmethod
    def __load_biom(cls, filepath: str, **kwargs) -> Tuple[pd.DataFrame, dict]:
        """Actual private method to process :mod:`biom` file.

        Parameters
        ----------
        filepath
            :mod:`biom` file path.
        kwargs
            Compatibility
        """
        biom_file = biom.load_table(filepath)
        return biom_file.to_dataframe(dense=True), {}

    def _rename_samples_by_map(
        self, map_like: Mapper, **kwargs
    ) -> Union[None, Mapper, dict]:
        """Rename sample names by map and ratify action.

        Parameters
        ----------
        map_like
            Mapper to use for renaming
        kwargs
            Compatibility
        """
        self.__internal_frequency.rename(mapper=map_like, axis=1, inplace=True)
        return self._ratify_action("_rename_samples_by_map", map_like, **kwargs)

    def _remove_features_by_id(
        self, ids: AnyGenericIdentifier, **kwargs
    ) -> Union[None, AnyGenericIdentifier, dict]:
        """Remove feature by id and ratify action.

        Parameters
        ----------
        ids
            Feature identifiers.
        kwargs
            Compatibility
        """
        tmp_ids = np.asarray(ids, dtype=self.__internal_frequency.index.dtype)
        if len(tmp_ids) > 0:
            self.__internal_frequency.drop(index=tmp_ids, inplace=True)
        return self._ratify_action("_remove_features_by_id", ids, **kwargs)

    def _merge_features_by_map(
        self, map_dict: Mapper, aggfunc: Union[str, Callable] = "sum", **kwargs
    ) -> Union[None, Mapper]:
        """Merge features by map with aggfunc and ratify action.

        Parameters
        ----------
        map_dict
            Feature-wise map to use for merging
        aggfunc
            Aggregation function
        kwargs
            Compatibility
        """
        tmp_agg_dict = defaultdict(list)
        for new_id, group in map_dict.items():
            tmp_agg_dict[new_id] = (
                self.__internal_frequency.loc[group, :].agg(func=aggfunc, axis=0).values
            )
        tmp_freq_table = pd.DataFrame.from_dict(
            tmp_agg_dict, orient="index", columns=self.__internal_frequency.columns
        )
        self.__init_frequency_table(tmp_freq_table)
        return self._ratify_action(
            "_merge_features_by_map", map_dict, aggfunc=aggfunc, **kwargs
        )

    def _remove_samples_by_id(
        self, ids: AnyGenericIdentifier, **kwargs
    ) -> Union[None, AnyGenericIdentifier, dict]:
        """Remove samples by id and ratify action.

        Parameters
        ----------
        ids
            Feature identifiers
        kwargs
            Compatibility
        """
        tmp_ids = np.asarray(ids, dtype=self.__internal_frequency.columns.dtype)
        if len(tmp_ids) > 0:
            self.__internal_frequency.drop(columns=tmp_ids, inplace=True)
        return self._ratify_action("_remove_samples_by_id", ids, **kwargs)

    def _merge_samples_by_map(
        self, map_dict: Mapper, aggfunc: Union[str, Callable] = "mean", **kwargs
    ) -> Optional[Mapper]:

        """Merge samples by map with aggfunc and ratify action.

        Parameters
        ----------
        map_dict
            Sample-wise map to use for merging
        aggfunc
            Aggregation function
        kwargs
            Compatibility
        """
        tmp_agg_dict = defaultdict(list)
        for new_id, group in map_dict.items():
            tmp_agg_dict[new_id] = (
                self.__internal_frequency.loc[:, group]
                .agg(func=aggfunc, axis=1)
                .to_dict()
            )
        tmp_freq_table = pd.DataFrame.from_dict(tmp_agg_dict, orient="columns")
        self.__init_frequency_table(tmp_freq_table)
        return self._ratify_action(
            "_merge_samples_by_map", map_dict, aggfunc=aggfunc, **kwargs
        )

    def transform_to_relative_abundance(self):
        """Transform absolute counts to relative."""
        self.__internal_frequency = self.__internal_frequency.div(
            self.__internal_frequency.sum(axis=0), axis=1
        )

    def replace_nan_with(self, value: Any) -> None:
        """Replace NaN values with `value`.

        Parameters
        ----------
        value
            Value to replace NaN's
        """
        self.__internal_frequency.fillna(value, inplace=True)

    def drop_features_by_id(self, ids: AnyGenericIdentifier) -> Union[None, np.ndarray]:
        """Drop features by `ids`

        Parameters
        ----------
        ids
            Feature identifiers
        """
        target_ids = np.asarray(ids)
        if self.__internal_frequency.index.isin(target_ids).sum() == len(target_ids):
            self._remove_features_by_id(target_ids)
            if self.is_buckled:
                return target_ids
        else:
            raise ValueError("Invalid _feature ids are provided.")

    def rename_samples(self, mapper: Mapper) -> None:
        """Rename sample names.

        Parameters
        ----------
        mapper
            Rename samples by map
        """
        if isinstance(mapper, dict) or callable(mapper):
            if isinstance(mapper, dict):
                if self.__internal_frequency.columns.isin(
                    list(mapper.keys())
                ).sum() == len(mapper):
                    self._rename_samples_by_map(mapper)
                else:
                    raise ValueError("Invalid sample ids are provided.")
            else:
                self._rename_samples_by_map(mapper)
        else:
            raise TypeError("Invalid `mapper` type.")

    def drop_features_without_counts(self) -> Optional[np.ndarray]:
        """Drop features that has no counts.

        Typically required after dropping samples.
        """
        target_ids = self.__internal_frequency.index[
            self.__internal_frequency.sum(axis=1) == 0
        ].values
        self._remove_features_by_id(target_ids)
        if self.is_buckled:
            return target_ids

    def drop_samples_by_id(self, ids: AnyGenericIdentifier) -> Optional[np.ndarray]:
        """Drop samples by `ids`

        Parameters
        ----------
        ids
            Sample identifiers
        """
        target_ids = np.asarray(ids)
        if self.__internal_frequency.columns.isin(target_ids).sum() == len(target_ids):
            self._remove_samples_by_id(target_ids)
            if self.is_buckled:
                return target_ids
        else:
            raise ValueError("Invalid _sample ids are provided.")

    def __init_frequency_table(self, freq_table: pd.DataFrame) -> None:
        """Initiate the frequency table."""
        self.__internal_frequency = freq_table

    def merge_features_by_map(
        self, mapping: Mapper, aggfunc: Union[str, Callable] = "sum", **kwargs
    ) -> Optional[Mapper]:
        """Merge features by `mapping`

        Parameters
        ----------
        mapping
            Map with values as feature identifiers to be aggregated.
        aggfunc
            Aggregation function to apply
        kwargs
            Compatibility
        """
        if isinstance(mapping, (dict, pd.Series)):
            tmp_ids = sorted(
                {x for _, v in mapping.items() for x in v}
            )  # FIXME: Uncool behavior make it better and follow the usage.
            if self.__internal_frequency.index.isin(tmp_ids).sum() == len(tmp_ids):
                return self._merge_features_by_map(mapping, aggfunc, **kwargs)
            else:
                raise ValueError("Invalid feature ids were found.")
        else:
            raise TypeError("`mapping` can be `dict` or `pd.Series`")

    def merge_samples_by_map(
        self, mapping: Mapper, aggfunc: Union[str, Callable] = "mean", **kwargs
    ) -> Optional[Mapper]:
        """Merge samples by `mapping`

        Parameters
        ----------
        mapping
            Map with values as sample identifiers to be aggregated.
        aggfunc
            Aggregation function to apply
        kwargs
            Compatibility
        """
        if isinstance(mapping, (dict, pd.Series)):
            tmp_ids = sorted(
                {x for _, v in mapping.items() for x in v}
            )  # FIXME: Uncool. See above.
            if self.__internal_frequency.columns.isin(tmp_ids).sum() == len(tmp_ids):
                return self._merge_samples_by_map(mapping, aggfunc, **kwargs)
            else:
                raise ValueError("Invalid sample ids were found.")
        else:
            raise TypeError("`mapping` can be `dict` or `pd.Series`")

    def copy(self) -> "FrequencyTable":
        """Copy of the instance."""
        return type(self)(
            frequency=self.__internal_frequency, metadata=self.metadata, name=self.name
        )

    def get_subset(
        self,
        rids: Optional[AnyGenericIdentifier] = None,
        sids: Optional[AnyGenericIdentifier] = None,
        *args,
        **kwargs
    ) -> "FrequencyTable":
        """Get subset of the :class:`.FrequencyTable`.

        Parameters
        ----------
        rids
            Feature Identifiers
        sids
            Sample Identifiers
        args
            Compatibility
        kwargs
            Compatibility

        Returns
        -------
            Instance of class:`.FrequencyTable`.
        """
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids).astype(self.__internal_frequency.index.dtype)
        if sids is None:
            target_sids = self.xsid
        else:
            target_sids = np.asarray(sids).astype(
                self.__internal_frequency.columns.dtype
            )
        if not (
            (self.xrid.isin(target_rids).sum() == len(target_rids))
            and (self.xsid.isin(target_sids).sum() == len(target_sids))
        ):
            raise ValueError("Invalid ids are provided.")
        return type(self)(
            frequency=self.__internal_frequency.loc[target_rids, target_sids],
            metadata=self.metadata,
            name=self.name,
        )

    def _export(
        self, sortby: str = "counts", ascending: bool = True, **kwargs
    ) -> Tuple[pd.DataFrame, dict]:
        """Creates frequency table for export.

        Parameters
        ----------
        sortby
            Apply sorting on ['counts']
        ascending
            Sorting
        kwargs
            Compatibility
        """
        if sortby == "counts":
            return (
                self.data.sort_values(
                    by=self.xsid.values.tolist(), axis=0, ascending=ascending
                ),
                kwargs,
            )
        else:
            raise NotImplemented

    def export(
        self, output_fp: str, *args, _add_ext: bool = False, sep: str = ",", **kwargs
    ) -> None:  # TODO: Improve
        """Exports the sample metadata content into the specified file.

        Parameters
        ----------
        output_fp
            Export filepath.
        args
            Compatibility
        _add_ext
            Add file extension or not.
        sep
            Delimiter
        kwargs
            Compatibility
        """
        tmp_export, rkwarg = self._export(*args, **kwargs)
        if _add_ext:
            tmp_export.to_csv("{}.csv".format(output_fp), sep=sep)
        else:
            tmp_export.to_csv(output_fp, sep=sep)

    @property
    def data(self) -> pd.DataFrame:
        """Pandas dataframe of `FrequencyTable`"""
        return self.__internal_frequency

    @property
    def xrid(self) -> pd.Index:
        """Feature axis."""
        return self.__internal_frequency.index

    @property
    def xsid(self) -> pd.Index:
        """Sample axis."""
        return self.__internal_frequency.columns

    @property
    def any_nan(self) -> bool:
        """Is there nan values present?"""
        return self.__internal_frequency.isnull().any().any()
