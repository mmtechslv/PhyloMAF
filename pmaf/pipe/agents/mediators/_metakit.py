from abc import ABC, abstractmethod

class MediatorBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def verify_factor(self,factor):
        """

        Parameters
        ----------
        factor :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def reconfig(self,name,value):
        """

        Parameters
        ----------
        name :
            
        value :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def state(self):
        """ """
        pass

    @property
    @abstractmethod
    def client(self):
        """ """
        pass

    @property
    @abstractmethod
    def configs(self):
        """ """
        pass

class MediatorAccessionMetabase(MediatorBackboneMetabase):
    """ """

    @abstractmethod
    def get_accession_by_identifier(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_identifier_by_accession(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass


class MediatorSequenceMetabase(MediatorBackboneMetabase):
    """ """
    @abstractmethod
    def get_sequence_by_identifier(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_identifier_by_sequence(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

class MediatorPhylogenyMetabase(MediatorBackboneMetabase):
    """ """
    @abstractmethod
    def get_phylogeny_by_identifier(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_identifier_by_phylogeny(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

class MediatorTaxonomyMetabase(MediatorBackboneMetabase):
    """ """
    @abstractmethod
    def get_taxonomy_by_identifier(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_identifier_by_taxonomy(self, docker, factor, **kwargs):
        """

        Parameters
        ----------
        docker :
            
        factor :
            
        **kwargs :
            

        Returns
        -------

        """
        pass
