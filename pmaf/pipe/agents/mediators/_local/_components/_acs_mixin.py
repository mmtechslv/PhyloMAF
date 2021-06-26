from pmaf.pipe.agents.mediators._metakit import MediatorAccessionMetabase
from pmaf.pipe.agents.mediators._local._base import MediatorLocalBase
from pmaf.database._metakit import DatabaseAccessionMetabase
from pmaf.pipe.agents.dockers._mediums._acs_medium import DockerAccessionMedium
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase
from pmaf.pipe.factors._base import FactorBase
import numpy as np
from collections import defaultdict
from typing import Optional, Any


class MediatorLocalAccessionMixin(MediatorLocalBase, MediatorAccessionMetabase):
    """Mixin class for local :term:`mediator` that handle accession data."""

    ACS_FILTER_METHODS = ["random", "first"]

    def __init__(
        self,
        database: DatabaseAccessionMetabase,
        acs_refrep: str = "tid",
        acs_sub_nodes: bool = False,
        acs_filter_method: Optional[str] = None,
        acs_filter_value: Optional[str] = None,
        **kwargs: Any
    ):
        """Mixin class constructor for :class:`.MediatorLocalAccessionMixin`

        Parameters
        ----------
        database
            Instance of :class:`~pmaf.database._core._base.DatabaseBase` and :class:`~pmaf.database._core._acs_base.DatabaseAccessionMixin`
        acs_refrep
            Taxonomy lookup level. Can be either "tid" for :term:`tids` or "rid" for :term:`rids`
        acs_sub_nodes
            Whether :term:`mediator` should include :term:`subs`
        acs_filter_method
            Method to filter accession numbers. Can be "random" and "first"
        acs_filter_value
            Complementary value for the `acs_filter_method`.
        kwargs
            Compatibility
        """
        if isinstance(database, DatabaseAccessionMetabase):
            if not database.storage_manager.has_accs:
                raise TypeError("`database` does not have valid accessions.")
        else:
            raise TypeError("`database` must be instance of DatabaseAccessionMetabase")
        if acs_refrep not in ["tid", "rid"]:
            raise ValueError("`acs_refrep` is invalid.")
        if acs_filter_method is not None:
            if isinstance(acs_filter_method, str):
                if not acs_filter_method in self.ACS_FILTER_METHODS:
                    raise ValueError("`acs_filter_method` is unknown.")
            elif callable(acs_filter_method):
                pass
            else:
                raise TypeError("`acs_filter_method` has invalid type.")
        if acs_filter_value is not None:
            if not isinstance(acs_filter_value, int):
                raise TypeError("`seq_filter_value` has invalid type.")
        super().__init__(
            database=database,
            acs_refrep=acs_refrep,
            acs_sub_nodes=bool(acs_sub_nodes),
            acs_filter_method=acs_filter_method,
            acs_filter_value=acs_filter_value,
            **kwargs
        )

    def get_accession_by_identifier(
        self, docker: DockerIdentifierMedium, factor: FactorBase, **kwargs: Any
    ) -> DockerAccessionMedium:
        """Get accession data that matches identifiers in `docker` within local
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
            An instance of :class:`.DockerAccessionMedium` with matching identifiers.
        """
        if not self.verify_factor(factor):
            raise ValueError("`factor` is invalid.")
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_accessions_by_identifier(docker, **kwargs)
            else:
                raise ValueError("`docker` must be singleton.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def __retrieve_accessions_by_identifier(self, docker, **kwargs):
        """Actual method to retrieve accession data from identifiers."""
        id_array = docker.to_array(exclude_missing=True)
        tmp_accessions = dict.fromkeys(id_array, None)
        tmp_metadata = dict.fromkeys(id_array, None)
        if self.configs["acs_refrep"] == "tid":
            tmp_db_accessions = self.client.get_accession_by_tid(
                ids=id_array, subs=self.configs["acs_sub_nodes"], iterator=False
            )
            for tid, accs_dict in tmp_db_accessions.items():
                (
                    tmp_accessions[tid],
                    tmp_metadata[tid],
                ) = self.__filter_rids_from_tids_accessions(accs_dict)
        elif self.configs["acs_refrep"] == "rid":
            tmp_db_accessions = self.client.get_accession_by_rid(
                ids=id_array, iterator=False
            )
            for rid, accs_dict in tmp_db_accessions.items():
                tmp_accessions[rid] = accs_dict
        else:
            raise ValueError("`acs_refrep` is invalid.")
        new_metadata = {
            "configs": self.configs,
            "verbose": tmp_metadata,
            "master": docker.wrap_meta(),
        }
        id_rev_map = {
            v: k for k, v in docker.get_subset(exclude_missing=True).data.items()
        }
        tmp_results_adj = {id_rev_map[k]: v for k, v in tmp_accessions.items()}
        tmp_results_adj.update({tid: None for tid in docker.missing})
        return DockerAccessionMedium(
            tmp_results_adj, name=docker.name, metadata=new_metadata
        )

    def __filter_rids_from_tids_accessions(self, accs_dict):
        """Filter matched accessions based on filtering configuration."""
        tmp_accs_dict = defaultdict(list)
        if self.configs["acs_filter_method"] == "random" and isinstance(
            self.configs["acs_filter_value"], int
        ):
            if len(accs_dict) > self.configs["acs_filter_value"]:
                tmp_target_ids = np.random.choice(
                    list(accs_dict.keys()), self.configs["acs_filter_value"], False
                )
            else:
                tmp_target_ids = list(accs_dict.keys())
            for rid in tmp_target_ids:
                for accs_src, accs_no in accs_dict[rid].items():
                    tmp_accs_dict[accs_src].append(accs_no)
            tmp_metadata_dict = {
                "total-rids": len(accs_dict),
                "selected-rids": len(tmp_target_ids),
            }
            ret = {k: tuple(v) for k, v in tmp_accs_dict.items()}
        elif self.configs["acs_filter_method"] == "first":
            ret = next(iter(accs_dict.values()))
            tmp_metadata_dict = {"total-rids": len(accs_dict), "selected-rids": 1}
        else:
            tmp_accs_dict = defaultdict(list)
            for rid, accs_elem_dict in accs_dict.items():
                for accs_src, accs_no in accs_elem_dict.items():
                    tmp_accs_dict[accs_src].append(accs_no)
            tmp_metadata_dict = {
                "total-rids": len(accs_dict),
                "selected-rids": len(accs_dict),
            }
            ret = {k: tuple(v) for k, v in tmp_accs_dict.items()}
        return ret, tmp_metadata_dict

    def get_identifier_by_accession(self, docker, factor, **kwargs): # TODO: This method is not yet implemented so fix it.
        """Get local database identifiers that match target accession numbers
        in `docker` within local database client.

        :meta private:

        Parameters
        ----------
        docker
            A :term:`docker` :term:`singleton` accession instance
        factor
            A :term:`factor` to accommodate matching process
        kwargs
            Compatibility

        Returns
        -------
            An instance of :class:`.DockerIdentifierMedium` with matching accessions.

            THIS METHOD IS CURRENTLY NOT IMPLEMENTED
        """
        raise NotImplementedError
