from abc import ABC, abstractmethod


class DatabaseBackboneMetabase(ABC):
    def __init__(self, storage_hdf5_fp, **kwargs):
        pass

    @abstractmethod
    def close(self):
        pass

    @classmethod
    @abstractmethod
    def build_database_storage(cls, **kwargs):
        pass

    @abstractmethod
    def find_rid_by_tid(self, ids, subs, iterator, flatten, mode):
        pass

    @abstractmethod
    def find_tid_by_rid(self, ids, levels, flatten, method, mode):
        pass

    def find_sub_tids_by_tid(self, ids, ter_rank, flatten, mode):
        pass

    @abstractmethod
    def take_tids_by_rank(self, levels, iterator, flatten, mode):
        pass

    @abstractmethod
    def take_rids_by_rank(self, levels, iterator, flatten, mode):
        pass

    @abstractmethod
    def get_stats_by_rid(self, ids, include, exclude):
        pass

    @abstractmethod
    def get_stats_by_tid(self, ids, include, exclude):
        pass

    @property
    @abstractmethod
    def xtid(self):
        pass

    @property
    @abstractmethod
    def xrid(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamp(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @property
    @abstractmethod
    def summary(self):
        pass

    @property
    @abstractmethod
    def storage_manager(self):
        pass

    @property
    @abstractmethod
    def avail_ranks(self):
        pass


class DatabasePhylogenyMetabase(DatabaseBackboneMetabase):
    @abstractmethod
    def prune_tree_by_tid(self, ids):
        pass

    @abstractmethod
    def infer_topology_by_tid(self, ids):
        pass

    @abstractmethod
    def prune_tree_by_rid(self, ids):
        pass

    @abstractmethod
    def infer_topology_by_rid(self, ids):
        pass


class DatabaseTaxonomyMetabase(DatabaseBackboneMetabase):
    @abstractmethod
    def get_lineage_by_tid(self, ids, missing_rank, desired_ranks, drop_ranks):
        pass

    @abstractmethod
    def get_lineage_by_rid(self, ids, missing_rank, desired_ranks, drop_ranks):
        pass

    @abstractmethod
    def get_taxonomy_by_tid(self, ids, levels):
        pass

    @abstractmethod
    def get_taxonomy_by_rid(self, ids, levels, result_format):
        pass

    @abstractmethod
    def get_taxonomy_by_rank(self, levels):
        pass


class DatabaseAccessionMetabase(DatabaseBackboneMetabase):
    @abstractmethod
    def get_accession_by_tid(self, ids, **kwargs):
        pass

    @abstractmethod
    def get_accession_by_rid(self, ids, **kwargs):
        pass


class DatabaseSequenceMetabase(DatabaseBackboneMetabase):
    @abstractmethod
    def get_sequence_by_tid(self, ids, **kwargs):
        pass

    @abstractmethod
    def get_sequence_by_rid(self, ids, **kwargs):
        pass

    @abstractmethod
    def get_alignment_by_tid(self, ids, **kwargs):
        pass

    @abstractmethod
    def get_alignment_by_rid(self, ids, **kwargs):
        pass
