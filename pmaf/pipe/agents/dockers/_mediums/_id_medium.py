from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
import pandas as pd
import numpy as np

class DockerIdentifierMedium(DockerIdentifierMetabase,DockerBase):
    """ """
    _UNIT_TYPES = (int,str,np.integer,type(None))
    def __init__(self, identifiers, **kwargs):
        if isinstance(identifiers,(list,tuple,np.ndarray,pd.Index)):
            tmp_identifiers = {k:v for k,v in enumerate(identifiers)}
        elif isinstance(identifiers,pd.Series):
            tmp_identifiers = identifiers.to_dict()
        elif isinstance(identifiers,dict):
            tmp_identifiers = identifiers
        elif isinstance(identifiers,self._UNIT_TYPES):
            tmp_identifiers = {kwargs.get('name',0):identifiers}
        else:
            raise TypeError('`identifiers` has invalid type.')
        super().__init__(_data_dict=tmp_identifiers,_valid_types=self._UNIT_TYPES,**kwargs)

    def to_array(self, indices=None, exclude_missing=False, unique=False):
        """

        Parameters
        ----------
        indices :
            (Default value = None)
        exclude_missing :
            (Default value = False)
        unique :
            (Default value = False)

        Returns
        -------

        """
        if indices is None:
            target_indices = self.index
        elif np.isscalar(indices):
            target_indices = np.asarray([indices])
        else:
            target_indices = np.asarray(indices)
        if not np.isin(target_indices, self.index).all():
            raise ValueError('`indices` are invalid.')
        if self.singleton:
            if exclude_missing:
                tmp_flat = np.asarray([self.data[ix] for ix in target_indices if ix not in self.missing])
            else:
                tmp_flat = np.asarray([self.data[ix] for ix in target_indices])
            if unique:
                return np.unique(tmp_flat)
            else:
                return tmp_flat
        else:
            return {ix: self.data[ix].to_array(exclude_missing=exclude_missing) for ix in target_indices}
