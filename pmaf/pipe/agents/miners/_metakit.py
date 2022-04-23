from abc import ABC, abstractmethod


class MinerBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def verify_docker(self, docker):
        """

        Parameters
        ----------
        docker :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_accession_by_identifier(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_identifier_by_accession(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_sequence_by_identifier(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_phylogeny_by_identifier(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_taxonomy_by_identifier(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @abstractmethod
    def yield_identifier_by_docker(self, docker, **kwargs):
        """

        Parameters
        ----------
        docker :

        **kwargs :


        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def factor(self):
        """ """
        pass

    @property
    @abstractmethod
    def mediator(self):
        """ """
        pass

    @property
    @abstractmethod
    def state(self):
        """ """
        pass
