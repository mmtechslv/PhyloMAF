from abc import ABC,abstractmethod

class DatabaseBackboneMetabase(ABC):
    """ """
    def __init__(self, storage_hdf5_fp, **kwargs):
        pass

    @abstractmethod
    def close(self):
        """ """
        pass

    @classmethod
    @abstractmethod
    def build_database_storage(cls,**kwargs):
        """

        Parameters
        ----------
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def find_rid_by_tid(self, ids, subs, iterator, flatten, mode):
        """

        Parameters
        ----------
        ids :
            
        subs :
            
        iterator :
            
        flatten :
            
        mode :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def find_tid_by_rid(self, ids, levels, flatten, method, mode):
        """

        Parameters
        ----------
        ids :
            
        levels :
            
        flatten :
            
        method :
            
        mode :
            

        Returns
        -------

        """
        pass

    def find_sub_tids_by_tid(self, ids, ter_rank, flatten, mode):
        """

        Parameters
        ----------
        ids :
            
        ter_rank :
            
        flatten :
            
        mode :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def take_tids_by_rank(self, levels, iterator, flatten, mode):
        """

        Parameters
        ----------
        levels :
            
        iterator :
            
        flatten :
            
        mode :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def take_rids_by_rank(self, levels, iterator, flatten, mode):
        """

        Parameters
        ----------
        levels :
            
        iterator :
            
        flatten :
            
        mode :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_stats_by_rid(self, ids, include, exclude):
        """

        Parameters
        ----------
        ids :
            
        include :
            
        exclude :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_stats_by_tid(self, ids, include, exclude):
        """

        Parameters
        ----------
        ids :
            
        include :
            
        exclude :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def xtid(self):
        """ """
        pass

    @property
    @abstractmethod
    def xrid(self):
        """ """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

    @property
    @abstractmethod
    def stamp(self):
        """ """
        pass

    @property
    @abstractmethod
    def state(self):
        """ """
        pass

    @property
    @abstractmethod
    def summary(self):
        """ """
        pass

    @property
    @abstractmethod
    def storage_manager(self):
        """ """
        pass

    @property
    @abstractmethod
    def avail_ranks(self):
        """ """
        pass

class DatabasePhylogenyMetabase(DatabaseBackboneMetabase):
    """ """
    @abstractmethod
    def prune_tree_by_tid(self, ids):
        """

        Parameters
        ----------
        ids :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def infer_topology_by_tid(self, ids):
        """

        Parameters
        ----------
        ids :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def prune_tree_by_rid(self, ids):
        """

        Parameters
        ----------
        ids :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def infer_topology_by_rid(self, ids):
        """

        Parameters
        ----------
        ids :
            

        Returns
        -------

        """
        pass

class DatabaseTaxonomyMetabase(DatabaseBackboneMetabase):
    """ """
    @abstractmethod
    def get_lineage_by_tid(self, ids, missing_rank, desired_ranks, drop_ranks):
        """

        Parameters
        ----------
        ids :
            
        missing_rank :
            
        desired_ranks :
            
        drop_ranks :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_lineage_by_rid(self, ids, missing_rank, desired_ranks, drop_ranks):
        """

        Parameters
        ----------
        ids :
            
        missing_rank :
            
        desired_ranks :
            
        drop_ranks :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_taxonomy_by_tid(self, ids, levels):
        """

        Parameters
        ----------
        ids :
            
        levels :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_taxonomy_by_rid(self, ids, levels, result_format):
        """

        Parameters
        ----------
        ids :
            
        levels :
            
        result_format :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_taxonomy_by_rank(self, levels):
        """

        Parameters
        ----------
        levels :
            

        Returns
        -------

        """
        pass


class DatabaseAccessionMetabase(DatabaseBackboneMetabase):
    """ """
    @abstractmethod
    def get_accession_by_tid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_accession_by_rid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

class DatabaseSequenceMetabase(DatabaseBackboneMetabase):
    """ """
    @abstractmethod
    def get_sequence_by_tid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_sequence_by_rid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_alignment_by_tid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_alignment_by_rid(self, ids, **kwargs):
        """

        Parameters
        ----------
        ids :
            
        **kwargs :
            

        Returns
        -------

        """
        pass



