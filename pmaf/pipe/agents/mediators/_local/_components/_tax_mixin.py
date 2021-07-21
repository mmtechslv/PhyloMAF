from pmaf.internal._constants import MAIN_RANKS
from pmaf.internal._shared import generate_lineages_from_taxa
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._metakit import (
    DockerIdentifierMetabase,
    DockerTaxonomyMetabase,
)
from pmaf.pipe.agents.mediators._metakit import MediatorTaxonomyMetabase
from pmaf.pipe.agents.mediators._local._base import MediatorLocalBase
from pmaf.pipe.factors._base import FactorBase
from pmaf.database._metakit import DatabaseTaxonomyMetabase
from pmaf.internal._shared import sort_ranks, get_rank_upto
from pmaf.database._shared._common import verify_tax_format
from collections import defaultdict
from fuzzywuzzy import process, fuzz
import warnings
import pandas as pd
import numpy as np
from typing import Optional, Any, Union


class MediatorLocalTaxonomyMixin(MediatorLocalBase, MediatorTaxonomyMetabase):
    """Mixin class for local :term:`mediator` that handle taxonomy data."""

    CORRELATION_METHODS = ["lineage", "complement", "taxon"]
    """Available methods for taxonomy correlations"""

    def __init__(
        self,
        database: DatabaseTaxonomyMetabase,
        tax_rank_tolerance: Optional[str] = None,
        tax_corr_method: str = "lineage",
        tax_fuzzy_cutoff: int = 95,
        tax_fuzzy_mode: bool = False,
        tax_format: Optional[str] = None,
        tax_refrep: Optional[str] = "tid",
        **kwargs: Any
    ):
        """Mixin class constructor for :class:`.MediatorLocalTaxonomyMixin`

        Parameters
        ----------
        database
            Instance of :class:`~pmaf.database._core._base.DatabaseBase` and :class:`~pmaf.database._core._tax_base.DatabaseTaxonomyMixin`
        tax_rank_tolerance
            Rank tolerance level when match is not found
        tax_corr_method
            Taxonomy correlation method. Can one of :attr:`.CORRELATION_METHODS`
            - The "lineage" refer to lineage based correlation approach
            - The "complement" is used when missing taxonomy (from Family to Domain) must be complemented
            - The "taxon" refer to individual and cumulative taxon matching approach
        tax_fuzzy_cutoff
            Cutoff value when fuzzy matching is enabled
        tax_fuzzy_mode
            If True enable fuzzy matching
        tax_format
            If not None then taxonomy formatting is enabled. # TODO: Elaborate on this
        tax_refrep
            Taxonomy lookup level. Can be either "tid" for :term:`tids` or "rid" for :term:`rids`
        kwargs
            Compatibility
        """
        if isinstance(database, DatabaseTaxonomyMetabase):
            if not database.storage_manager.has_tax:
                raise TypeError("`database` does not have valid taxonomy present.")
        else:
            raise TypeError("`database` must be instance of DatabaseTaxonomyMetabase")

        if tax_rank_tolerance is not None:
            if isinstance(tax_rank_tolerance, str):
                if tax_rank_tolerance not in MAIN_RANKS:
                    raise ValueError("`tax_rank_tolerance` has invalid rank.")
            else:
                raise TypeError("`tax_rank_tolerance` has invalid type.")
        if isinstance(tax_format, str):
            if not verify_tax_format(tax_format):
                raise ValueError("`tax_format` has invalid format.")
        elif tax_format is None:
            pass
        else:
            raise TypeError("`tax_format` has invalid type.")
        if isinstance(tax_corr_method, str):
            if tax_corr_method not in self.CORRELATION_METHODS:
                raise ValueError("`tax_corr_method` is unknown.")
        else:
            raise TypeError("`tax_corr_method` has invalid type.")
        if isinstance(tax_fuzzy_cutoff, int):
            if not (tax_fuzzy_cutoff > 0 and tax_fuzzy_cutoff < 100):
                raise ValueError(
                    "`tax_corr_method` must be greater than 0 and less than 100. "
                )
            if tax_fuzzy_cutoff < 90:
                warnings.warn(
                    "Warning! Assigned cutoff value is too low. Consider value greater than 90."
                )
        else:
            raise TypeError("`tax_fuzzy_cutoff` has invalid type.")
        if tax_refrep not in ["tid", "rid"]:
            raise ValueError("`tax_refrep` is invalid.")

        super().__init__(
            database=database,
            tax_rank_tolerance=tax_rank_tolerance,
            tax_corr_method=tax_corr_method,
            tax_fuzzy_cutoff=tax_fuzzy_cutoff,
            tax_fuzzy_mode=bool(tax_fuzzy_mode),
            tax_format=tax_format,
            tax_refrep=tax_refrep,
            **kwargs
        )

    def get_taxonomy_by_identifier(self, docker: DockerIdentifierMedium, factor: FactorBase, **kwargs: Any) -> DockerTaxonomyMedium:
        """Get taxonomy data that matches identifiers in `docker` within local
        database client.

        Parameters
        ----------
        docker
            A :term:`docker` :term:`singleton` identifier instance
        factor
            A :term:`factor` to accommodate matching process
        kwargs
            Compatibility

        Returns
        -------
            An instance of :class:`.DockerTaxonomyMedium` with matching identifiers.
        """
        if not self.verify_factor(factor):
            raise ValueError("`factor` is invalid.")
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_taxonomy_by_identifier(docker, **kwargs)
            else:
                raise ValueError("`docker` must be singleton.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def get_identifier_by_taxonomy(self, docker: DockerTaxonomyMedium, factor: FactorBase, **kwargs: Any) -> DockerIdentifierMedium:
        """Get local database identifiers that match target taxonomy in
        `docker` within local database client.

        Parameters
        ----------
        docker
            A :term:`docker` :term:`singleton` taxonomy instance
        factor
            A :term:`factor` to accommodate matching process
        kwargs
            Compatibility

        Returns
        -------
            An instance of :class:`.DockerIdentifierMedium` with matching taxonomy.
        """
        if not self.verify_factor(factor):
            raise ValueError("`factor` is invalid.")
        if isinstance(docker, DockerTaxonomyMetabase):
            if docker.singleton:
                return self.__retrieve_identifier_by_taxonomy(docker, **kwargs)
            else:
                raise ValueError("`docker` must be singleton.")
        else:
            raise TypeError("`docker` must be instance of DockerTaxonomyMetabase.")

    def __retrieve_identifier_by_taxonomy(self, docker, **kwargs):
        if self.configs["tax_corr_method"] == "lineage":
            return self.__correlator_lineage_by_taxonomy(docker, **kwargs)
        elif self.configs["tax_corr_method"] == "complement":
            return self.__complement_taxonomy_by_taxonomy(docker, **kwargs)
        elif self.configs["tax_corr_method"] == "taxon":
            return self.__correlator_taxon_by_taxonomy(docker, **kwargs)
        else:
            raise NotImplementedError

    def __taxon_correlator(self, ref_taxa_series, target_taxa_array):
        """Correlate taxonomy individually for 'taxon' method."""
        tmp_product = pd.DataFrame(
            index=target_taxa_array,
            columns=["match", "method", "score"],
            data=0,
            dtype=object,
        )

        exact_match_mask = ref_taxa_series.isin(target_taxa_array)
        exact_match_map = (
            ref_taxa_series[exact_match_mask]
            .reset_index()
            .set_index(ref_taxa_series.name)["index"]
        )
        tmp_product.loc[exact_match_map.index, "match"] = exact_match_map.values
        tmp_product.loc[exact_match_map.index, "method"] = "exact"

        uncorrelated_taxa = target_taxa_array[
            ~np.isin(target_taxa_array, ref_taxa_series.values)
        ]
        uncorrelated_taxa_map = pd.Series(
            data=uncorrelated_taxa, index=uncorrelated_taxa
        )
        remaining_ref_taxa = ref_taxa_series[~exact_match_mask]
        if len(uncorrelated_taxa) > 0 and len(remaining_ref_taxa) > 0:
            remaining_ref_taxa_flat = remaining_ref_taxa.drop_duplicates().values
            remaining_ref_taxa_rev = remaining_ref_taxa.reset_index().set_index(
                remaining_ref_taxa.name
            )["index"]
            fuzzy_correlated_map = uncorrelated_taxa_map.map(
                lambda taxon: process.extractOne(
                    taxon,
                    remaining_ref_taxa_flat,
                    scorer=fuzz.ratio,
                    score_cutoff=self.configs["tax_fuzzy_cutoff"],
                )
            )
            tmp_product.loc[
                fuzzy_correlated_map.index, "match"
            ] = fuzzy_correlated_map.map(
                lambda corr: remaining_ref_taxa_rev[corr[0]] if corr is not None else 0
            )
            tmp_product.loc[fuzzy_correlated_map.index, "method"] = "fuzzy"
            tmp_product.loc[
                fuzzy_correlated_map.index, "score"
            ] = fuzzy_correlated_map.map(
                lambda corr: corr[1] if corr is not None else None
            )

        return tmp_product

    # ADD RANK TOLERANCE FUNCTION
    def __correlator_taxon_by_taxonomy(self, docker, *kwargs):
        """Run taxonomy correlator for 'taxon' method."""

        ref_avail_ranks = self.client.avail_ranks
        target_avail_ranks = docker.get_avail_ranks()
        shared_ranks = [rank for rank in target_avail_ranks if rank in ref_avail_ranks]

        shared_ranks_sorted = sort_ranks(shared_ranks)

        rank_tolerance = self.__parse_rank_tolerance(shared_ranks_sorted)

        matching_df = pd.DataFrame(
            data=0, index=docker.index, columns=shared_ranks_sorted, dtype=int
        )
        match_method_df = pd.DataFrame(
            data="", index=docker.index, columns=shared_ranks_sorted, dtype=str
        )
        match_score_df = pd.DataFrame(
            data=0, index=docker.index, columns=shared_ranks_sorted, dtype=int
        )

        matched_tids = None
        last_rank = None
        for rank in shared_ranks_sorted:
            target_rank_taxonomy = docker.to_dataframe(
                ranks=rank, exclude_missing=True
            ).dropna()
            ref_rank_taxonomy = self.client.get_taxonomy_by_rank(rank)
            if matched_tids is None:
                ref_rank_taxonomy_filtered = ref_rank_taxonomy.drop_duplicates()
                target_rank_gpy = target_rank_taxonomy.groupby(target_rank_taxonomy)
                target_rank_groups = target_rank_gpy.apply(
                    lambda tax_group: tax_group.index.values
                )
                target_rank_taxonomy_unique = target_rank_groups.index.values
                matched_map = self.__taxon_correlator(
                    ref_rank_taxonomy_filtered, target_rank_taxonomy_unique
                )
                for taxon, tid, method, score in matched_map.itertuples():
                    target_taxon_ids = target_rank_groups.loc[taxon]
                    matching_df.loc[target_taxon_ids, rank] = int(tid)
                    match_method_df.loc[target_taxon_ids, rank] = method
                    match_score_df.loc[target_taxon_ids, rank] = score
                matched_tids = matched_map["match"][matched_map["match"] != 0].values
            else:
                tid_subs_map = self.client.find_sub_tids_by_tid(
                    matched_tids, ter_rank=rank, flatten=False, mode="dict"
                )
                target_rank_tid_gpy = matching_df.groupby(last_rank)
                for prior_tid, target_taxon_ids in target_rank_tid_gpy.groups.items():
                    if prior_tid != 0:
                        target_rank_sub_taxonomy = target_rank_taxonomy.loc[
                            target_rank_taxonomy.index.isin(target_taxon_ids)
                        ]
                        potential_rank_ref_tids = tid_subs_map[prior_tid]
                        ref_rank_taxonomy_filtered = ref_rank_taxonomy.loc[
                            potential_rank_ref_tids
                        ].drop_duplicates()
                        target_rank_sub_taxon_gpy = target_rank_sub_taxonomy.groupby(
                            target_rank_sub_taxonomy
                        )
                        target_rank_sub_groups = target_rank_sub_taxon_gpy.apply(
                            lambda tax_group: tax_group.index.values
                        )
                        target_rank_sub_taxonomy_unique = (
                            target_rank_sub_groups.index.values
                        )
                        matched_map = self.__taxon_correlator(
                            ref_rank_taxonomy_filtered, target_rank_sub_taxonomy_unique
                        )
                        for taxon, tid, method, score in matched_map.itertuples():
                            target_taxon_sub_ids = target_rank_sub_groups.loc[taxon]
                            matching_df.loc[target_taxon_sub_ids, rank] = int(tid)
                            match_method_df.loc[target_taxon_sub_ids, rank] = method
                            match_score_df.loc[target_taxon_ids, rank] = score
                matched_tids = matching_df.loc[
                    matching_df.loc[:, rank] != 0, rank
                ].values
            last_rank = rank

        target_taxonomy = docker.to_dataframe(ranks=shared_ranks).loc[matching_df.index]

        rank_trials = defaultdict(dict)

        valid_taxa_map_df = pd.DataFrame(
            index=target_taxonomy.index,
            columns=shared_ranks_sorted,
            data=False,
            dtype=bool,
        )

        for rev_rank in shared_ranks_sorted[::-1]:
            valid_terminal_taxa = (target_taxonomy[rev_rank].notna()) & (
                matching_df[rev_rank] != 0
            )
            valid_non_terminal_taxa = (target_taxonomy[rev_rank].isna()) & (
                matching_df[rev_rank] == 0
            )
            valid_taxa_map_df.loc[:, rev_rank] = (
                valid_terminal_taxa | valid_non_terminal_taxa
            )

        valid_taxa = valid_taxa_map_df.loc[matching_df.index].all(1)

        target_ref_map = (
            matching_df.loc[valid_taxa]
            .apply(
                lambda row: int(row[row != 0].values[-1])
                if sum(row == 0) != len(row)
                else 0,
                axis=1,
                result_type="reduce",
            )
            .astype(int)
        )
        correlations_meta = pd.DataFrame(
            index=target_ref_map.index, columns=["matches", "method"], dtype=object
        )
        correlations_meta.loc[:, "matches"] = target_ref_map.values
        correlations_meta.loc[:, "method"] = match_method_df.loc[
            target_ref_map.index, shared_ranks_sorted[-1]
        ]
        uncorrelated_taxa = target_taxonomy.index[
            ~target_taxonomy.index.isin(target_ref_map.index)
        ]

        rank_trials["kickoff"] = {
            "correlations": correlations_meta.to_dict(orient="index"),
            "uncorrelated": uncorrelated_taxa.values.tolist(),
            "added": len(target_ref_map),
            "tolerated-ranks": None,
        }

        if len(rank_tolerance) > 0 and len(uncorrelated_taxa) > 0:
            for limiting_rank in [
                rank for rank in MAIN_RANKS[::-1] if rank in rank_tolerance.keys()
            ]:
                tolerated_matching_df = matching_df.loc[
                    uncorrelated_taxa,
                    matching_df.columns[
                        ~matching_df.columns.isin(rank_tolerance[limiting_rank])
                    ],
                ]
                tolerated_shared_ranks_sorted = sort_ranks(
                    tolerated_matching_df.columns.tolist()
                )

                tolerated_target_ref_map = (
                    tolerated_matching_df.loc[uncorrelated_taxa]
                    .apply(
                        lambda row: int(row[row != 0].values[-1])
                        if sum(row == 0) != len(row)
                        else 0,
                        axis=1,
                        result_type="reduce",
                    )
                    .astype(int)
                )
                tolerated_correlations_meta = pd.DataFrame(
                    index=tolerated_target_ref_map.index,
                    columns=["matches", "method"],
                    dtype=object,
                )
                tolerated_correlations_meta.loc[
                    :, "matches"
                ] = tolerated_target_ref_map.values
                tolerated_correlations_meta.loc[:, "method"] = match_method_df.loc[
                    tolerated_target_ref_map.index, tolerated_shared_ranks_sorted[-1]
                ]
                target_ref_map = target_ref_map.append(tolerated_target_ref_map)
                uncorrelated_taxa = target_taxonomy.index[
                    ~target_taxonomy.index.isin(target_ref_map.index)
                ]

                rank_trials[limiting_rank] = {
                    "correlations": tolerated_correlations_meta.to_dict(orient="index"),
                    "uncorrelated": uncorrelated_taxa.values.tolist(),
                    "added": len(tolerated_target_ref_map),
                    "tolerated-ranks": rank_tolerance[limiting_rank],
                }
                if len(uncorrelated_taxa) == 0:
                    break

        ref_taxonomy = self.client.get_taxonomy_by_tid(levels=shared_ranks)
        identifiers_metadata = defaultdict(dict)
        identifier_dict = defaultdict(dict)
        for ix in docker.index:
            if ix in target_ref_map.index:
                if target_ref_map[ix] != 0:
                    tmp_ix_rank_metadata = dict.fromkeys(shared_ranks_sorted)
                    for rank in shared_ranks_sorted:
                        if matching_df.loc[ix, rank] != 0:
                            tmp_ix_rank_details = {
                                "reference": ref_taxonomy.loc[
                                    matching_df.loc[ix, rank], rank
                                ],
                                "target": target_taxonomy.loc[ix, rank],
                            }
                            if match_method_df.loc[ix, rank] == "exact":
                                tmp_ix_rank_metadata[rank] = {
                                    "matching-method": "exact",
                                    "match": matching_df.loc[ix, rank],
                                    "matching-details": tmp_ix_rank_details,
                                }
                            else:
                                tmp_ix_rank_metadata[rank] = {
                                    "matching-method": "fuzzy",
                                    "matching-score": match_score_df.loc[ix, rank],
                                    "matching-details": tmp_ix_rank_details,
                                }
                    identifiers_metadata[ix] = tmp_ix_rank_metadata
                    identifier_dict[ix] = int(target_ref_map.loc[ix])
                else:
                    identifier_dict[ix] = None
            else:
                identifier_dict[ix] = None

        new_metadata = {
            "configs": self.configs,
            "rank-trials": dict(rank_trials),
            "verbose": dict(identifiers_metadata),
            "master": docker.wrap_meta(),
        }
        return DockerIdentifierMedium(
            identifiers=identifier_dict, name=docker.name, metadata=new_metadata
        )

    def __complement_taxonomy_by_taxonomy(self, docker, **kwargs):
        """Run taxonomy 'complement' method to fill missing taxa."""
        target_taxonomy = docker.to_dataframe()
        docker_avail_ranks = sort_ranks(docker.get_avail_ranks())
        db_avail_ranks = self.client.avail_ranks
        shared_avail_ranks = [
            rank for rank in docker_avail_ranks if rank in db_avail_ranks
        ]
        lower_taxa_func = lambda taxon: taxon if type(taxon) != str else taxon.lower()

        tdb_taxonomy = self.client.get_taxonomy_by_tid()
        target_taxonomy_low = target_taxonomy.applymap(lower_taxa_func)
        tdb_taxonomy_low = tdb_taxonomy.applymap(lower_taxa_func)

        shared_avail_ranks_tolerated = sort_ranks(shared_avail_ranks)
        tmp_metadata_ranks = defaultdict(dict)

        index_ref = target_taxonomy.index
        index_matched = []
        index_unmatched = target_taxonomy_low.index

        tmp_correlations = dict.fromkeys(index_unmatched, None)
        tmp_corr_metadata = dict.fromkeys(index_unmatched, None)
        tmp_transit = dict.fromkeys(index_unmatched, None)

        trial = 0
        total_match = False
        while len(shared_avail_ranks_tolerated) > 0 and (not total_match):
            database_lineages = generate_lineages_from_taxa(
                tdb_taxonomy_low.loc[:, db_avail_ranks],
                True,
                shared_avail_ranks_tolerated,
            )
            target_lineages = generate_lineages_from_taxa(
                target_taxonomy_low.loc[index_unmatched, :],
                True,
                shared_avail_ranks_tolerated,
            )
            correlations = self.__primary_lineage_correlator(
                target_lineages, database_lineages
            )
            matched_corr = correlations[correlations["matches"].map(len) > 0]
            index_matched.extend(matched_corr.index.tolist())
            index_unmatched = index_ref[~index_ref.isin(index_matched)]
            for ix, corrs, method in matched_corr.itertuples():
                if method == "exact":
                    selected_corr = corrs[0]
                    tmp_matches_metadata = {
                        "win": selected_corr,
                        "all": corrs,
                        "lineages": {corr: database_lineages[corr] for corr in corrs},
                    }
                else:
                    tmp_corrs = sorted(corrs, key=lambda fzc: fzc[1], reverse=True)
                    selected_corr = tmp_corrs[0][0]
                    tmp_matches_metadata = {
                        "win": selected_corr,
                        "all": tmp_corrs,
                        "lineages": {
                            corr: database_lineages[corr] for corr, _ in tmp_corrs
                        },
                    }
                tmp_correlations[ix] = selected_corr
                tmp_corr_metadata[ix] = {
                    "method": method,
                    "verbose": tmp_matches_metadata,
                    "rank-tolerance-trial": trial,
                }
                tmp_pass_ranks = get_rank_upto(
                    docker_avail_ranks[::-1], shared_avail_ranks_tolerated[-1]
                )
                tmp_transit[ix] = {
                    "method": method,
                    "lost-taxonomy": {
                        rank: docker.data[ix][rank] for rank in tmp_pass_ranks
                    },
                }
            tmp_metadata_ranks[trial] = {
                "ranks": tuple(shared_avail_ranks_tolerated),
                "matched": len(matched_corr),
                "unmatched": len(index_unmatched),
            }
            shared_avail_ranks_tolerated = shared_avail_ranks_tolerated[:-1]
            total_match = True if len(index_unmatched) == 0 else False
            trial = trial + 1
        new_metadata = {
            "configs": self.configs,
            "correlations": tmp_corr_metadata,
            "master": docker.wrap_meta(),
        }
        return DockerIdentifierMedium(
            identifiers=tmp_correlations,
            name=docker.name,
            metadata=new_metadata,
            _transit=tmp_transit,
        )

    def __retrieve_taxonomy_by_identifier(self, docker, **kwargs):
        """Get taxonomy that match identifiers depending on `tax_refrep`
        config."""
        valid_identifier = docker.get_subset(exclude_missing=True)
        id_array = valid_identifier.to_array(unique=True)
        if self.configs["tax_refrep"] == "tid":
            tmp_taxonomy_df = self.client.get_taxonomy_by_tid(ids=id_array)
        elif self.configs["tax_refrep"] == "rid":
            tmp_taxonomy_df = self.client.get_taxonomy_by_rid(
                ids=id_array, tax_format=self.configs["tax_format"]
            )
        else:
            raise ValueError("`tax_refrep` is invalid.")
        id_map = defaultdict(list)
        for ix, dbix in valid_identifier.get_iterator():
            id_map[dbix].append(ix)
        tmp_taxonomy = dict.fromkeys(docker.index, None)
        for dbix, taxa in tmp_taxonomy_df.iterrows():
            for ix in id_map[dbix]:
                tmp_taxonomy[ix] = taxa.to_dict()
        if (
            self.configs["tax_corr_method"] == "complement"
            and docker._transit is not None
        ):
            for ix in tmp_taxonomy.keys():
                if tmp_taxonomy[ix] is not None:
                    tmp_taxonomy[ix].update(docker._transit[ix]["lost-taxonomy"])
        new_metadata = {"configs": self.configs, "master": docker.wrap_meta()}
        return DockerTaxonomyMedium(
            taxonomy=tmp_taxonomy, name=docker.name, metadata=new_metadata
        )

    def __correlator_lineage_by_taxonomy(self, docker, **kwargs):
        """Run taxonomy correlator using 'lineage' method."""
        ref_avail_ranks = self.client.avail_ranks
        target_avail_ranks = docker.get_avail_ranks()
        shared_ranks = [rank for rank in target_avail_ranks if rank in ref_avail_ranks]
        parsed_rank_tolerance = self.__parse_rank_tolerance(shared_ranks)
        ref_taxonomy = self.client.get_taxonomy_by_rank(shared_ranks)
        ref_lineages = generate_lineages_from_taxa(
            ref_taxonomy, missing_rank=True, desired_ranks=shared_ranks
        )
        target_taxonomy = docker.to_dataframe(exclude_missing=True, ranks=shared_ranks)
        correlations, matching_details, rank_trials = self.__correlate_dfs_by_lineage(
            ref_lineages, target_taxonomy, shared_ranks, parsed_rank_tolerance
        )
        return self.__parse_lineage_correlation_result(
            docker, correlations, matching_details, rank_trials
        )

    def __parse_lineage_correlation_result(
        self, master_taxonomy_singleton, correlations, matching_details, rank_trials
    ):
        """Parse 'lineage' correlation result."""
        identifiers_dict = dict.fromkeys(master_taxonomy_singleton.index)
        identifiers_metadata = dict.fromkeys(master_taxonomy_singleton.index)
        for ix in master_taxonomy_singleton.index:
            if ix in correlations.index:
                tmp_correlation = correlations.loc[ix]
                for match_result in tmp_correlation["matches"]:
                    if tmp_correlation["method"] == "exact":
                        identifiers_dict[ix] = match_result
                        identifiers_metadata[ix] = {
                            "matching-method": "exact",
                            "matching-details": {
                                "reference": matching_details["ref-values"][
                                    match_result
                                ],
                                "target": matching_details["target-values"][ix],
                            },
                        }
                    else:
                        identifiers_dict[ix] = match_result[0]
                        identifiers_metadata[ix] = {
                            "matching-method": "fuzzy",
                            "matching-score": match_result[1],
                            "matching-details": {
                                "reference": matching_details["ref-values"][
                                    match_result[0]
                                ],
                                "target": matching_details["target-values"][ix],
                            },
                        }
            else:
                identifiers_dict[ix] = None
                identifiers_metadata[ix] = {"matching-method": "fuzzy"}
        new_metadata = {
            "configs": self.configs,
            "rank-trials": rank_trials,
            "verbose": dict(identifiers_metadata),
            "master": master_taxonomy_singleton.wrap_meta(),
        }
        return DockerIdentifierMedium(
            identifiers=identifiers_dict,
            name=master_taxonomy_singleton.name,
            metadata=new_metadata,
        )

    def __correlate_dfs_by_lineage(
        self, ref_lineages, target_taxonomy, shared_ranks, rank_tolerance
    ):
        """Perform lineage correlation for taxonomy dataframe."""
        self_lineages = generate_lineages_from_taxa(
            target_taxonomy, True, shared_ranks, False
        )
        correlations = self.__primary_lineage_correlator(self_lineages, ref_lineages)
        uncorrelated_feature_ids = self_lineages.index[
            ~self_lineages.index.isin(correlations.index)
        ]
        uncorrelated_lineages = self_lineages[uncorrelated_feature_ids]
        rank_trials = defaultdict(dict)
        matching_details = {
            "target-values": self_lineages[correlations.index].to_dict()
        }
        rank_trials["kickoff"] = {
            "correlations": correlations.to_dict(orient="index"),
            "uncorrelated": uncorrelated_feature_ids.values.tolist(),
            "added": len(correlations),
            "tolerated-ranks": None,
        }
        if len(rank_tolerance) > 0 and len(uncorrelated_lineages) > 0:
            for limiting_rank in [
                rank for rank in MAIN_RANKS[::-1] if rank in rank_tolerance.keys()
            ]:
                self_lineages = generate_lineages_from_taxa(
                    target_taxonomy, True, shared_ranks, rank_tolerance[limiting_rank]
                )
                unassigned_self_lineages = self_lineages.loc[uncorrelated_feature_ids]
                new_correlations = self.__primary_lineage_correlator(
                    unassigned_self_lineages, ref_lineages
                )
                correlations = correlations.append(new_correlations)
                uncorrelated_feature_ids = self_lineages.index[
                    ~self_lineages.index.isin(correlations.index)
                ]
                uncorrelated_lineages = self_lineages[uncorrelated_feature_ids]
                matching_details["target-values"].update(
                    self_lineages[new_correlations.index].to_dict()
                )
                rank_trials[limiting_rank] = {
                    "correlations": new_correlations.to_dict(orient="index"),
                    "uncorrelated": uncorrelated_feature_ids.values.tolist(),
                    "added": len(new_correlations),
                    "tolerated-ranks": rank_tolerance[limiting_rank],
                }
                if len(uncorrelated_lineages) == 0:
                    break
        matched_ids = [
            list(match_elem)
            for match_elem in correlations[correlations["method"] == "exact"][
                "matches"
            ].values
        ]
        matched_ids.extend(
            [
                list(fuzzy_elem[0] for fuzzy_elem in match_elem)
                for match_elem in correlations[correlations["method"] == "fuzzy"][
                    "matches"
                ].values
            ]
        )
        matched_ids_flat = [
            matched_id
            for matched_ids_elem in matched_ids
            for matched_id in matched_ids_elem
        ]
        matching_details.update(
            {"ref-values": ref_lineages[matched_ids_flat].to_dict()}
        )
        return correlations, matching_details, rank_trials

    def __primary_lineage_correlator(
        self, primary_lineages: pd.Series, secondary_lineages: pd.Series
    ) -> pd.DataFrame:
        """Correlates lineages and returns results of correlations. If
        `secondary_lineages` has duplicates then all duplicates will be removed
        except first.

        Parameters
        ----------
        primary_lineages
            pandas Series of target taxonomy with taxon IDs as index and lineage as values
        secondary_lineages
            pandas Series of reference taxonomy with taxon IDs as index and lineage as values

        Returns
        -------
            Dictionary with correlation results. Result format:
            {'assigned': pandas Index with matched lineages, 'unassigned':
            pandas Series with unmatched lineages, 'correlations': pandas Series
            with index with IDs from `primary_lineages` and values from index
            `secondary_lineages` , 'duplicated': pandas Series with lineages
            that had duplicates including first element among duplicates,
            'verbose': pandas Dataframe with lineages as index, target(
            `primary_lineages` ) taxonomy IDs as primary_id column and
            reference( `secondary_lineages` ) taxonomy IDs(or None if unmatched)
            as secondary_id column}
        """
        ref_lineages = secondary_lineages.str.lower()
        target_lineages = primary_lineages.str.lower()

        match_mask = ref_lineages.isin(target_lineages)
        matching_lineages = ref_lineages[match_mask]
        matchlin_gby = matching_lineages.groupby(matching_lineages)
        gr_ref_lin_df = matchlin_gby.apply(
            lambda lin_group: lin_group.index.values
        ).reset_index()
        gr_ref_lin_df.columns = ["lineage", "matches"]
        gr_ref_lin_df = gr_ref_lin_df.set_index("lineage")
        trg_lin_df = target_lineages.reset_index()
        trg_lin_df.columns = ["target", "lineage"]
        trg_lin_df = trg_lin_df.set_index("lineage")
        correlated_lineages = trg_lin_df.join(gr_ref_lin_df, how="inner").set_index(
            "target"
        )
        correlated_lineages["method"] = "exact"
        if self.configs["tax_fuzzy_mode"]:
            uncorrelated = target_lineages[
                ~target_lineages.index.isin(correlated_lineages.index)
            ]
            remaining_ref_lin = ref_lineages[~match_mask].drop_duplicates()
            remaining_ref_lin_flat = remaining_ref_lin.values.tolist()
            remaining_ref_lin.name = "lineage"
            remaining_ref_lin_map = (
                remaining_ref_lin.reset_index().set_index("lineage")["index"].to_dict()
            )

            fuzzy_correlated_lineages = uncorrelated.map(
                lambda lin: process.extractOne(
                    lin,
                    remaining_ref_lin_flat,
                    scorer=fuzz.ratio,
                    score_cutoff=self.configs["tax_fuzzy_cutoff"],
                )
            )
            fuzzy_correlated_lineages_fixed = fuzzy_correlated_lineages.map(
                lambda corr: [(remaining_ref_lin_map[corr[0]], corr[1])]
                if corr is not None
                else []
            ).to_frame("matches")
            fuzzy_correlated_lineages_fixed["method"] = "fuzzy"
            correlated_lineages = correlated_lineages.append(
                fuzzy_correlated_lineages_fixed
            )
        correlated_lineages_valid = correlated_lineages[
            correlated_lineages["matches"]
            .map(lambda tmp_matches: len(tmp_matches))
            .astype(bool)
        ]
        return correlated_lineages_valid

    def __parse_rank_tolerance(self, target_ranks):
        """Here rank lists are generated until it reaches upto_rank.

        For example, if upto_rank='f' and shared_avail_ranks=['c', 'o',
        'f', 'g', 's'] then return will contain {'f': ['g', 's'], 'g':
        ['s']}
        """
        target_ranks_sorted = sort_ranks(target_ranks)
        if (self.configs["tax_rank_tolerance"] in target_ranks_sorted) and (
            (target_ranks_sorted.index(self.configs["tax_rank_tolerance"]) + 1)
            != len(target_ranks_sorted)
        ):
            tol_index = len(target_ranks_sorted) - target_ranks_sorted.index(
                self.configs["tax_rank_tolerance"]
            )
            return {
                target_ranks_sorted[-(e + 1)]: target_ranks_sorted[-e:]
                for e in range(1, tol_index)
            }
        else:
            return {}
