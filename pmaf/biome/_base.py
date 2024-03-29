from ._metakit import BiomeBackboneMetabase, BiomeFeatureMetabase, BiomeSampleMetabase
from typing import Any, Optional
from pmaf.internal._typing import Shape


class BiomeBackboneBase(BiomeBackboneMetabase):
    """Base class for all biome classes."""

    def __init__(
        self, metadata: Optional[dict] = None, name: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Constructor for `essentials` base.

        Args:
            metadata: Metadata of `essential` instance.
            name: Name/Label of `essential` instance
            **kwargs: Compatibility.
        """
        if isinstance(name, (str, int, type(None))):
            self.__name = name
        else:
            raise TypeError("`name` can be str,int or None")
        if isinstance(metadata, dict):
            self.__metadata = metadata
        elif metadata is None:
            self.__metadata = {}
        else:
            raise TypeError("`metadata` can be dict or None")

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        name = self.__name if self.__name is not None else "N/A"
        preffix = "{}:[{}]".format(class_name, name)
        if isinstance(self, BiomeFeatureMetabase) and not isinstance(
            self, BiomeSampleMetabase
        ):
            elements = ["Features:[{}]".format(len(self.xrid))]
        elif isinstance(self, BiomeSampleMetabase) and not isinstance(
            self, BiomeFeatureMetabase
        ):
            elements = ["Samples:[{}]".format(len(self.xsid))]
        else:
            elements = [
                "Features:[{}]".format(len(self.xrid)),
                "Samples:[{}]".format(len(self.xsid)),
            ]
        for name, value in self._repr_appendage__().items():
            elements.append("{}:[{}]".format(name, value))
        return "<{}, {}>".format(preffix, ", ".join(elements))

    @property
    def shape(self) -> Shape:
        """Return the shape/size of the `essential` instance.

        Parameters
        ----------

        Returns
        -------
        type
            Tuple with shape
        """

        if isinstance(self, BiomeFeatureMetabase) and isinstance(
            self, BiomeSampleMetabase
        ):
            return (len(self.xrid), len(self.xsid))
        elif isinstance(self, BiomeFeatureMetabase):
            return (len(self.xrid),)
        elif isinstance(self, BiomeSampleMetabase):
            return (len(self.xsid),)
        else:
            raise NotImplementedError

    @property
    def metadata(self):
        """The `essential` instance metadata."""
        return self.__metadata

    @metadata.setter
    def metadata(self, value):
        """

        Parameters
        ----------
        value :


        Returns
        -------

        """
        if value is None:
            self.__metadata = {}
        else:
            if isinstance(value, dict):
                self.__metadata = value
            else:
                raise TypeError("`metadata` can be None or dict")

    @property
    def name(self):
        """The `essential` instance name."""
        return self.__name

    @name.setter
    def name(self, value):
        """

        Parameters
        ----------
        value :


        Returns
        -------

        """
        if value is None:
            self.__name = {}
        else:
            if isinstance(value, (str, int)):
                self.__name = value
            else:
                raise TypeError("`name` can be None, str or int.")
