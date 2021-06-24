from abc import ABC,abstractmethod

class PhyloTreeMetabase(ABC):
    @abstractmethod
    def get_ascii_art(self):
        pass

    @abstractmethod
    def write(self, tree_fp, tree_format,root_node, output_format):
        pass

    @abstractmethod
    def unroot(self):
        pass

    @abstractmethod
    def sort_by_name(self):
        pass

    @abstractmethod
    def render(self, output_fp):
        pass

    @abstractmethod
    def prune_by_ids(self, ids):
        pass

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def annotate_nodes_by_map(self, node_mapping,only_tips):
        pass

    @abstractmethod
    def replace_nodes_by_map(self, node_mapping,only_tips):
        pass

    @property
    @abstractmethod
    def _backend(self):
        pass

    @property
    @abstractmethod
    def total_nodes(self):
        pass

    @property
    @abstractmethod
    def total_internal_nodes(self):
        pass

    @property
    @abstractmethod
    def total_tips(self):
        pass

    @property
    @abstractmethod
    def internal_node_names(self):
        pass

    @property
    @abstractmethod
    def internal_nodes(self):
        pass

    @property
    @abstractmethod
    def nodes(self):
        pass

    @property
    @abstractmethod
    def node_names(self):
        pass

    @property
    @abstractmethod
    def tips(self):
        pass

    @property
    @abstractmethod
    def tip_names(self):
        pass
