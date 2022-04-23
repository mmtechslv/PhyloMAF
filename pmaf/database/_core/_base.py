import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from pmaf.database._metakit import DatabaseBackboneMetabase
from pmaf.database._manager import DatabaseStorageManager
from pmaf.internal._shared import get_rank_upto, sort_ranks
from pmaf.database._shared._common import to_mode
import numpy as np
import pandas as pd
from collections import defaultdict
from functools import reduce
from pmaf.internal._typing import AnyGenericIdentifier
from typing import Optional, Union, Tuple, Generator, Sequence, Any


class DatabaseBase(DatabaseBackboneMetabase):
    """Base database class that provides minimum functionality."""

    def __init__(self, storage_hdf5_fp: str):
        """

        Parameters
        ----------
        storage_hdf5_fp
            File path to :term:`hdf5`

        """
        self.__storage_manager = DatabaseStorageManager(storage_hdf5_fp, self.name)
        if self.__storage_manager.state != 1:
            raise ValueError("Invalid local storage file provided.")
        self.__avail_ranks = self.__storage_manager.summary["avail-ranks"].split("|")
        tmp_tid_stats = self.__storage_manager.retrieve_data_by_element("stat-taxs")
        self.__novel_tids = tmp_tid_stats[tmp_tid_stats["novel"] == True].index.values

    def __repr__(self):
        class_name = self.__class__.__name__
        if self.__storage_manager.state:
            state = "Ready" if self.__storage_manager.state == 1 else "Incomplete"
            ranks = "".join(self.__avail_ranks)
            total_taxa = self.__storage_manager.summary["total-taxa"]
            tax_state = (
                "+" if self.__storage_manager.element_state["taxonomy-sheet"] else "-"
            )
            tree_state = (
                "+" if self.__storage_manager.element_state["tree-object"] else "-"
            )
            seq_state = "".join(
                [
                    "+" if state_elem else "-"
                    for state_elem in [
                        self.__storage_manager.element_state["sequence-representative"],
                        self.__storage_manager.element_state["sequence-aligned"],
                        self.__storage_manager.element_state["sequence-accession"],
                    ]
                ]
            )
            repr_str = "<{}:[{}], Taxa: [{}], Ranks: [{}], Taxonomy/Sequence/Tree: [{}/{}/{}]>".format(
                class_name, state, total_taxa, ranks, tax_state, seq_state, tree_state
            )
        else:
            repr_str = "<{}:[Closed]>".format(class_name)
        return repr_str

    def take_tids_by_rank(
        self,
        levels: Union[str, Sequence[str], None] = None,
        iterator: bool = False,
        flatten: bool = False,
        mode: str = "dict",
    ) -> Any:
        """Get :term:`tids` for given taxonomic ranks (`level`)

        Parameters
        ----------
        levels
            Taxonomic ranks for which to retrieve :term:`tids`.
        iterator
            Whether to data in chunks as iterator.
        flatten
            Whether to flatten :term:`tids` for all ranks instead of returning Dict[rank, :term:`tids`]
        mode
            Retrieve data as 'array', 'frame' or 'dict'(default)

        Returns
        -------
            Return :term:`tids` with type depending on input parameters.
        """
        if self.storage_manager.state != 1:
            raise RuntimeError("Storage is closed.")
        if levels is None:
            target_rank_levels = np.asarray(self.avail_ranks)
        elif isinstance(levels, str):
            target_rank_levels = np.asarray([levels])
        else:
            target_rank_levels = np.asarray(levels)
        if not all([rank in self.avail_ranks for rank in target_rank_levels]):
            raise ValueError("`rank_levels` contain invalid ranks.")
        map2tid = self.storage_manager.retrieve_data_by_element("map-rep2tid")

        def map_generator():
            for rank in target_rank_levels:
                tids = map2tid.loc[:, rank].drop_duplicates()
                yield rank, tids[tids > 0].values

        tmp_map_gen = map_generator()
        if not iterator:
            if len(target_rank_levels) > 1:
                per_rank_tid_map = defaultdict(dict)
                for rank, tids in tmp_map_gen:
                    per_rank_tid_map[rank] = tids
                if not flatten:
                    return to_mode(per_rank_tid_map, mode, target_rank_levels)
                else:
                    per_rank_rid_flat = reduce(np.union1d, per_rank_tid_map.values())
                    return to_mode(per_rank_rid_flat, "array", None)
            else:
                _, rids = next(tmp_map_gen)
                return to_mode(rids, mode, None)
        else:
            return tmp_map_gen

    def take_rids_by_rank(
        self,
        levels: Union[str, Sequence[str], None] = None,
        iterator: bool = False,
        flatten: bool = False,
        mode: str = "dict",
    ) -> Any:
        """Get :term:`rids` for given taxonomic ranks (`level`)

        Parameters
        ----------
        levels
            Taxonomic ranks for which to retrieve :term:`rids`.
        iterator
            Whether to return data in chunks as iterator.
        flatten
            Whether to flatten :term:`rids` for all ranks instead of returning Dict[rank, :term:`rids`]
        mode
            Retrieve data as 'array', 'frame' or 'dict'(default)


        Returns
        -------
            Return :term:`rids` with type depending on input parameters.
        """
        if self.storage_manager.state != 1:
            raise RuntimeError("Storage is closed.")
        if levels is None:
            target_rank_levels = np.asarray(self.avail_ranks)
        elif isinstance(levels, str):
            target_rank_levels = np.asarray([levels])
        else:
            target_rank_levels = np.asarray(levels)
        if not all([rank in self.avail_ranks for rank in target_rank_levels]):
            raise ValueError("`rank_levels` contain invalid ranks.")

        map2tid = self.storage_manager.retrieve_data_by_element("map-rep2tid")

        def map_generator():
            """"""
            tmp_reps = set()
            for rank in target_rank_levels:
                groupby = map2tid.groupby(rank)
                for tid, rids in groupby.groups.items():
                    if tid != 0:
                        tmp_reps.update(np.unique(rids.values))
                yield rank, np.asarray(list(tmp_reps))

        tmp_map_gen = map_generator()
        if not iterator:
            if len(target_rank_levels) > 1:
                per_rank_rid_map = defaultdict(dict)
                for rank, rids in tmp_map_gen:
                    per_rank_rid_map[rank] = rids
                if not flatten:
                    return to_mode(per_rank_rid_map, mode, target_rank_levels)
                else:
                    per_rank_rid_flat = reduce(np.union1d, per_rank_rid_map.values())
                    return to_mode(per_rank_rid_flat, "array", None)
            else:
                _, rids = next(tmp_map_gen)
                return to_mode(rids, mode, None)
        else:
            return tmp_map_gen

    def find_sub_tids_by_tid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        ter_rank: Optional[str] = None,
        flatten: bool = False,
        mode: str = "frame",
    ) -> Any:
        """Get :term:`sub<subs>`-:term:`tids` by target :term:`tids` as `ids`
        parameter.

        Parameters
        ----------
        ids
            Target :term:`tids` for which retrieve :term:`sub<subs>`-:term:`tids`
        ter_rank
            Terminal rank upto which retrieve :term:`sub<subs>`-:term:`tids`
        flatten
            Whether to flatten :term:`rids` for all ranks instead of returning Dict[rank, :term:`rids`]
        mode
            Retrieve data as 'array', 'frame' or 'dict'(default)

        Returns
        -------
            Return :term:`tids` with type depending on input parameters.
        """
        if self.storage_manager.state != 1:
            raise RuntimeError("Storage is closed.")
        if not ((ter_rank in self.avail_ranks) or (ter_rank is None)):
            raise ValueError("Invalid `ter_rank` value is provided.")
        if ids is None:
            target_ids = self.xtid.values
        else:
            target_ids = np.asarray(ids)
        target_unique_ids = np.unique(target_ids)
        if not self.xtid.isin(target_unique_ids).sum() == len(target_unique_ids):
            raise ValueError("Invalid taxon ids provided.")
        map2tid = self.storage_manager.retrieve_data_by_element("map-rep2tid")
        focus_map2tid = map2tid[map2tid.columns[map2tid.columns != "tid"]]
        target_ranks = focus_map2tid.columns[
            focus_map2tid.isin(target_unique_ids).any(axis=0)
        ].values.tolist()
        rid_mask = focus_map2tid.isin(target_unique_ids).any(axis=1)
        target_map2tid = focus_map2tid[rid_mask]
        if not flatten:
            tmp_tids_map = defaultdict(list)
            for rank in target_ranks:
                groupby = target_map2tid.groupby(rank, sort=False, axis=0)
                for tid, subtids in groupby.groups.items():
                    if tid != 0 and tid in target_unique_ids:
                        tmp_subranks = get_rank_upto(self.avail_ranks[::-1], rank)
                        if tmp_subranks:
                            if ter_rank is None:
                                tmp_subtids = target_map2tid.loc[subtids, tmp_subranks]
                                tmp_tids_map[tid].extend(
                                    np.unique(
                                        tmp_subtids.values[
                                            tmp_subtids.values > 0
                                        ].flatten()
                                    )
                                )
                            else:
                                tmp_subtids_adj = get_rank_upto(
                                    tmp_subranks[::-1], ter_rank, True
                                )
                                if tmp_subtids_adj:
                                    tmp_subtids = target_map2tid.loc[
                                        subtids, tmp_subtids_adj
                                    ]
                                    tmp_tids_map[tid].extend(
                                        np.unique(
                                            tmp_subtids.values[
                                                tmp_subtids.values > 0
                                            ].flatten()
                                        )
                                    )
            return to_mode(
                {
                    tid: np.asarray(rids, dtype=map2tid.dtypes[0])
                    for tid, rids in tmp_tids_map.items()
                },
                mode,
                target_ids,
            )
        else:
            tmp_tids_flat = set()
            for rank in target_ranks:
                groupby = target_map2tid.groupby(rank, axis=0)
                for tid, subtids in groupby.groups.items():
                    if tid != 0 and tid in target_unique_ids:
                        tmp_subranks = get_rank_upto(self.avail_ranks[::-1], rank)
                        if tmp_subranks:
                            if ter_rank is None:
                                tmp_subtids = target_map2tid.loc[subtids, tmp_subranks]
                                tmp_tids_flat.update(
                                    np.unique(
                                        tmp_subtids.values[
                                            tmp_subtids.values > 0
                                        ].flatten()
                                    ).tolist()
                                )
                            else:
                                tmp_subtids_adj = get_rank_upto(
                                    tmp_subranks[::-1], ter_rank, True
                                )
                                if tmp_subtids_adj:
                                    tmp_subtids = target_map2tid.loc[
                                        subtids, tmp_subtids_adj
                                    ]
                                    tmp_tids_flat.update(
                                        np.unique(
                                            tmp_subtids.values[
                                                tmp_subtids.values > 0
                                            ].flatten()
                                        ).tolist()
                                    )
            return to_mode(list(tmp_tids_flat), "array", None)

    def find_rid_by_tid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        subs: bool = False,
        iterator: bool = False,
        flatten: bool = False,
        mode: str = "frame",
    ) -> Any:
        """Get :term:`rids` by target :term:`tids`.

        Parameters
        ----------
        ids
            Target :term:`tids` for which retrieve :term:`sub<subs>`-:term:`tids`
        subs
            Whether to include :term:`subs`
        iterator
            Whether to return data in chunks as iterator.
        flatten
            Whether to flatten results into single array.
        mode
            Retrieve data as 'array', 'frame' or 'dict'(default)

        Returns
        -------
            Return :term:`rids` with type depending on input parameters.
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = self.xtid.values
            else:
                target_ids = np.asarray(ids, dtype=self.xtid.dtype)
            total_valid_tids = self.xtid.isin(target_ids).sum()
            target_unique_ids = np.unique(target_ids)
            if self.xtid.isin(target_unique_ids).sum() == len(target_unique_ids):
                map2tid = self.storage_manager.retrieve_data_by_element("map-rep2tid")

                def map_generator():
                    if not subs:
                        partial_map = map2tid[map2tid["tid"].isin(target_ids)]
                        tid_rid_gps = partial_map.groupby("tid", sort=False).groups
                        for tid in target_ids:
                            yield tid, tid_rid_gps.get(tid, pd.Index([])).values
                    else:
                        partial_map = map2tid[
                            map2tid[map2tid.columns[map2tid.columns != "tid"]]
                            .isin(target_ids)
                            .any(axis=1)
                        ]
                        tid_rid_gps_col = {
                            rank: partial_map.groupby(rank, sort=False).groups
                            for rank in self.avail_ranks
                        }
                        for tid in target_ids:
                            point_rank = None
                            for rank in self.avail_ranks:
                                if tid in tid_rid_gps_col[rank].keys():
                                    point_rank = rank
                                    break
                            yield tid, np.asarray(
                                []
                            ) if point_rank is None else tid_rid_gps_col[
                                point_rank
                            ].get(
                                tid, pd.Index([])
                            ).values

                tmp_map_gen = map_generator()
                if not iterator:
                    if not flatten:
                        if total_valid_tids == len(target_ids):
                            tmp_reps = defaultdict(np.ndarray)
                            for tid, rids in tmp_map_gen:
                                tmp_reps[tid] = rids
                            return to_mode(tmp_reps, mode, None)
                        else:
                            tmp_reps = pd.Series(index=target_unique_ids, dtype=object)
                            for tid, rids in tmp_map_gen:
                                tmp_reps[tid] = rids
                            return to_mode(tmp_reps.loc[target_ids], mode, None)
                    else:
                        tmp_reps_flat = set()
                        for _, rids in tmp_map_gen:
                            tmp_reps_flat.update(rids)
                        return to_mode(list(tmp_reps_flat), "array", None)
                else:
                    return tmp_map_gen
            else:
                raise ValueError("Invalid taxon ids provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def find_tid_by_rid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        levels: Union[str, Sequence[str], None] = None,
        flatten: bool = False,
        method: str = "legal",
        mode: str = "frame",
    ) -> Any:
        """Get :term:`tids` by target :term:`rids`.

        Parameters
        ----------
        ids
            Target :term:`tids` for which retrieve :term:`sub<subs>`-:term:`tids`
        levels
            Limiting taxonomic ranks
        flatten
            Whether to flatten results into single array.
        method
            Can be 'legal' for filtering non-id values like zeros or 'asis' to keep original database values.
        mode
            Retrieve data as 'array', 'frame' or 'dict'(default)

        Returns
        -------
            Return :term:`tids` with type depending on input parameters.
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = self.xrid.values
            else:
                target_ids = np.asarray(ids)
            if levels is None:
                target_ranks = np.asarray(self.avail_ranks)
            elif isinstance(levels, str):
                target_ranks = np.asarray([levels])
            else:
                target_ranks = np.asarray(levels)

            target_unique_ranks = np.asarray(sort_ranks(np.unique(target_ranks)))
            target_unique_ids = np.unique(target_ids)
            if self.xrid.isin(target_unique_ids).sum() == len(target_unique_ids):
                map2tid = self.storage_manager.retrieve_data_by_element("map-rep2tid")
                if map2tid.columns.isin(target_unique_ranks).sum() == len(
                    target_unique_ranks
                ):
                    if not flatten:
                        if len(target_ranks) > 1:
                            if method == "legal":
                                retriever = lambda rid_row: rid_row[rid_row > 0].values
                                tid_rid_product = map2tid.loc[
                                    target_unique_ids, target_unique_ranks
                                ].apply(retriever, axis=1)
                                return to_mode(
                                    tid_rid_product.loc[target_ids], mode, None
                                )
                            elif method == "asis":
                                tid_rid_product = map2tid.loc[
                                    target_unique_ids, target_unique_ranks
                                ]
                                return to_mode(
                                    tid_rid_product.loc[target_ids, target_ranks],
                                    mode,
                                    None,
                                )
                            else:
                                raise ValueError("Invalid `method` value is provided.")
                        else:
                            if method == "legal":
                                tid_array = map2tid.loc[
                                    target_unique_ids, target_unique_ranks[0]
                                ]
                                tid_rid_product = tid_array[tid_array > 0]
                                return to_mode(
                                    tid_rid_product.loc[target_ids], mode, None
                                )
                            elif method == "asis":
                                tid_rid_product = map2tid.loc[
                                    target_unique_ids, target_unique_ranks[0]
                                ]
                                return to_mode(
                                    tid_rid_product.loc[target_ids], mode, None
                                )
                            else:
                                raise ValueError("Invalid `method` value is provided.")
                    else:
                        flat_tid_rid_product = np.unique(
                            map2tid.loc[
                                target_unique_ids, target_unique_ranks
                            ].values.ravel()
                        )
                        if method == "legal":
                            tid_rid_product = flat_tid_rid_product[
                                flat_tid_rid_product > 0
                            ]
                        elif method == "asis":
                            tid_rid_product = flat_tid_rid_product
                        else:
                            raise ValueError("Invalid `method` value is provided.")
                        return to_mode(tid_rid_product, "array", None)
                else:
                    raise ValueError("Invalid `levels` is invalid.")
            else:
                raise ValueError("Invalid repseq ids provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def get_stats_by_rid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        include: Union[str, Sequence[str], None] = None,
        exclude: Union[str, Sequence[str], None] = None,
    ) -> pd.DataFrame:
        """Get pre-generated statistics for target :term:`rids`

        Parameters
        ----------
        ids
            Target :term:`rids`
        include
            Columns to include
        exclude
            Columns to exclude

        Returns
        -------
            :class:`~pandas.DataFrame` with requested statistics per :term:`rid<rids>`
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = self.xrid.values
            else:
                target_ids = np.asarray(ids)
            target_unique_ids = np.unique(target_ids)
            if self.xrid.isin(target_unique_ids).sum() == len(target_unique_ids):
                if "stat-reps" in self.storage_manager.active_elements:
                    if include is None:
                        target_inc = np.asarray([])
                    elif isinstance(include, str):
                        target_inc = np.asarray([include])
                    else:
                        target_inc = np.asarray(include)
                    if exclude is None:
                        target_exc = np.asarray([])
                    elif isinstance(exclude, str):
                        target_exc = np.asarray([exclude])
                    else:
                        target_exc = np.asarray(exclude)

                    db_summary = self.storage_manager.summary
                    rid_stat_cols = db_summary["columns-stat-reps"].split("|")
                    total_col_request = np.union1d(target_inc, target_exc)
                    target_cols = []
                    for col in total_col_request:
                        if col not in rid_stat_cols:
                            raise ValueError("Invalid column names are requested.")
                    for col in rid_stat_cols:
                        if len(target_inc) > 0 and len(target_exc) > 0:
                            if (col in target_inc) and (col not in target_exc):
                                target_cols.append(col)
                        elif len(target_inc) > 0 and len(target_exc) == 0:
                            if col in target_inc:
                                target_cols.append(col)
                        elif len(target_inc) == 0 and len(target_exc) > 0:
                            if col not in target_exc:
                                target_cols.append(col)
                        else:
                            target_cols.append(col)
                    if ids is None:
                        product = self.storage_manager.retrieve_data_by_element(
                            "stat-reps", target_cols
                        )
                    else:
                        tmp_product = self.storage_manager.get_element_data_by_ids(
                            "stat-reps", target_unique_ids
                        )
                        product = tmp_product.loc[target_ids, target_cols]
                    if not isinstance(include, str):
                        return product
                    else:
                        return product.loc[:, target_cols[0]]
                else:
                    raise RuntimeError("Storage does not contain requested stats.")
            else:
                raise ValueError("Invalid repseq ids provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def get_stats_by_tid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        include: Union[str, Sequence[str], None] = None,
        exclude: Union[str, Sequence[str], None] = None,
    ) -> pd.DataFrame:
        """Get pre-generated statistics for target :term:`tids`

        Parameters
        ----------
        ids
            Target :term:`tids`
        include
            Columns to include
        exclude
            Columns to exclude

        Returns
        -------
            :class:`~pandas.DataFrame` with requested statistics per :term:`tid<tids>`
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = self.xtid.values
            else:
                target_ids = np.asarray(ids)
            target_unique_ids = np.unique(target_ids)
            if self.xtid.isin(target_unique_ids).sum() == len(target_unique_ids):
                if "stat-taxs" in self.storage_manager.active_elements:
                    if include is None:
                        target_inc = np.asarray([])
                    elif isinstance(include, str):
                        target_inc = np.asarray([include])
                    else:
                        target_inc = np.asarray(include)
                    if exclude is None:
                        target_exc = np.asarray([])
                    elif isinstance(exclude, str):
                        target_exc = np.asarray([exclude])
                    else:
                        target_exc = np.asarray(exclude)

                    db_summary = self.storage_manager.summary
                    rid_stat_cols = db_summary["columns-stat-taxs"].split("|")
                    total_col_request = np.union1d(target_inc, target_exc)
                    target_cols = []
                    for col in total_col_request:
                        if col not in rid_stat_cols:
                            raise ValueError("Invalid column names are requested.")
                    for col in rid_stat_cols:
                        if len(target_inc) > 0 and len(target_exc) > 0:
                            if (col in target_inc) and (col not in target_exc):
                                target_cols.append(col)
                        elif len(target_inc) > 0 and len(target_exc) == 0:
                            if col in target_inc:
                                target_cols.append(col)
                        elif len(target_inc) == 0 and len(target_exc) > 0:
                            if col not in target_exc:
                                target_cols.append(col)
                        else:
                            target_cols.append(col)
                    if ids is None:
                        product = self.storage_manager.retrieve_data_by_element(
                            "stat-taxs", target_cols
                        )
                    else:
                        tmp_product = self.storage_manager.get_element_data_by_ids(
                            "stat-taxs", target_unique_ids
                        )
                        product = tmp_product.loc[target_ids, target_cols]
                    if not isinstance(include, str):
                        return product
                    else:
                        return product.loc[:, target_cols[0]]
                else:
                    raise RuntimeError("Storage does not contain requested stats.")
            else:
                raise ValueError("Invalid taxon ids provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def close(self):
        """Closes local client by shutting down storage manager."""
        self.__storage_manager.shutdown()

    @property
    def xtid(self) -> pd.Index:
        """Unique taxon identifiers."""
        if self.__storage_manager.state == 1:
            return self.__storage_manager.taxon_ids
        else:
            raise RuntimeError("Storage is closed.")

    @property
    def xrid(self) -> pd.Index:
        """Feature/Representative/Reference identifiers."""
        if self.__storage_manager.state == 1:
            return self.__storage_manager.repseq_ids
        else:
            raise RuntimeError("Storage is closed.")

    @property
    def stamp(self) -> pd.Series:
        """Database stamp during creation."""
        if self.__storage_manager.state == 1:
            return self.__storage_manager.retrieve_data_by_element("metadata-db-stamp")
        else:
            raise RuntimeError("Storage is closed.")

    @property
    def state(self) -> bool:
        """State of the storage manager and database."""
        return True if self.__storage_manager.state == 1 else False

    @property
    def summary(self) -> pd.Series:
        """Summary storage element states."""
        if self.__storage_manager.state == 1:
            return self.__storage_manager.summary
        else:
            raise RuntimeError("Storage is closed.")

    @property
    def novel_tids(self) -> np.ndarray:
        """Array of novel :term:`tids` produced during database creating."""
        if self.__storage_manager.state == 1:
            return self.__novel_tids
        else:
            raise RuntimeError("Storage is closed.")

    @property
    def storage_manager(self) -> DatabaseStorageManager:
        """Working storage manager."""
        return self.__storage_manager

    # TODO: Check all usages and make sure all use tuples then change this return hint to tuple as it should be
    @property
    def avail_ranks(
        self,
    ) -> Sequence[str]:
        """Available taxonomic ranks in the database."""
        return self.__avail_ranks
