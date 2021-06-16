import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from ._metakit import BiomeAssemblyBackboneMetabase
from pmaf.biome.essentials._metakit import (
    EssentialBackboneMetabase,
    EssentialSampleMetabase,
    EssentialFeatureMetabase,
)
from pmaf.biome.essentials._taxonomy import RepTaxonomy
from pmaf.biome.essentials._frequency import FrequencyTable
from pmaf.biome._base import BiomeBackboneBase
from pmaf.biome.essentials._controller import EssentialsController
import numpy as np
from functools import reduce
import pandas as pd
from os import path
from typing import Union, Sequence, Any, Optional, List
from pmaf.internal._typing import GenericIdentifier


class BiomeAssembly(BiomeBackboneBase, BiomeAssemblyBackboneMetabase):
    """Assembly class for interconnecting and containing `essentials`"""

    def __init__(
        self,
        essentials: Optional[Sequence[EssentialBackboneMetabase]] = None,
        *args: Optional[EssentialBackboneMetabase],
        curb: Union[str, EssentialBackboneMetabase, None] = None,
        copy: bool = True,
        **kwargs: Any
    ) -> None:

        """Constructor for :class:`.BiomeAssembly`

        Args:
                essentials: Single or _multiple instances of `essentials`
                *args: Instances of `essentials`
                curb: Set limiting instance of `essentials` that will be used to
                    subset remaining essentials to identical axes.
                    If set tp 'intersect' intersection will be used as limiter.
                copy: Whether to copy `essentials` or not.
                **kwargs: Compatibility.

        """
        if essentials is not None:
            if isinstance(essentials, (tuple, list)):
                tmp_essentials = essentials
            else:
                tmp_essentials = [essentials]
        else:
            tmp_essentials = []
        if len(args) > 0:
            for arg in args:
                tmp_essentials.append(arg)
        if len(tmp_essentials) == 0:
            raise ValueError("No essentials were provided.")
        target_rids = None
        target_sids = None
        if curb is not None:
            if isinstance(curb, EssentialBackboneMetabase):
                if isinstance(curb, EssentialFeatureMetabase):
                    target_rids = curb.get_feature_ids(str)
                if isinstance(curb, EssentialSampleMetabase):
                    target_sids = curb.get_sample_ids(str)
            elif curb == "intersect":
                tmp_rids_list = []
                tmp_sids_list = []
                for essential in tmp_essentials:
                    if isinstance(essential, EssentialFeatureMetabase):
                        tmp_rids_list.append(essential.get_feature_ids(str))
                    if isinstance(essential, EssentialSampleMetabase):
                        tmp_sids_list.append(essential.get_sample_ids(str))
                target_rids = (
                    reduce(np.intersect1d, tmp_rids_list)
                    if len(tmp_rids_list) > 0
                    else target_rids
                )
                target_sids = (
                    reduce(np.intersect1d, tmp_sids_list)
                    if len(tmp_sids_list) > 0
                    else target_sids
                )
            else:
                raise ValueError("`curb` is invalid.")

        essentials_adj = []
        controller = EssentialsController(**kwargs)
        for essential in tmp_essentials:
            if not controller.verify_essential(
                essential, check_axis=curb is None, check_mount=not copy
            ):
                raise ValueError(
                    "Essential {} is invalid.".format(essential.__class__.__name__)
                )
            if curb is not None:
                if isinstance(essential, EssentialFeatureMetabase) and not isinstance(
                    essential, EssentialSampleMetabase
                ):
                    essentials_adj.append(essential.get_subset(target_rids))
                elif isinstance(essential, EssentialSampleMetabase) and not isinstance(
                    essential, EssentialFeatureMetabase
                ):
                    essentials_adj.append(essential.get_subset(target_sids))
                else:
                    essentials_adj.append(
                        essential.get_subset(target_rids, target_sids)
                    )
            else:
                if copy:
                    essentials_adj.append(essential.copy())
                else:
                    essentials_adj.append(essential)

        for essential in essentials_adj:
            controller.insert_essential(essential)
        self.__controller = controller
        super().__init__(**kwargs)

    def __getattr__(self, attribute: str) -> EssentialBackboneMetabase:
        """Provides attribute lookup for installed `essentials`.

        Args:
                attribute: Class name of the `essential`.

        Returns:
                Instance of :class:`~pmaf.biome.essentials._base.EssentialBackboneBase`

        """
        for essential in self.__controller.essentials:
            if attribute == type(essential).__name__:
                return essential
        super().__getattribute__(attribute)

    def __dir__(self):
        """Provides list of installed `essential` class names for built-in :func:`dir` method()"""
        return sorted(
            dir(type(self))
            + [type(essential).__name__ for essential in self.__controller.essentials]
        )

    def _repr_appendage__(self):
        """Helper for `__repr__` method of class :class:`~pmaf.biome.BiomeBackboneBase`"""
        return {"Essentials": len(self.__controller.essentials)}

    def copy(self) -> "BiomeAssembly":
        """Copy of the instance."""
        copied_essentials = [
            essential.copy() for essential in self.__controller.essentials
        ]
        return type(self)(*copied_essentials, name=self.name, metadata=self.metadata)

    def add_essentials(
        self,
        *args: EssentialBackboneMetabase,
        curb: Optional[str] = None,
        copy: bool = True
    ) -> None:
        """Add instance of `essentials` to the current instance of :class:`.BiomeAssembly`

        Args:
                *args: Instances of `essentials` to add.
                curb: Can be either `intersect` or None.
                copy: Whether to copy essentials or not.

        """
        tmp_essentials = []
        for arg in args:
            if isinstance(arg, (list, tuple)):
                tmp_essentials.extend(arg)
            else:
                tmp_essentials.append(arg)
        tmp_essentials_adj = []
        for essential in tmp_essentials:
            if self.__controller.verify_essential(
                essential, check_axis=curb is None, check_mount=not copy
            ):
                if curb == "intersect":
                    if isinstance(
                        essential, EssentialFeatureMetabase
                    ) and not isinstance(essential, EssentialSampleMetabase):
                        tmp_essentials_adj.append(
                            essential.get_subset(self.__controller.xrid)
                        )
                    elif isinstance(
                        essential, EssentialSampleMetabase
                    ) and not isinstance(essential, EssentialFeatureMetabase):
                        tmp_essentials_adj.append(
                            essential.get_subset(self.__controller.xsid)
                        )
                    else:
                        tmp_essentials_adj.append(
                            essential.get_subset(
                                self.__controller.xrid, self.__controller.xsid
                            )
                        )
                else:
                    if copy:
                        tmp_essentials_adj.append(essential.copy())
                    else:
                        tmp_essentials_adj.append(essential)
            else:
                raise ValueError(
                    "Essential {} is invalid.".format(essential.__class__.__name__)
                )
        for essential in tmp_essentials_adj:
            self.__controller.insert_essential(essential)

    def get_subset(
        self,
        rids: Optional[GenericIdentifier] = None,
        sids: Optional[GenericIdentifier] = None,
        **kwargs
    ) -> "BiomeAssembly":
        """Get subset of the :class:`.BiomeAssembly`.

        Args:
                rids: Feature Identifiers
                sids: Sample Identifiers
                **kwargs: Compatibility

        Returns:
                Instance of :class:`.BiomeAssembly`.

        """
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids)
        if sids is None:
            target_sids = self.xsid
        else:
            target_sids = np.asarray(sids)
        if not (
            (self.xrid.isin(target_rids).sum() == len(target_rids))
            and (self.xsid.isin(target_sids).sum() == len(target_sids))
        ):
            raise ValueError("Invalid ids are provided.")
        tmp_subset_essentials = []
        for essential in self.__controller.essentials:
            if isinstance(essential, EssentialFeatureMetabase) and not isinstance(
                essential, EssentialSampleMetabase
            ):
                tmp_subset_essentials.append(essential.get_subset(target_rids))
            elif isinstance(essential, EssentialSampleMetabase) and not isinstance(
                essential, EssentialFeatureMetabase
            ):
                tmp_subset_essentials.append(essential.get_subset(target_sids))
            else:
                tmp_subset_essentials.append(
                    essential.get_subset(target_rids, target_sids)
                )
        return type(self)(
            tmp_subset_essentials, metadata=self.metadata, name=self.name, copy=False
        )

    def __make_otu_table(
        self,
        rids: Optional[GenericIdentifier] = None,
        sids: Optional[GenericIdentifier] = None,
        taxonomy_column_name: str = "Taxonomy",
        **kwargs: Any
    ) -> pd.DataFrame:
        """Create an OTU-table :class:`~pandas.DataFrame`

        Args:
                rids: Feature identifiers.
                sids: Sample identifiers
                taxonomy_column_name: Taxonomy column to create.
                **kwargs: Compatibility

        Returns:
                :class:`~pandas.DataFrame` of OTU-table

        """
        if not self.__controller.has_essential_by_types(RepTaxonomy, FrequencyTable):
            raise AttributeError(
                "`RepTaxonomy` and `FrequencyTable` were not found in assembly."
            )
        if not isinstance(taxonomy_column_name, str):
            raise TypeError("`taxonomy_column_name` must have <str> type..")
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids)
        if sids is None:
            target_sids = self.xsid
        else:
            target_sids = np.asarray(sids)
        if not (
            (self.xrid.isin(target_rids).sum() == len(target_rids))
            and (self.xsid.isin(target_sids).sum() == len(target_sids))
        ):
            raise ValueError("Invalid ids are provided.")
        tmp_freq = self.__controller.take_essential_by_type(FrequencyTable).get_subset(
            rids=target_rids, sids=target_sids, **kwargs
        )
        tmp_tax = self.__controller.take_essential_by_type(RepTaxonomy).get_subset(
            rids=target_rids, **kwargs
        )
        tmp_freq_df, _ = tmp_freq._export(**kwargs)
        tmp_freq_df[taxonomy_column_name], _ = tmp_tax._export(**kwargs)
        return tmp_freq_df

    def to_otu_table(self, *args: Any, **kwargs: Any) -> pd.DataFrame:
        """Crate an OTU-table :class:`~pandas.DataFrame`

        Args:
                *args: Compatibility.
                **kwargs: Compatibility

        Returns:
                :class:`~pandas.DataFrame` of OTU-table

        """
        return self.__make_otu_table(*args, **kwargs)[0]

    def write_otu_table(
        self, output_fp: str, *args: Any, sep: str = ",", **kwargs: Any
    ) -> None:
        """Write OTU-table to the file.

        Args:
          output_fp: Output filepath
          *args: Compatibility
          sep: Delimiter
          **kwargs: Compatibility

        """
        tmp_otu_table = self.__make_otu_table(*args, **kwargs)
        tmp_otu_table.to_csv(output_fp, sep=sep)

    def export(
        self,
        output_dir: str,
        prefix: Optional[str] = None,
        as_otu_table: bool = False,
        sep: str = ",",
        **kwargs: Any
    ) -> None:
        """Export data from assembly to the directory.

        Args:
                output_dir: Export directory path.
                prefix: Prefix for output files.
                as_otu_table: Create OTU-table from :class:`~pmaf.biome.essentials._frequency.FrequncyTable` and  :class:`~pmaf.biome.essentials._taxonomy.RepTaxonomy`
                sep: Delimiter
                **kwargs: Compatibility.

        """
        for essential in self.__controller.essentials:
            if not (
                as_otu_table and isinstance(essential, (FrequencyTable, RepTaxonomy))
            ):
                if prefix is not None:
                    tmp_output_fp = path.join(
                        output_dir, "{}.{}".format(prefix, essential.__class__.__name__)
                    )
                else:
                    tmp_output_fp = path.join(
                        output_dir, "{}".format(essential.__class__.__name__)
                    )
                essential.export(tmp_output_fp, _add_ext=True, sep=sep, **kwargs)
        if as_otu_table:
            otu_table = self.__make_otu_table(None, None, **kwargs)
            if prefix is not None:
                tmp_output_fp = path.join(
                    output_dir, "{}.{}.csv".format(prefix, "OtuTable")
                )
            else:
                tmp_output_fp = path.join(output_dir, "{}.csv".format("OtuTable"))
            otu_table.to_csv(tmp_output_fp, sep=sep)

    @property
    def essentials(self) -> List[EssentialBackboneMetabase]:
        """List of `essentials`"""
        return self.__controller.essentials

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
        """:class:`~pmaf.biome.essentials._controller.EssentialsController` of `essentials`"""
        return self.__controller
