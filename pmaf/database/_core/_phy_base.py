from pmaf.database._metakit import DatabasePhylogenyMetabase
from pmaf.phylo.tree._tree import PhyloTree
import numpy as np
import pandas as pd
from collections import defaultdict
import ete3
import pickle
from pmaf.internal._typing import AnyGenericIdentifier
from typing import Optional, Tuple


class DatabasePhylogenyMixin(DatabasePhylogenyMetabase):
    """Mixin class for handling phylogeny data."""

    def __retrieve_tree_instance(self):
        tree_pickled = self.storage_manager.retrieve_data_by_element("tree-object")
        return pickle.loads(tree_pickled)

    @staticmethod
    def __copy_ete3_node(node: ete3.Tree) -> ete3.Tree:
        """Static method that make a ete3 tree node copy.

        Parameters
        ----------
        node
            Ete3 Tree

        Returns
        -------
        """
        tmp_node = ete3.TreeNode()
        for feature in node.features:
            tmp_node.add_feature(feature, getattr(node, feature))
        return tmp_node

    def prune_tree_by_tid(
        self,
        ids: AnyGenericIdentifier,
        subreps: bool = False,
        include_rid: bool = False,
    ) -> PhyloTree:
        """Prune reference tree and keep tips with `ids`

        Parameters
        ----------
        ids
            Target :term:`tids` or tips of the tree to keep.
        subreps
            Whether to look for :term:`subs`.
        include_rid
            Whether to keep phylogeny with :term:`rids` attached to :term:`tids`.

        Returns
        -------
           Pruned reference phylogenetic tree.
        """
        if self.storage_manager.state == 1:
            target_ids = np.unique(np.asarray(ids))
            if self.xtid.isin(target_ids).sum() == len(target_ids):
                repseq_map = self.find_rid_by_tid(
                    target_ids, subs=subreps, iterator=False, flatten=False, mode="dict"
                )
                if min(map(len, repseq_map.values())) == 0:
                    raise ValueError(
                        "At least one of tids does not contain any direct rids. Use `subreps=True` to prevent this error."
                    )
                rids_flat = list(
                    set(
                        [
                            str(rid)
                            for rid_list in repseq_map.values()
                            for rid in rid_list
                        ]
                    )
                )
                tid_rid_map = {
                    tid: list(map(str, rids)) for tid, rids in repseq_map.items()
                }

                ref_tree = self.__retrieve_tree_instance()

                target_nodes = []
                tid_rid_node_map = defaultdict(list)
                for node in ref_tree.iter_leaves():
                    if node.name in rids_flat:
                        target_nodes.append(node)
                        for tid, rids in tid_rid_map.items():
                            if node.name in rids:
                                tid_rid_node_map[tid].append(node)

                node_map = defaultdict(None)
                tmp_tree = self.__copy_ete3_node(ref_tree)
                tmp_tree.name = "root"
                node_map[ref_tree] = tmp_tree

                for node in target_nodes:
                    ancestors = [node] + node.get_ancestors()
                    for ancestor in ancestors[::-1][1:]:
                        if ancestor not in node_map.keys():
                            tmp_new_node = self.__copy_ete3_node(ancestor)
                            node_map[ancestor.up].add_child(tmp_new_node)
                            node_map[ancestor] = tmp_new_node

                tmp_tree.standardize(preserve_branch_length=True)
                if not include_rid:
                    adj_tids = []
                    for tid, rid_nodes in tid_rid_node_map.items():
                        new_rid_nodes = [node_map[node] for node in rid_nodes]
                        adj_tid = "t{}".format(str(tid))
                        adj_tids.append(adj_tid)
                        if len(new_rid_nodes) > 1:
                            tmp_tid_node = tmp_tree.get_common_ancestor(new_rid_nodes)
                            tmp_tid_node.add_child(name=adj_tid)
                        else:
                            new_rid_nodes[0].add_child(name=adj_tid)

                    tmp_tree.prune(adj_tids, preserve_branch_length=True)
                    for leave in tmp_tree.traverse():
                        if leave.name.startswith("t"):
                            leave.name = leave.name[1:]
                else:
                    for node in target_nodes:
                        node_map[node].name = "r{}".format(node.name)

                    for tid, rid_nodes in tid_rid_node_map.items():
                        new_rid_nodes = [node_map[node] for node in rid_nodes]
                        if len(new_rid_nodes) > 1:
                            tmp_mcra = tmp_tree.get_common_ancestor(new_rid_nodes)
                            if tmp_mcra.name.startswith("t"):
                                tmp_mcra.add_sister(name=str(tid))
                            else:
                                tmp_mcra.name = str(tid)
                        else:
                            if new_rid_nodes[0].name.startswith("t"):
                                new_rid_nodes[0].add_sister(name=str(tid))
                            else:
                                new_rid_nodes[0].name = str(tid)
                return PhyloTree(tmp_tree)
            else:
                raise RuntimeError("Invalid identifiers are provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def prune_tree_by_rid(self, ids: AnyGenericIdentifier) -> PhyloTree:
        """Prune the reference tree and keep `ids`

        Parameters
        ----------
        ids
            Target :term:`rids` or tips of the tree to keep.

        Returns
        -------
            Pruned reference phylogenetic tree
        """
        if self.storage_manager.state == 1:
            target_ids = np.unique(np.asarray(ids))
            if self.xrid.isin(target_ids).sum() == len(target_ids):
                repseq_ids = list(map(str, target_ids))
                ref_tree = self.__retrieve_tree_instance()

                target_nodes = []
                for node in ref_tree.iter_leaves():
                    if node.name in repseq_ids:
                        target_nodes.append(node)

                node_map = defaultdict(None)
                tmp_tree = self.__copy_ete3_node(ref_tree)
                node_map[ref_tree] = tmp_tree

                for node in target_nodes:
                    ancestors = [node] + node.get_ancestors()
                    for ancestor in ancestors[::-1][1:]:
                        if ancestor not in node_map.keys():
                            tmp_new_node = self.__copy_ete3_node(ancestor)
                            node_map[ancestor.up].add_child(tmp_new_node)
                            node_map[ancestor] = tmp_new_node
                tmp_tree.standardize(preserve_branch_length=True)
                return PhyloTree(tmp_tree)
            else:
                raise RuntimeError("Invalid identifiers are provided.")
        else:
            raise RuntimeError("Storage is closed.")

    # TODO: This function should work with PhyloTree not ete3.Tree
    @staticmethod
    def __fix_mapped_tree_nodes(
        tree: ete3.Tree,
        root_name: str,
        tips: Optional[AnyGenericIdentifier] = None,
    ) -> ete3.Tree:
        """Private helper method to fix tree nodes during by standardizing the
        tree and removing intermediate nodes.

        Parameters
        ----------
        tree
            Target tree to fix
        root_name
            Root of the target tree
        tips
            Tips to prune for

        Returns
        -------
            Return fixed tree
        """
        tree.standardize(preserve_branch_length=True)
        for node in tree.traverse():
            if node.name == root_name:
                node.name = "root"
            elif node.name.startswith("+") or node.name.startswith("r+"):
                node.name = ""
        if tips is not None:
            tree.prune(tips, preserve_branch_length=True)
        return tree

    def infer_topology_by_tid(
        self,
        ids: AnyGenericIdentifier,
        subreps: bool = False,
        include_rid: bool = False,
    ) -> PhyloTree:
        """Quickly infers topology from tree node map.

        Parameters
        ----------
        ids
            Tips to keep.
        subreps
            Whether to look for :term:`subs`.
        include_rid
            Whether to keep phylogeny with :term:`rids` attached to :term:`tids`.

        Returns
        -------
            Pruned reference phylogenetic tree.
        """
        if self.storage_manager.state == 1:
            target_ids = np.unique(np.asarray(ids))
            if self.xtid.isin(target_ids).sum() == len(target_ids):
                repseq_map = self.find_rid_by_tid(
                    target_ids, subs=subreps, iterator=False, flatten=False, mode="dict"
                )
                if min(map(len, repseq_map.values())) == 0:
                    raise ValueError(
                        "At least one of tids does not contain any direct rids. Use `subreps=True` to prevent this error."
                    )
                rids_flat = list(
                    set(
                        [
                            str(rid)
                            for rid_list in repseq_map.values()
                            for rid in rid_list
                        ]
                    )
                )
                tree_map_df, root_node_name = self.__make_tree_map_by_rid(rids_flat)
                (
                    preceding_list_dict,
                    following_df_dict,
                ) = self.__make_aligned_lineage_maps(tree_map_df, repseq_map)
                if not include_rid:
                    tmp_tree = self.__infer_tree_for_tids(
                        preceding_list_dict, root_node_name
                    )
                    return PhyloTree(
                        self.__fix_mapped_tree_nodes(
                            tmp_tree, root_node_name, list(preceding_list_dict.keys())
                        )
                    )
                else:
                    tmp_tree = self.__infer_tree_for_tids_with_rids(
                        preceding_list_dict, following_df_dict, root_node_name
                    )
                    return PhyloTree(
                        self.__fix_mapped_tree_nodes(tmp_tree, root_node_name)
                    )
            else:
                raise RuntimeError("Invalid identifiers are provided.")
        else:
            raise RuntimeError("Storage is closed.")

    def infer_topology_by_rid(self, ids: AnyGenericIdentifier):
        """Quickly infers topology from tree node map.

        Parameters
        ----------
        ids
            Tips to keep.

        Returns
        -------
            Pruned reference phylogenetic tree.
        """
        if self.storage_manager.state == 1:
            target_ids = np.unique(np.asarray(ids))
            if self.xrid.isin(target_ids).sum() == len(target_ids):
                repseq_ids = list(map(str, target_ids))
                tree_map_df, root_node_name = self.__make_tree_map_by_rid(repseq_ids)
                tmp_tree = self.__infer_tree_for_rids(
                    tree_map_df, root_node_name, repseq_ids
                )
                return PhyloTree(
                    self.__fix_mapped_tree_nodes(tmp_tree, root_node_name, repseq_ids)
                )
            else:
                raise RuntimeError("Invalid identifiers are provided.")
        else:
            raise RuntimeError("Storage is closed.")

    @staticmethod
    def __infer_tree_for_tids(
        preceding_list_dict: dict, root_node_name: str
    ) -> ete3.Tree:
        """Infer reference tree for :term:`tids` as tips`.

        Parameters
        ----------
        preceding_list_dict
            Preceding lineage map.
        root_node_name
            Tree root name

        Returns
        -------
            Inferred tree
        """
        existing_nodes_dict = defaultdict(ete3.Tree)
        tmp_tree = ete3.Tree(name=root_node_name)
        existing_nodes_dict[root_node_name] = tmp_tree
        for tip_lineage_map in preceding_list_dict.values():
            last_node = tmp_tree
            for lineage_taxon_name in tip_lineage_map:
                if lineage_taxon_name in existing_nodes_dict.keys():
                    last_node = existing_nodes_dict[lineage_taxon_name]
                else:
                    new_node = last_node.add_child(name=lineage_taxon_name)
                    last_node = new_node
                    existing_nodes_dict[lineage_taxon_name] = new_node
        return tmp_tree

    # FIX THIS
    @staticmethod
    def __infer_tree_for_rids(
        tree_map_df: pd.DataFrame,
        root_node_name: str,
        tip_ids: AnyGenericIdentifier,
    ) -> ete3.Tree:
        """Infer reference tree for :term:`rids` as tips.

        Parameters
        ----------
        tree_map_df
            Reference tree map
        root_node_name
            Tree root node name
        tip_ids
            Tip ids (:term:`rids`)

        Returns
        -------
            Inferred tree.
        """
        lineage_map_list = list(tree_map_df.values)
        lineage_map_list_fixed = []
        for lineage_map_list_elem in lineage_map_list:
            taxon_elem_seen = set()
            tmp_lineage_map_list_elem_unique_ordered = [
                elem
                for elem in lineage_map_list_elem
                if not (elem in taxon_elem_seen or taxon_elem_seen.add(elem))
            ]
            lineage_map_list_fixed.append(tmp_lineage_map_list_elem_unique_ordered)
        tmp_tree = ete3.Tree(name=root_node_name)

        for tip_lineage_map in lineage_map_list_fixed:
            last_node = tmp_tree
            for lineage_taxon_name in tip_lineage_map:
                try:
                    existing_nodes = next(
                        tmp_tree.iter_search_nodes(name=lineage_taxon_name)
                    )
                except StopIteration:
                    existing_nodes = None
                except:
                    raise
                if existing_nodes is not None:
                    last_node = existing_nodes
                else:
                    last_node = last_node.add_child(name=lineage_taxon_name)
        return tmp_tree

    def __make_tree_map_by_rid(self, repseq_ids):
        tree_map = self.storage_manager.retrieve_data_by_element("map-tree")
        non_roots_indices = tree_map[tree_map["pid"].notna()].index
        top_level_uid = tree_map[
            ~tree_map.index.isin(non_roots_indices)
        ].index.values.tolist()[0]
        if tree_map is not None:
            taxon_level = 1
            existing_ids = tree_map.index[tree_map.index.isin(repseq_ids)].values
            pid_map_df = (
                tree_map.loc[existing_ids]["pid"]
                .reset_index()
                .reindex(columns=["pid", "uid"])
                .rename(columns={"pid": taxon_level, "uid": 0})
            )
            top_level = False
            while not top_level:
                taxon_level = taxon_level + 1
                tmp_level_map = tree_map.loc[pid_map_df[taxon_level - 1]]["pid"]
                if tmp_level_map.isna().any():
                    tmp_level_map.fillna(top_level_uid, inplace=True)
                pid_map_df.set_index(taxon_level - 1, inplace=True)
                tmp_level_map.rename(taxon_level, inplace=True)
                pid_map_df.loc[:, taxon_level] = tmp_level_map
                pid_map_df.reset_index(inplace=True)
                if tmp_level_map.nunique() == 1:
                    if tmp_level_map.iloc[0] == top_level_uid:
                        top_level = True
            pid_map_df = pid_map_df.reindex(
                sorted(pid_map_df.columns, reverse=True), axis=1
            )
            pid_map_df.drop(taxon_level, axis=1, inplace=True)
            return pid_map_df, top_level_uid

    def __make_aligned_lineage_maps(
        self, tree_map_df: pd.DataFrame, repseq_map: pd.DataFrame
    ) -> Tuple[dict, dict]:
        """Creates a lineage map dataframe to use for tree inferring.

        Parameters
        ----------
        tree_map_df
            Original tree map :class:`~pandas.DataFrame` retrieved from storage
        repseq_map
            Original repseq map :class:`~pandas.DataFrame` retrieved from storage

        Returns
        -------
            (Node preceding lineage map, node following lineage maps)
        """
        total_levels = tree_map_df.shape[1]
        mca_preceding_lineage_dict = defaultdict(list)
        mca_following_aligned_df_dict = defaultdict(pd.DataFrame)

        def adjust_unique(rid_row):
            unique_rid = rid_row.unique()
            return np.concatenate(
                (unique_rid, np.array([None] * (total_levels - len(unique_rid))))
            )

        for tid, rid_list in repseq_map.items():
            tid_str = str(tid)
            tmp_pid_map_df = tree_map_df[tree_map_df[0].isin(list(map(str, rid_list)))]
            if len(rid_list) > 1:
                tmp_pid_map_df_adjusted = tmp_pid_map_df.apply(
                    adjust_unique, axis=1, result_type="broadcast"
                )
                mca_level = (
                    np.argmax(
                        ~tmp_pid_map_df_adjusted.apply(
                            lambda level_col: level_col.duplicated(keep=False), axis=0
                        )
                        .all(axis=0)
                        .values
                    )
                    - 1
                )
                tmp_preceding = tmp_pid_map_df_adjusted.iloc[
                    0, :mca_level
                ].values.tolist() + [tid_str]
                tmp_following = tmp_pid_map_df_adjusted.iloc[:, mca_level:]
                tmp_following_adj = tmp_following.loc[
                    :, ~tmp_following.isnull().all(axis=0)
                ]
                mca_preceding_lineage_dict[tid_str].extend(tmp_preceding)
                mca_following_aligned_df_dict[tid_str] = tmp_following_adj
            else:
                mca_preceding_lineage_dict[tid_str].extend(
                    tmp_pid_map_df.iloc[0, :].unique()[:-1].tolist() + [tid_str]
                )
        return mca_preceding_lineage_dict, mca_following_aligned_df_dict

    @staticmethod
    def __make_tree_node_from_aligned_df(
        aligned_df: pd.DataFrame, root_name: str
    ) -> ete3.Tree:
        """Creates a tree node from alignment.

        Parameters
        ----------
        aligned_df
            Lineage map dataframe
        root_name
            Root name for created node

        Returns
        -------
            Node created from lineage dataframe
        """
        nodes_dict = defaultdict(ete3.Tree)
        tmp_tree = ete3.Tree(name=root_name)
        nodes_dict[root_name] = tmp_tree
        for _, lineage_id_map in aligned_df.iterrows():
            last_node = tmp_tree
            for node_id in lineage_id_map:
                if node_id is None:
                    break
                elif node_id in nodes_dict.keys():
                    last_node = nodes_dict[node_id]
                else:
                    new_node = last_node.add_child(name="r{}".format(node_id))
                    last_node = new_node
                    nodes_dict[node_id] = new_node
        return tmp_tree

    def __infer_tree_for_tids_with_rids(
        self, preceding_list_dict: dict, following_df_dict: dict, root_node_name: str
    ) -> ete3.Tree:
        """Infer reference tree from tree map for :term:`tids` without dropping
        :term:`rids`

        Parameters
        ----------
        preceding_list_dict
           Preceding lineage map
        following_df_dict
            Following lineage map
        root_node_name
            Root node name

        Returns
        -------
            Inferred tree

        """
        nodes_dict = defaultdict(ete3.Tree)
        tmp_tree = ete3.Tree(name=root_node_name)
        nodes_dict[root_node_name] = tmp_tree
        for lineage_id_list in preceding_list_dict.values():
            last_node = tmp_tree
            for node_id in lineage_id_list:
                if node_id in nodes_dict.keys():
                    last_node = nodes_dict[node_id]
                else:
                    last_node = last_node.add_child(name=node_id)
                    nodes_dict[node_id] = last_node

        tmp_tree.prune(preceding_list_dict.keys(), preserve_branch_length=True)

        for tid, lineage_id_df in following_df_dict.items():
            if tid in nodes_dict.keys():
                tid_node = nodes_dict[tid]
                parent_node = tid_node.up
                parent_node.remove_child(tid_node)
                new_tid_node = self.__make_tree_node_from_aligned_df(lineage_id_df, tid)
                parent_node.add_child(new_tid_node)

        return tmp_tree
