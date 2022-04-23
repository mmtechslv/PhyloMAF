from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
import pandas as pd
import numpy as np
from typing import Union, Any, Sequence, Optional, Dict


class DockerIdentifierMedium(DockerIdentifierMetabase, DockerBase):
    """The :term:`docker` class responsible for handling any kind of
    identifiers."""

    _UNIT_TYPES = (int, str, np.integer, type(None))

    def __init__(
        self,
        identifiers: Union[Sequence, pd.Series, dict, "DockerIdentifierMedium"],
        **kwargs: Any
    ):
        """Constructor.

        Parameters
        ----------
        identifiers
            List-like or dict-like like identifier data where values are either
            identifiers with types :attr:`.UNIT_TYPES` (singleton) or instances of :class:`.DockerIdentifierMedium`
        kwargs
            Compatibility
        """
        if isinstance(identifiers, (list, tuple, np.ndarray, pd.Index)):
            tmp_identifiers = {k: v for k, v in enumerate(identifiers)}
        elif isinstance(identifiers, pd.Series):
            tmp_identifiers = identifiers.to_dict()
        elif isinstance(identifiers, dict):
            tmp_identifiers = identifiers
        elif isinstance(identifiers, self._UNIT_TYPES):
            tmp_identifiers = {kwargs.get("name", 0): identifiers}
        else:
            raise TypeError("`identifiers` has invalid type.")
        super().__init__(
            _data_dict=tmp_identifiers, _valid_types=self._UNIT_TYPES, **kwargs
        )

    def to_array(
        self,
        indices: Optional[np.ndarray] = None,
        exclude_missing: bool = False,
        unique=False,
    ) -> Union[np.ndarray, Dict[Union[str, int], Optional[np.ndarray]]]:
        """Convert to :class:`numpy.ndarray` with identifiers.

        Parameters
        ----------
        indices
            Target indices or None for all
        exclude_missing
            Exclude missing data
        unique
            Drop duplicated identifiers

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`numpy.ndarray`
            if not :term:`singleton` then return dictionary with values :meth:`.to_array`
        """
        if indices is None:
            target_indices = self.index
        elif np.isscalar(indices):
            target_indices = np.asarray([indices])
        else:
            target_indices = np.asarray(indices)
        if not np.isin(target_indices, self.index).all():
            raise ValueError("`indices` are invalid.")
        if self.singleton:
            if exclude_missing:
                tmp_flat = np.asarray(
                    [self.data[ix] for ix in target_indices if ix not in self.missing]
                )
            else:
                tmp_flat = np.asarray([self.data[ix] for ix in target_indices])
            if unique:
                return np.unique(tmp_flat)
            else:
                return tmp_flat
        else:
            return {
                ix: self.data[ix].to_array(exclude_missing=exclude_missing)
                for ix in target_indices
            }
