from pmaf.pipe.agents.mediators._metakit import MediatorPhylogenyMetabase
from pmaf.pipe.agents.mediators._local._base import MediatorLocalBase
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase
from pmaf.pipe.agents.dockers._mediums._phy_medium import DockerPhylogenyMedium
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.database._metakit import DatabasePhylogenyMetabase
from pmaf.pipe.factors._base import FactorBase
from typing import Optional, Any


class MediatorLocalPhylogenyMixin(MediatorLocalBase, MediatorPhylogenyMetabase):
    """Mixin class for local :term:`mediator` that handle phylogeny data."""

    PHYLO_EXTRACT_METHODS = ["infer", "prune"]

    def __init__(
        self,
        database: DatabasePhylogenyMetabase,
        phy_method: str = "infer",
        phy_sub_nodes: bool = True,
        phy_ignore_tips: bool = False,
        phy_refrep: str = "tid",
        **kwargs: Any
    ):
        """Mixin class constructor for :class:`.MediatorLocalPhylogenyMixin`

        Parameters
        ----------
        database
            Instance of :class:`~pmaf.database._core._base.DatabaseBase` and :class:`~pmaf.database._core._phy_base.DatabasePhylogenyMixin`
        phy_method
            Phylogeny retrieval method. Can be either "infer" or "prune"
        phy_sub_nodes
            Whether :term:`mediator` should include :term:`subs`
        phy_ignore_tips
            Ignore duplicated tips
        phy_refrep
            Taxonomy lookup level. Can be either "tid" for :term:`tids` or "rid" for :term:`rids`
        kwargs
            Compatibility
        """
        if isinstance(database, DatabasePhylogenyMetabase):
            if not database.storage_manager.has_tree:
                raise TypeError("`database` does not have valid tree present.")
        else:
            raise TypeError("`database` must be instance of DatabasePhylogenyMetabase")
        if isinstance(phy_method, str):
            if phy_method not in self.PHYLO_EXTRACT_METHODS:
                raise ValueError("`phy_method` is unknown.")
        else:
            raise TypeError("`phy_method` has invalid type.")
        if phy_refrep not in ["tid", "rid"]:
            raise ValueError("`phy_refrep` is invalid.")
        super().__init__(
            database=database,
            phy_method=phy_method,
            phy_sub_nodes=bool(phy_sub_nodes),
            phy_ignore_tips=bool(phy_ignore_tips),
            phy_refrep=phy_refrep,
            **kwargs
        )

    def get_phylogeny_by_identifier(
        self, docker: DockerIdentifierMedium, factor: FactorBase, **kwargs: Any
    ) -> DockerPhylogenyMedium:
        """Get phylogeny data that matches identifiers in `docker` within local
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
            An instance of :class:`.DockerPhylogenyMedium` with matching identifiers.
        """
        if not self.verify_factor(factor):
            raise ValueError("`factor` is invalid.")
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_phylogeny_by_identifier(docker, **kwargs)
            else:
                raise ValueError("`docker` must be singleton.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def get_identifier_by_phylogeny(self, docker, factor, **kwargs):
        """:meta private:"""
        raise NotImplementedError

    def __retrieve_phylogeny_by_identifier(self, docker, **kwargs):
        """Actual method that retrieves phylogeny based on specified method in
        configurations."""
        id_array = docker.to_array(exclude_missing=True)
        if (
            self.configs["phy_refrep"] == "tid"
            and self.configs["phy_method"] == "infer"
        ):
            tmp_tree = self.client.infer_topology_by_tid(
                ids=id_array, subreps=self.configs["phy_sub_nodes"], include_rid=False
            )
        elif (
            self.configs["phy_refrep"] == "rid"
            and self.configs["phy_method"] == "infer"
        ):
            tmp_tree = self.client.infer_topology_by_rid(ids=id_array)
        elif (
            self.configs["phy_refrep"] == "tid"
            and self.configs["phy_method"] == "prune"
        ):
            tmp_tree = self.client.prune_tree_by_tid(
                ids=id_array, subreps=self.configs["phy_sub_nodes"], include_rid=False
            )
        elif (
            self.configs["phy_refrep"] == "rid"
            and self.configs["phy_method"] == "prune"
        ):
            tmp_tree = self.client.prune_tree_by_rid(ids=id_array)
        else:
            raise ValueError("`phy_refrep` or `phy_method` is invalid.")

        tmp_identifier_valids = docker.get_subset(exclude_missing=True)
        id_rev_map = {str(v): str(k) for k, v in tmp_identifier_valids.data.items()}
        tmp_tree.replace_nodes_by_map(id_rev_map, only_tips=True)
        new_metadata = {
            "configs": self.configs,
            "id-map": tmp_identifier_valids.data,
            "master": docker.wrap_meta(),
        }
        return DockerPhylogenyMedium(
            tmp_tree,
            ignore_tips=self.configs["phy_ignore_tips"],
            name=docker.name,
            metadata=new_metadata,
        )
