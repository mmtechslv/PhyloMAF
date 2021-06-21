import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
import pandas as pd
import numpy as np
from pmaf.phylo.tree._tree import PhyloTree
from pmaf.phylo.tree._backends import TreeEte3Base
from io import StringIO
from typing import Union, Optional, Tuple, Any
from pmaf.internal._typing import AnyGenericIdentifier, Mapper


class RepPhylogeny(EssentialBackboneBase, EssentialFeatureMetabase):
    """An `essential` class for handling phylogeny data."""

    def __init__(
        self,
        tree: Union[PhyloTree, TreeEte3Base, StringIO, str],
        feature_ids: Optional[AnyGenericIdentifier] = None,
        prune: bool = False,
        annotation: Union[dict, pd.Series, None] = None,
        copy: bool = True,
        ignore_polytomy: bool = False,
        **kwargs: Any
    ) -> None:
        """Constructor for :class:`.RepPhylogeny`

        Parameters
        ----------
        tree
            Phylogeny data
        feature_ids
            Target feature identifiers
        prune
            Whether to prune for `feature_ids`
        annotation
            Annotations for tips
        copy
            Whether to copy the original tree. May require long time if tree is large.
        ignore_polytomy
            Whether to resolve tree polytomy or not.
        kwargs
            Compatibility
        """
        super().__init__(**kwargs)
        if feature_ids is None:
            tmp_feature_ids = np.asarray([])
        else:
            tmp_feature_ids = np.asarray(feature_ids)
            if len(np.unique(tmp_feature_ids)) < len(tmp_feature_ids):
                raise ValueError("`feature_ids` cannot contain duplicates.")
        if annotation is not None:
            if isinstance(annotation, dict):
                tmp_annotation = annotation
            elif isinstance(annotation, pd.Series):
                tmp_annotation = annotation.to_dict()
            else:
                raise TypeError("`annotation` can be None or dict-like")
        else:
            tmp_annotation = {}
        if isinstance(tree, PhyloTree):
            if tree.total_nodes > 0:
                tmp_tree = tree.copy() if copy else tree
            else:
                raise ValueError("Provided `tree` has no nodes")
        else:
            tmp_tree = PhyloTree(tree, copy=copy)
        tmp_node_names = tmp_tree.node_names
        tmp_feature_ids_adj = [type(tmp_node_names[0])(fid) for fid in tmp_feature_ids]
        if len(tmp_feature_ids_adj) > 0:
            if all(
                [feature_id in tmp_node_names for feature_id in tmp_feature_ids_adj]
            ):
                tmp_tip_ids = tmp_feature_ids_adj
            else:
                raise ValueError(
                    "Some ids in `feature_ids` are not present in `tree` nodes."
                )
        else:
            tmp_tip_ids = tmp_tree.tip_names
        if len(tmp_tip_ids) != len(list(set(tmp_tip_ids))):
            raise ValueError("Tree tips must have unique names.")
        if prune and len(tmp_feature_ids_adj) > 0:
            tmp_tree.prune_by_ids(tmp_tip_ids)
        if len(tmp_annotation) > 0:
            tmp_annotation_adj = {
                type(tmp_tip_ids[0])(k): v for k, v in tmp_annotation.items()
            }
            if not all([tip_id in tmp_annotation_adj.keys() for tip_id in tmp_tip_ids]):
                raise ValueError(
                    "Some indices in `annotation` are not present in `tree` nodes."
                )
        else:
            tmp_annotation_adj = {}
        tmp_tree.sort_by_name()
        tmp_tree.clear_internal_node_names()
        if not ignore_polytomy:
            tmp_tree.resolve_polytomy()
        self.__feature_ids = np.asarray(tmp_tip_ids)
        self.__feature_ids_dtype = self.__feature_ids.dtype
        # PhyloTree class uses ete3 trees, which work unstable when tips are not
        # strings. Therefore, dtype of internal `__feature_ids` and external `xrid`
        # are kept different.
        self.__internal_tree = tmp_tree
        self.__annotations = tmp_annotation_adj

    def _remove_features_by_id(
        self, ids: AnyGenericIdentifier, **kwargs: Any
    ) -> Optional[AnyGenericIdentifier]:
        """Remove features by feature ids and ratify action.

        Parameters
        ----------
        ids
            Feature identifiers
        **kwargs
            Compatibility

        Returns
        -------
        """
        tmp_ids = np.asarray(ids).astype(self.__feature_ids.dtype)

        if len(tmp_ids) > 0:
            for node_name in tmp_ids:
                self.__internal_tree.remove_node_by_name(str(node_name))
        self.__feature_ids = np.asarray(
            [fid for fid in self.__feature_ids if fid not in tmp_ids]
        )
        return self._ratify_action("_remove_features_by_id", ids, **kwargs)

    def _merge_features_by_map(
        self,
        map_dict: Mapper,
        _annotations: Union[dict, pd.Series, None] = None,
        **kwargs: Any
    ) -> Optional[Mapper]:
        """Merge features by map..

        Parameters
        ----------
        map_dict
            Map to use for merging
        _annotations
            New annotations to passed to
            `essential` class :class:`~pmaf.biome.essentials._taxonomy.RepTaxonomy`
        **kwargs
            Compatibility
        """
        new_tips = []
        for new_id, group in map_dict.items():
            tmp_new_name = str(new_id)
            new_tips.append(tmp_new_name)
            if len(group) > 1:
                tmp_new_node = self.__internal_tree.merge_nodes(list(map(str, group)))
            else:
                tmp_new_node = self.__internal_tree.get_node_by_name(str(group[0]))
            tmp_new_node.name = tmp_new_name
        self.__feature_ids_dtype = type(list(map_dict.keys())[0])
        self.__internal_tree.prune_by_ids(new_tips)
        self.__annotations = (
            {str(tid): annot for tid, annot in _annotations.items()}
            if _annotations is not None
            else {}
        )
        self.__feature_ids = np.array(new_tips, dtype=str)
        return self._ratify_action(
            "_merge_features_by_map", map_dict, _annotations=_annotations, **kwargs
        )

    def __make_annotated_tree(self) -> PhyloTree:
        """Create an original tree with annotated tips.

        Returns:
            Annotated tree of class :class:`~pmaf.phylo.tree._tree.PhyloTree`
        """
        tmp_annotated_tree = self.__internal_tree.copy()
        tmp_annotated_tree.annotate_nodes_by_map(self.__annotations, only_tips=True)
        tmp_annotated_tree.sort_by_name()
        return tmp_annotated_tree

    def get_annotated_tree(self) -> PhyloTree:
        """Retrieves annotated tree.

        Returns
        -------
        Annotated tree of class
            class:`~pmaf.phylo.tree.PhyloTree`
        """
        if len(self.__annotations) > 0:
            return self.__make_annotated_tree()
        else:
            raise RuntimeError("Annotations are not present.")

    def resolve_polytomy(self) -> None:
        """Resolve tree polytomy."""
        self.__internal_tree.resolve_polytomy()

    def render_art(self, output_fp: str, annotated: bool = False) -> Any:
        """Renders tree into file.

        Parameters
        ----------
        output_fp
            File to render into. File format depends on the extension.
            For example, .pdf will produce PDF file and
            while .png will produce PNG file.
        annotated
            Whether to create tree with annotated tips or not.
        """
        if annotated:
            if len(self.__annotations) > 0:
                return self.__make_annotated_tree().render(output_fp)
            else:
                raise RuntimeError("Annotations are not present.")
        else:
            return self.__internal_tree.render(output_fp)

    def get_ascii_art(self, annotated: bool = False) -> str:
        """Creates ASCII art of the tree.

        Parameters
        ----------
        annotated :
            Whether to create tree with annotated tips or not.
        annotated: bool :
             (Default value = False)

        Returns
        -------
            String with ASCII art
        """
        if annotated:
            if len(self.__annotations) > 0:
                return self.__make_annotated_tree().get_ascii_art()
            else:
                raise RuntimeError("Annotations are not present.")
        else:
            return self.__internal_tree.get_ascii_art()

    def _export(
        self, rooted: bool = False, annotated: bool = False, **kwargs: Any
    ) -> Tuple[str, dict]:
        """Creates the Newick formatted tree for export.

        Parameters
        ----------
        rooted :
            Whether to create rooted tree or not.
        annotated :
            Whether to create tree with annotated tips or not.
        **kwargs :
            Compatibility.
        """
        if annotated:
            if len(self.__annotations) > 0:
                return (
                    self.__make_annotated_tree().get_newick_str(
                        root_node=rooted, quoted_nodes=True, **kwargs
                    ),
                    kwargs,
                )
            else:
                raise RuntimeError("Annotations are not present.")
        else:
            return (
                self.__internal_tree.get_newick_str(
                    root_node=rooted, quoted_nodes=False, **kwargs
                ),
                kwargs,
            )

    def export(self, output_fp: str, _add_ext: bool = False, **kwargs: Any) -> None:
        """Exports the Newick formatted phylogenetic tree into specified file.

        Parameters
        ----------
        output_fp :
            Export filepath
        _add_ext :
            Add file extension or not.
        **kwargs :
            Compatibility
        """
        tmp_export, _ = self._export(**kwargs)
        if _add_ext:
            tmp_filepath = "{}.tre".format(output_fp)

        else:
            tmp_filepath = output_fp
        with open(tmp_filepath, "w") as output:
            output.write(tmp_export)

    def copy(self) -> "RepPhylogeny":
        """Copy of the instance."""
        return type(self)(
            tree=self.__internal_tree,
            feature_ids=self.__feature_ids,
            annotation=self.__annotations,
            copy=True,
            metadata=self.metadata,
            name=self.name,
        )

    def get_subset(
        self, rids: Optional[AnyGenericIdentifier] = None, *args, **kwargs: Any
    ) -> "RepPhylogeny":
        """Get subset of the :class:`.RepPhylogeny`.

        Parameters
        ----------
        rids :
            Feature Identifiers
        *args :
            Compatibility
        **kwargs :
            Compatibility

        Returns
        -------
            Instance of class:`.RepPhylogeny`.
        """
        if rids is None:
            target_rids = self.__feature_ids
        else:
            target_rids = np.asarray(rids).astype(str)
        if not np.isin(self.__feature_ids, target_rids).sum() == len(target_rids):
            raise ValueError("Invalid feature ids are provided.")
        tmp_tree = self.__internal_tree.copy()
        tmp_tree.prune_by_ids(target_rids)
        return type(self)(
            tree=tmp_tree,
            feature_ids=self.__feature_ids,
            annotation=self.__annotations,
            copy=True,
            metadata=self.metadata,
            name=self.name,
        )

    def write(self, output_fp: str, mode: str = "w", **kwargs: Any) -> None:
        """Writes the Newick tree into specified file.

        Parameters
        ----------
        output_fp :
            Output filepath
        mode :
            File write mode.
        **kwargs :
            Compatibility
        """

        tmp_export, _ = self._export(**kwargs)
        with open(output_fp, mode) as output:
            output.write(tmp_export)

    @property
    def data(self) -> PhyloTree:
        """Phylogenetic Tree."""
        return self.__internal_tree

    @property
    def annotations(self) -> dict:
        """Tip Annotations."""
        return self.__annotations

    @property
    def xrid(self) -> AnyGenericIdentifier:
        """Feature identifiers."""
        return pd.Index(self.__feature_ids).astype(self.__feature_ids_dtype)
