from abc import ABC, abstractmethod


class EntrezBackboneMetabase(ABC):
    """ """

    @property
    @abstractmethod
    def state(self):
        """ """
        pass

    @abstractmethod
    def get_taxid_by_query(self, query):
        """

        Parameters
        ----------
        query :


        Returns
        -------

        """
        pass
