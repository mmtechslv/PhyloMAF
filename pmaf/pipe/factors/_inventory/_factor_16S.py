from pmaf.pipe.factors._base import FactorBase


class Factor16S(FactorBase):
    """Factor class for mining :term:`16S` :term:`rRNA` data."""

    def __init__(self, **kwargs):
        """Constructor for :class:`.Factor16S`

        Parameters
        ----------
        kwargs
            Additional factors for custom pipe members.
        """
        self.__externals = kwargs
        self.__factors = {
            "molecule-type": "DNA",
            "gene-type": "marker",
            "gene-name": "rRNA",
            "gene-target": "16S",
        }

    @property
    def externals(self):
        """Additional parameters."""
        return self.__externals

    @property
    def factors(self):
        """Public factors that define :class:`.Factor16S`"""
        return self.__factors
