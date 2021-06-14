import warnings

warnings.simplefilter('ignore', category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialSampleMetabase
from pmaf.biome.essentials._base import EssentialBackboneBase
from os import path
import pandas as pd
import numpy as np
from collections import defaultdict
import biom
from typing import Union, Optional, TypeVar, Tuple, Callable, Any
from pmaf.internal._typing import GenericIdentifier, Mapper

T = TypeVar('T', bound='SampleMetadata')


class SampleMetadata(EssentialBackboneBase, EssentialSampleMetabase):
	"""An `essential` class for handling sample metadata."""

	def __init__(self,
				 samples: Union[pd.DataFrame, str],
				 axis: Union[int, str] = 1,
				 index_col: Union[str, int] = 0,
				 **kwargs: Any) -> None:
		"""Constructor for :class:`.SampleMetadata`

		Args:
			samples: Data containing sample metadata
			axis: Sample index axis. Using 0/`index` sets rows as sample indices while 1/`columns` sets columns as indices.
			index_col: Which row/column to use as index.
			**kwargs: Passed to :func:`~pandas.read_csv` or :mod:`biom` loader.

		"""
		tmp_sample = None
		tmp_metadata = kwargs.pop('metadata', {})
		if axis in [0, 1, 'index', 'columns']:
			tmp_axis = 0 if axis in [0, 'index'] else 1
		else:
			raise ValueError('`axis` is invalid.')
		if isinstance(samples, pd.DataFrame):
			if samples.shape[1] > 0:
				tmp_sample = samples
			else:
				raise ValueError('Provided `samples` Datafame is invalid.')
		elif isinstance(samples, str):
			if path.isfile(samples):
				file_extension = path.splitext(samples)[-1].lower()
				if file_extension in ['.csv', '.tsv']:
					tmp_sample = pd.read_csv(samples, index_col=index_col, **kwargs)
				elif file_extension in ['.biom', '.biome']:
					tmp_frequency, new_metadata = self.__load_biom(samples, **kwargs)
					tmp_metadata.update({'biom': new_metadata})
				else:
					raise NotImplementedError('File type is not supported.')
			else:
				raise FileNotFoundError('Provided `samples` file path is invalid.')
		else:
			raise TypeError('Provided `samples` has invalid type.')
		tmp_sample = tmp_sample.T if tmp_axis == 1 else tmp_sample

		self.__internal_samples = pd.concat([tmp_sample.select_dtypes([], ['object']),
											 tmp_sample.select_dtypes(['object']).apply(pd.Series.astype,
																						dtype='category')], axis=1) \
			.reindex(tmp_sample.columns, axis=1)
		super().__init__(metadata=tmp_metadata, **kwargs)

	@classmethod
	def from_csv(cls,
				 filepath: str,
				 **kwargs: Any) -> T:
		"""Factory method to construct a :class:`.SampleMetadata` from CSV file.

		Args:
			filepath (str): Path to .csv file.
			**kwargs: Passed to the constructor.

		Returns:
			Instance of :class:`.SampleMetadata`

		"""
		tmp_sample = pd.read_csv(filepath, **kwargs)
		tmp_metadata = kwargs.pop('metadata', {})
		tmp_metadata.update({'filepath': path.abspath(filepath)})
		return cls(samples=tmp_sample, metadata=tmp_metadata, **kwargs)

	@classmethod
	def from_biom(cls,
				  filepath: str,
				  **kwargs) -> T:
		"""Factory method to construct a :class:`.SampleMetadata` from :mod:`biom` file.

		Args:
			filepath: (str): Path to :mod:`biom` file.
			**kwargs: Passed to the constructor.

		Returns:
			Instance of :class:`.SampleMetadata`
		"""
		samples_frame, new_metadata = cls.__load_biom(filepath, **kwargs)
		tmp_metadata = kwargs.pop('metadata', {})
		tmp_metadata.update({'biom': new_metadata})
		return cls(frequency=samples_frame, metadata=tmp_metadata, **kwargs)

	@classmethod
	def __load_biom(cls,
					filepath: str,
					**kwargs: Any) -> Tuple[pd.DataFrame, dict]:
		"""Actual private method to process :mod:`biom` file.

		Args:
			filepath: :mod:`biom` file path.
			**kwargs:  Compatibility.
		"""
		biom_file = biom.load_table(filepath)
		if biom_file.metadata(axis='sample') is not None:
			sample_data = biom_file.metadata_to_dataframe('sample')
		else:
			raise ValueError('Biom file does not contain sample metadata.')
		return sample_data, {}

	def _rename_samples_by_map(self,
							   map_like: Mapper,
							   **kwargs) -> Optional[Mapper]:
		"""Rename sample names by map and ratify action.

		Args:
			map_like: Mapper to use for renaming.
			**kwargs: Compatibility
		"""
		self.__internal_samples.rename(mapper=map_like, axis=0, inplace=True)
		return self._ratify_action('_rename_samples_by_map', map_like, **kwargs)

	def _remove_samples_by_id(self,
							  ids: GenericIdentifier,
							  **kwargs) -> Optional[GenericIdentifier]:
		"""Remove samples by sample ids and ratify action.

		Args:
			ids: Sample identifiers
			**kwargs: Compatibility

		"""
		tmp_ids = np.asarray(ids, dtype=self.__internal_samples.index.dtype)
		if len(tmp_ids) > 0:
			self.__internal_samples.drop(tmp_ids, inplace=True)
		return self._ratify_action('_remove_samples_by_id', ids, **kwargs)

	def _merge_samples_by_map(self,
							  map_dict: Mapper,
							  aggfunc: Union[str, Callable] = 'mean',
							  variable: Union[str, int, None] = None,
							  **kwargs) -> Optional[Mapper]:
		"""Merge samples and ratify action.

		Args:
			map_dict: Map to use for merging
			aggfunc: Aggregation function
			variable: Compatibility
			**kwargs: Compatibility

		"""
		tmp_agg_dict = defaultdict(list)
		for new_id, group in map_dict.items():
			tmp_agg_dict[new_id] = self.__internal_samples.loc[group, :].agg(func=aggfunc, axis=0).to_dict()
		tmp_samples = pd.DataFrame.from_dict(tmp_agg_dict, orient='index')
		tmp_samples.index.name = self.__internal_samples.index.name
		self.__internal_samples = tmp_samples
		return self._ratify_action('_merge_samples_by_map', map_dict, aggfunc=aggfunc, **kwargs)

	def rename_samples(self,
					   mapper: Mapper) -> None:
		"""Rename sample names by `mapper`

		Args:
			mapper: Dict-like mapper use for renaming.

		"""
		if isinstance(mapper, dict) or callable(mapper):
			if isinstance(mapper, dict):
				if self.__internal_samples.index.isin(list(mapper.keys())).sum() == len(mapper):
					self._rename_samples_by_map(mapper)
				else:
					raise ValueError('Invalid sample ids are provided.')
			else:
				self._rename_samples_by_map(mapper)
		else:
			raise TypeError('Invalid `mapper` type.')

	def drop_sample_by_id(self,
						  ids: GenericIdentifier,
						  **kwargs) -> Optional[GenericIdentifier]:
		"""Drop samples by sample identifiers.

		Args:
			ids: Identifiers to remove
			**kwargs: Compatibility
		"""
		target_ids = np.asarray(ids)
		if self.xsid.isin(target_ids).sum() == len(target_ids):
			return self._remove_samples_by_id(target_ids, **kwargs)
		else:
			raise ValueError('Invalid sample ids are provided.')

	def get_variables_by_id(self,
							ids: Optional[GenericIdentifier] = None,
							variables: Optional[GenericIdentifier] = None) -> Union[pd.Series, pd.DataFrame, str, int]:
		"""Get sample metadata by sample identifiers and variables.

		Args:
			ids: Sample identifiers
			variables: Metadata varibles

		Returns:
			:class:`~pandas.DataFrame`

		"""
		if ids is None:
			target_ids = self.xsid
		else:
			target_ids = np.asarray(ids)
		if variables is None:
			target_vars = self.variables
		else:
			target_vars = np.asarray(variables)
		if (self.__internal_samples.index.isin(target_ids).sum() <= len(target_ids)) and (
				self.__internal_samples.columns.isin(target_vars).sum() <= len(target_vars)):
			return self.__internal_samples.loc[target_ids, target_vars]
		else:
			raise ValueError('Invalid sample ids or variables are provided.')

	def merge_samples_by_variable(self,
								  variable: Union[str, int],
								  aggfunc: Union[str, Callable] = 'mean',
								  **kwargs) -> Optional[Mapper]:
		"""Merge samples by `variable`.

		Args:
			variable: Sample metadata variable.
			aggfunc: Aggregation function that will be applied to both :class:`.SampleMetadata` instance and ratified to other `essentials` if contained in :class:`~pmaf.biome.assembly.BiomeAssembly` instance.
			**kwargs: Compatibility

		"""
		ret = {}
		if variable not in self.__internal_samples.columns:
			raise TypeError('`variable` is invalid.')
		groups = self.__internal_samples.groupby(variable)
		if len(groups.groups) > 1:
			tmp_variable = []
			tmp_groups = []
			group_indices = []
			for var, sample_ids in groups.groups.items():
				tmp_variable.append(var)
				tmp_groups.append(list(sample_ids))
				group_indices.append(var)
			ret = dict(zip(group_indices, tmp_groups))
		return self._merge_samples_by_map(ret, aggfunc=aggfunc, variable=variable, **kwargs)

	def copy(self) -> T:
		"""Copy of the instance."""
		return type(self)(samples=self.__internal_samples.copy(), axis=0, metadata=self.metadata, name=self.name)

	def get_subset(self,
				   sids: GenericIdentifier = None,
				   *args,
				   **kwargs) -> T:
		"""Get subset of the :class:`.SampleMetadata`.

		Args:
			sids: Sample Identifiers
			*args: Compatibility
			**kwargs: Compatibility

		Returns:
			 Instance of :class:`.SampleMetadata`.
		"""
		if sids is None:
			target_sids = self.xsid
		else:
			target_sids = np.asarray(sids).astype(self.__internal_samples.index.dtype)
		if not self.xsid.isin(target_sids).sum() == len(target_sids):
			raise ValueError('Invalid sample ids are provided.')
		return type(self)(samples=self.__internal_samples.loc[target_sids, :], axis=0, metadata=self.metadata,
						  name=self.name)

	def _export(self,
				*args,
				**kwargs) -> Tuple[pd.DataFrame, dict]:
		"""Present only for backward compatibility with other `essentials`. """
		return self.data, kwargs

	def export(self,
			   output_fp: str,
			   *args,
			   _add_ext: bool = False,
			   sep: str = ',',
			   **kwargs) -> None:
		"""Exports the sample metadata content into the specified file.

		Args:
			output_fp: Export filepath
			*args: Compatibility
			_add_ext: Add file extension or not.
			sep: Delimiter
			**kwargs: Compatibility
		"""
		tmp_export, rkwarg = self._export(*args, **kwargs)
		if _add_ext:
			tmp_export.to_csv("{}.csv".format(output_fp), sep=sep)
		else:
			tmp_export.to_csv(output_fp, sep=sep)

	@property
	def variables(self) -> np.ndarray:
		""" Sample metadata variables """
		return self.__internal_samples.columns.values

	@property
	def data(self) -> pd.DataFrame:
		""" Sample metadata """
		return self.__internal_samples

	@property
	def xsid(self) -> pd.Index:
		""" Sample identifiers """
		return self.__internal_samples.index
