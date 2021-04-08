import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
import pandas as pd
import numpy as np
from pmaf.phylo.tree._tree import PhyloTree

class RepPhylogeny(EssentialBackboneBase, EssentialFeatureMetabase):
    def __init__(self, tree, feature_ids=None, prune=False, annotation=None, copy=True, ignore_polytomy=False,**kwargs):
        super().__init__(**kwargs)
        if feature_ids is None:
            tmp_feature_ids = np.asarray([])
        else:
            tmp_feature_ids = np.asarray(feature_ids)
            if len(np.unique(tmp_feature_ids)) < len(tmp_feature_ids):
                raise ValueError('`feature_ids` cannot contain duplicates.')
        if annotation is not None:
            if isinstance(annotation, dict):
                tmp_annotation = annotation
            elif isinstance(annotation, pd.Series):
                tmp_annotation = annotation.to_dict()
            else:
                raise TypeError('`annotation` can be None or dict-like')
        else:
            tmp_annotation = {}
        if isinstance(tree, PhyloTree):
            if tree.total_nodes>0:
                    tmp_tree = tree.copy() if copy else tree
            else:
                raise ValueError('Provided `tree` has no nodes')
        else:
            tmp_tree = PhyloTree(tree,copy=copy)
        tmp_node_names = tmp_tree.node_names
        tmp_feature_ids_adj = [type(tmp_node_names[0])(fid) for fid in tmp_feature_ids]
        if len(tmp_feature_ids_adj)>0:
            if all([feature_id in tmp_node_names for feature_id in tmp_feature_ids_adj]):
                tmp_tip_ids = tmp_feature_ids_adj
            else:
                raise ValueError('Some ids in `feature_ids` are not present in `tree` nodes.')
        else:
            tmp_tip_ids = tmp_tree.tip_names
        if len(tmp_tip_ids)!=len(list(set(tmp_tip_ids))):
            raise ValueError('Tree tips must have unique names.')
        if prune and len(tmp_feature_ids_adj)>0:
            tmp_tree.prune_by_ids(tmp_tip_ids)
        if len(tmp_annotation)>0:
            tmp_annotation_adj = {type(tmp_tip_ids[0])(k):v for k,v in tmp_annotation.items()}
            if not all([tip_id in tmp_annotation_adj.keys() for tip_id in tmp_tip_ids]):
                raise ValueError('Some indices in `annotation` are not present in `tree` nodes.')
        else:
            tmp_annotation_adj = {}
        tmp_tree.sort_by_name()
        tmp_tree.clear_internal_node_names()
        if not ignore_polytomy:
            tmp_tree.resolve_polytomy()
        self.__feature_ids = np.asarray(tmp_tip_ids)
        self.__internal_tree = tmp_tree
        self.__annotations = tmp_annotation_adj

    def _remove_features_by_id(self, ids, **kwargs):
        tmp_ids = np.asarray(ids).astype(self.__feature_ids.dtype)
        
        if len(tmp_ids)>0:
            for node_name in tmp_ids:
                self.__internal_tree.remove_node_by_name(str(node_name))
        self.__feature_ids = np.asarray([fid for fid in self.__feature_ids if fid not in tmp_ids])
        return self._ratify_action('_remove_features_by_id', ids, **kwargs)

    def _merge_features_by_map(self, map_dict, _annotations=None, **kwargs):
        new_tips = []
        for new_id, group in map_dict.items():
            tmp_new_name = str(new_id)
            new_tips.append(tmp_new_name)
            if len(group)>1:
                tmp_new_node = self.__internal_tree.merge_nodes(list(map(str,group)))
            else:
                tmp_new_node = self.__internal_tree.get_node_by_name(str(group[0]))
            tmp_new_node.name = tmp_new_name
        self.__internal_tree.prune_by_ids(new_tips)
        self.__annotations = {str(tid):annot for tid,annot in _annotations.items()} if _annotations is not None else {}
        self.__feature_ids = np.array(new_tips,dtype=self.__feature_ids.dtype)
        return self._ratify_action('_merge_features_by_map', map_dict, _annotations=_annotations, **kwargs)

    def __make_annotated_tree(self):
        tmp_annotated_tree = self.__internal_tree.copy()
        tmp_annotated_tree.annotate_nodes_by_map(self.__annotations, only_tips=True)
        tmp_annotated_tree.sort_by_name()
        return tmp_annotated_tree

    def get_annotated_tree(self):
        if len(self.__annotations) > 0:
            return self.__make_annotated_tree()
        else:
            raise RuntimeError('Annotations are not present.')

    def resolve_polytomy(self):
        self.__internal_tree.resolve_polytomy()

    def render_art(self,output_fp,annotated=False):
        if annotated:
            if len(self.__annotations)>0:
                return self.__make_annotated_tree().render(output_fp)
            else:
                raise RuntimeError('Annotations are not present.')
        else:
            return self.__internal_tree.render(output_fp)

    def get_ascii_art(self,annotated=False):
        if annotated:
            if len(self.__annotations)>0:
                return self.__make_annotated_tree().get_ascii_art()
            else:
                raise RuntimeError('Annotations are not present.')
        else:
            return self.__internal_tree.get_ascii_art()

    def _export(self,rooted=False,annotated=False,**kwargs):
        if annotated:
            if len(self.__annotations)>0:
                return self.__make_annotated_tree().get_newick_str(root_node=rooted,quoted_nodes=True,**kwargs), kwargs
            else:
                raise RuntimeError('Annotations are not present.')
        else:
            return self.__internal_tree.get_newick_str(root_node=rooted,quoted_nodes=False,**kwargs), kwargs

    def export(self, output_fp, _add_ext=False, **kwargs):
        tmp_export, _ = self._export(**kwargs)
        if _add_ext:
            tmp_filepath = "{}.tre".format(output_fp)

        else:
            tmp_filepath = output_fp
        with open(tmp_filepath,'w') as output:
            output.write(tmp_export)

    def copy(self):
        return type(self)(tree=self.__internal_tree, feature_ids=self.__feature_ids, annotation=self.__annotations, copy=True, metadata = self.metadata,name=self.name)

    def get_subset(self, rids=None, *args, **kwargs):
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids)
        if not self.xrid.isin(target_rids).sum() == len(target_rids):
            raise ValueError('Invalid feature ids are provided.')
        tmp_tree = self.__internal_tree.copy()
        tmp_tree.prune_by_ids(target_rids.astype(str))
        return type(self)(tree=tmp_tree, feature_ids=self.__feature_ids, annotation=self.__annotations, copy=True, metadata = self.metadata,name=self.name)

    def write(self, output_fp, mode='w',  **kwargs):
        tmp_export,_ = self._export(**kwargs)
        with open(output_fp, mode) as output:
            output.write(tmp_export)

    @property
    def data(self):
        return self.__internal_tree

    @property
    def annotations(self):
        return self.__annotations

    @property
    def xrid(self):
        return pd.Index(self.__feature_ids).astype(int)