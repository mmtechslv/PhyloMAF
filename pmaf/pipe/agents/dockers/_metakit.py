from abc import ABC,abstractmethod

class DockerBackboneMetabase(ABC):
    """Base interface for all Docker classes."""
    @abstractmethod
    def wrap_meta(self):
        """Returns a wrapped metadata as a dictionary."""
        pass

    @abstractmethod
    def get_subset(self, indices, exclude_missing):
        """Returns subset of the Docker instance.

        Parameters
        ----------
        indices :
            
        exclude_missing :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_iterator(self, indices, exclude_missing):
        """Returns an generator for that iterates over Docker elements.

        Parameters
        ----------
        indices :
            
        exclude_missing :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def singleton(self):
        """Returns true if instance is singleton."""
        pass

    @property
    @abstractmethod
    def empty(self):
        """Returns true of instance is empty."""
        pass

    @property
    @abstractmethod
    def data(self):
        """Returns objects with actual data that docker contains."""
        pass

    @property
    @abstractmethod
    def missing(self):
        """Returns IDs of elements that are set to None."""
        pass

    @property
    @abstractmethod
    def valid(self):
        """Returns IDs of elements that are not set to None."""
        pass

    @property
    @abstractmethod
    def _transit(self):
        """Returns true of Docker is a transit/intermediate object."""
        pass

    @property
    @abstractmethod
    def metadata(self):
        """Returns metadata of the Docker."""
        pass

    @metadata.setter
    @abstractmethod
    def metadata(self, value):
        """Setter for the metadata property of the docker.

        Parameters
        ----------
        value :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def name(self):
        """Returns name/label of the docker."""
        pass

    @name.setter
    @abstractmethod
    def name(self, value):
        """Set name property of the docker.

        Parameters
        ----------
        value :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def index(self):
        """Returns all IDs."""
        pass

    @property
    @abstractmethod
    def count(self):
        """ """
        pass

class DockerIdentifierMetabase(DockerBackboneMetabase):
    """Interface for DockerIdentifiers."""
    @abstractmethod
    def to_array(self, indices, exclude_missing):
        """Converts Docker elements into array or Docker container into dict of arrays.

        Parameters
        ----------
        indices :
            
        exclude_missing :
            

        Returns
        -------

        """
        pass

class DockerTaxonomyMetabase(DockerBackboneMetabase):
    """Interface for DockerTaxonomy."""
    @abstractmethod
    def get_avail_ranks(self,indices):
        """

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def to_dataframe(self, indices, ranks):
        """Converts docker elements into dataframe or Docker container into dict of dataframes.

        Parameters
        ----------
        indices :
            
        ranks :
            

        Returns
        -------

        """
        pass

class DockerPhylogenyMetabase(DockerBackboneMetabase):
    """Interface for DockerPhylogeny."""
    @abstractmethod
    def get_node_names(self, indices):
        """

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_tip_names(self, indices):
        """Returns only tip names of the tree that Docker contains.

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

class DockerSequenceMetabase(DockerBackboneMetabase):
    """Interface for DockerSequence."""
    @abstractmethod
    def to_multiseq(self, indices):
        """Converts Docker elements into Multiseq object.

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_records(self, indices): # FIXME: This method is ugly since it only required by classifier module that is not working at the moment. Hence, it should be carried out only when necessary by a separate function.
        """Returns the Docker elements as "record" tuples.

        Parameters
        ----------
        indices :
            

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_stats(self, indices):# FIXME: Same as DockerSequenceMetabase.get_records(...). Just remove it.
        """Returns the "stats" for "record" elements.

        Parameters
        ----------
        indices) :
            # FIXME: Same as DockerSequenceMetabase.get_records(...:
        indices) :
            # FIXME: Same as DockerSequenceMetabase.get_records(...:
        indices) :
            # FIXME: Same as DockerSequenceMetabase.get_records(...:
        indices):# FIXME: Same as DockerSequenceMetabase.get_records(... :
            

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def mode(self):
        """Returns mode of the Docker instance. Mode refers to DNA, RNA or Protein."""
        pass

    @property
    @abstractmethod
    def aligned(self):
        """Returns True if the sequences that Docker contains are aligned."""
        pass

class DockerAccessionMetabase(DockerBackboneMetabase):
    """Interface for DockerAccession."""
    @property
    @abstractmethod
    def sources(self):
        """ """
        pass

    @abstractmethod
    def to_identifier_by_src(self, source, exclude_missing):
        """Converts the Docker elements to the DockerIdentifier for selected `source` parameter.

        Parameters
        ----------
        source :
            
        exclude_missing :
            

        Returns
        -------

        """
        pass