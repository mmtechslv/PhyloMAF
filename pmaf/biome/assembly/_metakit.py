from abc import abstractmethod
from pmaf.biome._metakit import BiomeFeatureMetabase, BiomeSampleMetabase


class BiomeAssemblyBackboneMetabase(BiomeFeatureMetabase, BiomeSampleMetabase):
    """ """

    @abstractmethod
    def export(self, output_dir, *args, **kwargs):
        """

        Parameters
        ----------
        output_dir :
            
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_subset(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def add_essentials(self, *args):
        """

        Parameters
        ----------
        *args :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def to_otu_table(self, *args, **kwargs):
        """

        Parameters
        ----------
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def write_otu_table(self, output_fp, *args, **kwargs):
        """

        Parameters
        ----------
        output_fp :
            
        *args :
            
        **kwargs :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def essentials(self):
        """ """
        pass

    @property
    @abstractmethod
    def controller(self):
        """ """
        pass
