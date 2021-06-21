from ._metakit import DockerBackboneMetabase
import numpy as np

class DockerBase(DockerBackboneMetabase):
    """ """
    def __init__(self, _data_dict, _valid_types, name=None, metadata=None, _transit=None, **kwargs):
        if isinstance(name,(str,int,np.integer,type(None))):
            tmp_name = name
        else:
            raise TypeError('`name` can be str,int or None')
        if isinstance(metadata,dict):
            tmp_metadata = metadata
        elif metadata is None:
            tmp_metadata = {}
        else:
            raise TypeError('`metadata` can be dict or None')
        container_mode_test = any([isinstance(data_elem, type(self)) for data_elem in _data_dict.values()])
        tmp_singelton = not container_mode_test
        tmp_transit = _transit
        if not container_mode_test:
            if all([isinstance(v, _valid_types) for v in _data_dict.values()]):
                tmp_data = _data_dict
            else:
                raise ValueError('Docker singleton can contain only following data types {}'.format(str(_valid_types)))
        else:
            if all([isinstance(data_elem, (type(self),type(None))) for data_elem in _data_dict.values()]):
                if len(_data_dict) == 1:
                    tmp_solo = next(iter(_data_dict.values()))
                    while len(tmp_solo.data) == 1:
                        tmp_solo_next = next(iter(tmp_solo.data.values()))
                        if isinstance(tmp_solo_next,type(self)):
                            tmp_solo = tmp_solo_next
                        else:
                            break
                    tmp_data = tmp_solo.data
                    tmp_metadata = {**tmp_solo.metadata, **tmp_metadata}
                    tmp_name = tmp_name if tmp_name is not None else tmp_solo.name
                    tmp_transit = tmp_solo._transit
                    if len(tmp_solo.data)>0:
                        if all([isinstance(data_elem, _valid_types) for data_elem in tmp_solo.data.values()]):
                            tmp_singelton = True
                else:
                    tmp_data = _data_dict
            else:
                raise TypeError('Docker container can only contain types as self or None.')

        self.__transit = tmp_transit
        self.__index = np.asarray(list(tmp_data.keys()))
        self.__data = dict(tmp_data)
        self.__singleton = tmp_singelton
        self.__name = tmp_name
        self.__metadata = tmp_metadata

    def __repr__(self):
        class_name = self.__class__.__name__
        name = self.__name if self.__name is not None else 'N/A'
        metadata = 'Yes' if len(self.metadata)>0 else 'No'
        repr_str = "<{}:[{}] Name:[{}], Metadata:[{}]>".format(class_name, self.count, name, metadata)
        return repr_str

    def wrap_meta(self):
        """ """
        return {'type':type(self).__name__,'metadata':self.__metadata,'name':self.__name}

    def get_subset(self,indices=None,exclude_missing=False):
        """

        Parameters
        ----------
        indices :
            (Default value = None)
        exclude_missing :
            (Default value = False)

        Returns
        -------

        """
        if indices is None:
            target_indices = self.__index
        elif np.isscalar(indices):
            target_indices = np.asarray([indices])
        else:
            target_indices = np.asarray(indices)
        if not np.isin(target_indices,self.__index).all():
            raise ValueError('`indices` are invalid.')
        if exclude_missing:
            tmp_subset = {ix:self.__data[ix] for ix in target_indices if self.__data[ix] is not None}
        else:
            tmp_subset = {ix: self.__data[ix] for ix in target_indices}
        return type(self)(tmp_subset,name=self.name,metadata=self.metadata)

    def get_iterator(self,indices=None,exclude_missing=False):
        """

        Parameters
        ----------
        indices :
            (Default value = None)
        exclude_missing :
            (Default value = False)

        Returns
        -------

        """
        if indices is None:
            target_indices = self.__index
        elif np.isscalar(indices):
            target_indices = np.asarray([indices])
        else:
            target_indices = np.asarray(indices)
        if not np.isin(target_indices,self.__index).all():
            raise ValueError('`indices` are invalid.')
        if exclude_missing:
            target_indices = np.asarray([ix for ix in target_indices if self.__data[ix] is not None])
        def iterator():
            """ """
            for ix in target_indices:
                yield ix, self.__data[ix]
        return iterator()

    @property
    def metadata(self):
        """ """
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
        if isinstance(value,dict):
            self.__metadata = value
        elif value is None:
            self.__metadata = {}
        else:
            raise TypeError('`metadata` can be dict or None')

    @property
    def name(self):
        """ """
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
        if isinstance(value,(str,int,type(None))):
            self.__name = value
        else:
            raise TypeError('`name` can be str,int or None')

    @property
    def singleton(self):
        """ """
        return self.__singleton

    @property
    def empty(self):
        """ """
        return self.count == 0

    @property
    def missing(self):
        """ """
        return np.asarray([k for k,v in self.__data.items() if v is None],dtype=self.__index.dtype)

    @property
    def valid(self):
        """ """
        return np.asarray([k for k,v in self.__data.items() if v is not None],dtype=self.__index.dtype)

    @property
    def data(self):
        """ """
        return self.__data

    @property
    def count(self):
        """ """
        return len(self.__data)

    @property
    def index(self):
        """ """
        return self.__index

    @property
    def _transit(self):
        """ """
        return self.__transit