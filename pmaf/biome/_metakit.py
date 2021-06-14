from abc import ABC, abstractmethod
from typing import Union, Sequence, TypeVar, Any, Optional, Type
from pmaf.internal._typing import GenericIdentifier

class BiomeBackboneMetabase(ABC):
    """ """

    @abstractmethod
    def _repr_appendage__(self):
        """ """
        pass

    @abstractmethod
    def copy(self):
        """ """
        pass

    @property
    @abstractmethod
    def shape(self):
        """ """
        pass

    @property
    @abstractmethod
    def metadata(self):
        """ """
        pass

    @metadata.setter
    @abstractmethod
    def metadata(self, value):
        """

        Args:
          value:

        Returns:

        """
        pass

    @property
    @abstractmethod
    def name(self):
        """ """
        pass

    @name.setter
    @abstractmethod
    def name(self,value):
        """

        Args:
          value:

        Returns:

        """
        pass


class BiomeFeatureMetabase(BiomeBackboneMetabase):
    """ """

    def get_feature_ids(self,
                        dtype: Union[str, Type, None] = None):
        """This function and its sample twin is a rescue method to fix RepPhylogeny index problem.

        Args:
            dtype: Type to cast into

        Returns:
            :class:`~numpy.ndarray` of type `dtype`

        """
        if dtype is None:
            return self.xrid
        else:
            return self.xrid.astype(dtype)

    @property
    @abstractmethod
    def xrid(self):
        """ """
        pass


class BiomeSampleMetabase(BiomeBackboneMetabase):
    """ """

    def get_sample_ids(self,
                       dtype: Union[str, Type, None] = None):
        """This function and its sample twin is a rescue method to fix RepPhylogeny index problem.

        Args:
            dtype: Type to cast into

        Returns:
            :class:`~numpy.ndarray` of type `dtype`

        """
        if dtype is None:
            return self.xsid
        else:
            return self.xsid.astype(dtype)

    @property
    @abstractmethod
    def xsid(self):
        """ """
        pass
