from ._metakit import PhyloTreeMetabase
from ._backends import TreeEte3Base
from os import path
from io import StringIO
import pandas as pd
from skbio import TreeNode as skbioTreeNode

class PhyloTree(PhyloTreeMetabase):
    ''' '''
    def __init__(self,tree,tree_format='newick',copy=False):
        if isinstance(tree, StringIO):
            tmp_bke_tree =  TreeEte3Base(tree.read(),'newick-str',copy)
        elif isinstance(tree,str):
            if path.isfile(tree):
                tmp_bke_tree =  TreeEte3Base(tree,'newick-fp',copy)
            else:
                tmp_bke_tree = TreeEte3Base(tree, 'newick-str',copy)
        elif isinstance(tree,PhyloTreeMetabase):
            tmp_bke_tree = TreeEte3Base(tree._backend, 'object',copy)
        else:
            tmp_bke_tree = TreeEte3Base(tree, 'object',copy)
        self.__backend = tmp_bke_tree
        self.__total_nodes = tmp_bke_tree.count()
        self.__total_internal_nodes = len(tmp_bke_tree.get_internal_nodes())
        self.__total_tips = len(tmp_bke_tree.get_tips())
        return

    def __repr__(self):
        class_name = self.__class__.__name__
        backend_name = self.__backend.name
        total_nodes = str(self.__total_nodes)
        total_tips = str(self.__total_tips)
        repr_str = "<{}:[{}], Nodes:[{}], Tips:[{}]>".format(class_name, backend_name, total_nodes, total_tips)
        return repr_str

    @property
    def internal_node_names(self):
        ''' '''
        return self.__backend.get_internal_nodes(True)

    @property
    def internal_nodes(self):
        ''' '''
        return self.__backend.get_internal_nodes()

    @property
    def nodes(self):
        ''' '''
        return self.__backend.get_nodes()

    @property
    def node_names(self):
        ''' '''
        return self.__backend.get_nodes(True)

    @property
    def tips(self):
        ''' '''
        return self.__backend.get_tips()

    @property
    def tip_names(self):
        ''' '''
        return self.__backend.get_tips(True)

    def write(self, tree_fp,**kwargs):
        '''

        Args:
          tree_fp: 
          **kwargs: 

        Returns:

        '''
        return self.__backend.write_newick(tree_fp, **kwargs)

    def to_skbio(self,rooted=False):
        '''

        Args:
          rooted: (Default value = False)

        Returns:

        '''
        return skbioTreeNode.read(StringIO(self.__backend.get_string(tree_format=1, root_node=rooted,output_format='newick')))

    def get_newick_str(self,**kwargs):
        '''

        Args:
          **kwargs: 

        Returns:

        '''
        return self.__backend.get_string(output_format='newick',**kwargs)

    def ladderize(self):
        ''' '''
        self.__backend.ladderize()

    def unroot(self):
        ''' '''
        return self.__backend.unroot()

    def sort_by_name(self):
        ''' '''
        return self.__backend.sort()

    def render(self, output_fp):
        '''

        Args:
          output_fp: 

        Returns:

        '''
        return self.__backend.make_tree_art(output_fp)

    def get_ascii_art(self):
        ''' '''
        return self.__backend.get_ascii_art()

    def resolve_polytomy(self):
        ''' '''
        return self.__backend.resolve_polytomy()

    def clear_internal_node_names(self):
        ''' '''
        internal_nodes = self.__backend.get_internal_nodes()
        for node in internal_nodes:
            node.name = ''

    def copy(self):
        ''' '''
        return type(self)(self.__backend.engine,copy=True)

    def prune_by_ids(self, node_ids):
        '''

        Args:
          node_ids: 

        Returns:

        '''
        all_nodes = self.__backend.get_nodes()
        target_nodes = [node for node in all_nodes if node.name in node_ids]
        return self.__backend.prune_for_ids(set(target_nodes))

    def annotate_nodes_by_map(self, node_mapping, only_tips=False):
        '''

        Args:
          node_mapping: 
          only_tips: (Default value = False)

        Returns:

        '''
        if isinstance(node_mapping,pd.Series):
            return self.__backend.add_str_node_names(node_mapping.to_dict(),only_tips)
        elif isinstance(node_mapping,dict):
            return self.__backend.add_str_node_names(node_mapping,only_tips)
        else:
            raise TypeError('`node_mapping` must be dict-like.')

    def replace_nodes_by_map(self, node_mapping,only_tips=False):
        '''

        Args:
          node_mapping: 
          only_tips: (Default value = False)

        Returns:

        '''
        if isinstance(node_mapping,pd.Series):
            return self.__backend.replace_node_names(node_mapping.to_dict(),only_tips)
        elif isinstance(node_mapping,dict):
            return self.__backend.replace_node_names(node_mapping,only_tips)
        else:
            raise TypeError('`node_mapping` must be dict-like.')

    def get_node_by_name(self,node_name):
        '''

        Args:
          node_name: 

        Returns:

        '''
        return self.__backend.find_node_by_name(node_name)

    def remove_node_by_name(self,node_name):
        '''

        Args:
          node_name: 

        Returns:

        '''
        if node_name in self.__backend.get_nodes(True):
            node_to_remove = self.__backend.find_node_by_name(node_name)
            return self.__backend.detach_node(node_to_remove)
        else:
            raise ValueError('Node with given name does not exist.')

    def remove_node(self,node):
        '''

        Args:
          node: 

        Returns:

        '''
        if node in self.__backend.get_nodes():
            node_to_remove = self.__backend.find_node_by_name(node)
            return self.__backend.detach_node(node_to_remove)
        else:
            raise ValueError('Node with given name does not exist.')

    def get_mcra_for_nodes(self,node_names):
        '''

        Args:
          node_names: 

        Returns:

        '''
        if pd.api.types.is_list_like(node_names):
            all_nodes = self.__backend.get_nodes()
            target_nodes = [node for node in all_nodes if node.name in node_names]
            return self.__backend.get_mcra_node_for_nodes(target_nodes)
        else:
            raise TypeError('`node_names` must be list-like.')

    def merge_nodes(self,tip_names):
        '''

        Args:
          tip_names: 

        Returns:

        '''
        if pd.api.types.is_list_like(tip_names):
            all_tips = self.__backend.get_tips()
            target_tips = [tip for tip in all_tips if tip.name in tip_names]
            exluded_tips = [tip for tip in all_tips if tip.name not in tip_names]
            avg_dist = sum([node.dist for node in target_tips])/len(target_tips)
            tmp_mrca = self.__backend.get_mcra_node_for_nodes(target_tips)
            tmp_merged_tip = tmp_mrca.add_child(dist=avg_dist)
            tmp_mrca.prune([tmp_merged_tip]+exluded_tips,preserve_branch_length=True)
            return tmp_merged_tip
        else:
            raise TypeError('`node_names` must be list-like.')

    @property
    def _backend(self):
        ''' '''
        return self.__backend.engine

    @property
    def total_nodes(self):
        ''' '''
        return self.__total_nodes

    @property
    def total_internal_nodes(self):
        ''' '''
        return self.__total_internal_nodes

    @property
    def total_tips(self):
        ''' '''
        return self.__total_tips








