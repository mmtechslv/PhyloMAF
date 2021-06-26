from pmaf.pipe.agents.dockers._metakit import DockerPhylogenyMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
import numpy as np
from pmaf.phylo.tree._tree import PhyloTree
from typing import Optional, Union, Any, Dict


class DockerPhylogenyMedium(DockerPhylogenyMetabase, DockerBase):
    """The :term:`docker` class responsible for handling phylogeny data."""
    _UNIT_TYPES = (PhyloTree, type(None))

    def __init__(
        self,
        trees: Union[list, dict, "DockerPhylogenyMedium"],
        ignore_tips=False,
        **kwargs: Any
    ):
        """Constructor.

        Parameters
        ----------
        trees
            List-like or dict-like like phylogeny data where values are either
            phylo-trees with types :attr:`.UNIT_TYPE` (singleton) or instances of :class:`.DockerPhylogenyMedium`
        ignore_tips
            If True do not raise error when tips are not unique
        kwargs
            Compatibility
        """
        if isinstance(trees, list):
            tmp_trees = {k: v for k, v in enumerate(trees)}
        elif isinstance(trees, dict):
            tmp_trees = trees
        else:
            tmp_trees = {kwargs.get("name", 0): trees}
        container_mode_test = any(
            [isinstance(data_elem, type(self)) for data_elem in tmp_trees.values()]
        )
        if not container_mode_test:
            if len(tmp_trees) > 1:
                raise ValueError(
                    "DockerPhylogenyMedium can only contain 1 tree at singleton mode"
                )
            tmp_adj_trees = dict.fromkeys(tmp_trees.keys())
            for ix, tree in tmp_trees.items():
                if isinstance(tree, self._UNIT_TYPES):
                    if tree is not None:
                        if tree.total_nodes > 0:
                            tmp_tree_elem = tree
                        else:
                            raise ValueError("Provided `tree` has no nodes")
                    else:
                        tmp_tree_elem = None
                else:
                    tmp_tree_elem = PhyloTree(tree, copy=False)
                if tmp_tree_elem is not None:
                    tmp_tip_ids = tmp_tree_elem.tip_names
                    if (
                        len(tmp_tip_ids) != len(list(set(tmp_tip_ids)))
                    ) and not ignore_tips:
                        raise ValueError("Tree tips must have unique names.")
                tmp_adj_trees[ix] = tmp_tree_elem
        else:
            tmp_adj_trees = tmp_trees
        super().__init__(
            _data_dict=tmp_adj_trees, _valid_types=self._UNIT_TYPES, **kwargs
        )
        self.__ignore_tips = bool(ignore_tips)

    def get_tip_names(
        self, indices: Optional[np.ndarray] = None, dtype: Optional[str] = None
    ) -> Union[dict, np.ndarray]:
        """Get tip labels/names of the phylogenetic tree.

        Parameters
        ----------
        indices
            Target indices or None for all
        dtype
            Cast to dtype

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`numpy.ndarray`
            if not :term:`singleton` then return dictionary with values :meth:`.get_tip_names`
        """
        if self.singleton:
            tips = next(iter(self.data.values())).tip_names
            if dtype is None:
                return np.asarray(tips)
            else:
                return np.asarray(tips, dtype=dtype)
        else:
            if indices is None:
                target_indices = self.index
            elif np.isscalar(indices):
                target_indices = np.asarray([indices])
            else:
                target_indices = np.asarray(indices)
            if not np.isin(target_indices, self.index).all():
                raise ValueError("`indices` are invalid.")
            return {
                ix: self.data[ix].get_tip_names(dtype=dtype)
                for ix in target_indices
                if self.data[ix] is not None
            }

    def get_node_names(
        self,
        indices: Optional[np.ndarray] = None,
        dtype: Optional[str] = None,
        include_missing: bool = False,
    ) -> Union[dict, np.ndarray]:
        """Get node labels/names of the phylogenetic tree.

        Parameters
        ----------
        indices
            Target indices or None for all
        dtype
            Cast to dtype
        include_missing
            Include names/labels with None value

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`numpy.ndarray`
            if not :term:`singleton` then return dictionary with values :meth:`.get_node_names`
        """
        if self.singleton:
            tmp_nodes = next(iter(self.data.values())).node_names
            if not include_missing:
                nodes = [node for node in tmp_nodes if node != ""]
            else:
                nodes = tmp_nodes
            if dtype is None:
                return np.asarray(nodes)
            else:
                return np.asarray(nodes, dtype=dtype)
        else:
            if indices is None:
                target_indices = self.index
            elif np.isscalar(indices):
                target_indices = np.asarray([indices])
            else:
                target_indices = np.asarray(indices)
            if not np.isin(target_indices, self.index).all():
                raise ValueError("`indices` are invalid.")
            return {
                ix: self.data[ix].get_node_names(
                    dtype=dtype, include_missing=include_missing
                )
                for ix in target_indices
                if self.data[ix] is not None
            }

    def get_tree(
        self, indices: Optional[np.ndarray] = None, exclude_missing: bool = False
    ) -> Union[PhyloTree, Dict[Union[str, int], Optional[PhyloTree]]]:
        """Get the phylogenetic tree instance.

        Parameters
        ----------
        indices
            Target indices or None for all
        exclude_missing
            Exclude missing data

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`.PhyloTree`
            if not :term:`singleton` then return dictionary with values :meth:`.get_tree`
        """
        if self.singleton:
            return next(iter(self.data.values()))
        else:
            if indices is None:
                target_indices = self.index
            elif np.isscalar(indices):
                target_indices = np.asarray([indices])
            else:
                target_indices = np.asarray(indices)
            if exclude_missing:
                target_indices = np.asarray(
                    [ix for ix in target_indices if self.data[ix] is not None]
                )
            if not np.isin(target_indices, self.index).all():
                raise ValueError("`indices` are invalid.")
            tmp_trees_dict = dict.fromkeys(target_indices, None)
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_trees_dict[ix] = self.data[ix].get_tree(
                        exclude_missing=exclude_missing
                    )
            return tmp_trees_dict
