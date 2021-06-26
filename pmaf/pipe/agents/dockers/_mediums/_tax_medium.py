from pmaf.pipe.agents.dockers._metakit import DockerTaxonomyMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
from pmaf.internal._shared import validate_ranks, extract_valid_ranks, sort_ranks
import pandas as pd
import numpy as np
from typing import Optional, Union, Any, Dict


class DockerTaxonomyMedium(DockerTaxonomyMetabase, DockerBase):
    """The :term:`docker` class responsible for handling taxonomy data."""

    _UNIT_TYPES = (dict, type(None))

    def __init__(
        self,
        taxonomy: Union[pd.DataFrame, list, dict, "DockerTaxonomyMedium"],
        **kwargs: Any
    ):
        """Constructor.

        Parameters
        ----------
        taxonomy
            List-like or dict-like like taxonomy data where values are either
            taxonomies with types :attr:`.UNIT_TYPE` (singleton) or instances of :class:`.DockerTaxonomyMedium`
        kwargs
            Compatibility
        """
        tmp_avail_ranks_fdf = None
        if isinstance(taxonomy, pd.DataFrame):
            valid_ranks = extract_valid_ranks(taxonomy.columns.tolist())
            if valid_ranks:
                tmp_taxonomy = taxonomy.loc[:, valid_ranks].to_dict(orient="index")
                tmp_avail_ranks_fdf = {
                    rank for rank in valid_ranks if taxonomy.loc[:, rank].notna().any()
                }
            else:
                raise ValueError("`taxonomy` contain invalid ranks.")
        else:
            if isinstance(taxonomy, list):
                tmp_taxonomy = {k: v for k, v in enumerate(taxonomy)}
            elif isinstance(taxonomy, dict):
                if all(
                    [
                        isinstance(value, (str, type(None)))
                        for value in taxonomy.values()
                    ]
                ):
                    tmp_taxonomy = {kwargs.get("name", 0): taxonomy}
                else:
                    tmp_taxonomy = taxonomy
            else:
                tmp_taxonomy = {kwargs.get("name", 0): taxonomy}
        container_mode_test = any(
            [isinstance(data_elem, type(self)) for data_elem in tmp_taxonomy.values()]
        )
        if not container_mode_test:
            if tmp_avail_ranks_fdf is None:
                tmp_ranks = set()
                for tax_elem in tmp_taxonomy.values():
                    if tax_elem is not None:
                        if validate_ranks(tax_elem.keys()):
                            tmp_ranks.update(tax_elem.keys())
                        else:
                            raise ValueError("`taxonomy` contain invalid ranks.")
                tmp_avail_ranks = list(tmp_ranks)
            else:
                tmp_avail_ranks = tmp_avail_ranks_fdf
            tmp_adj_taxonomy = dict.fromkeys(tmp_taxonomy.keys(), None)
            for ix, tax_elem in tmp_taxonomy.items():
                if tax_elem is not None:
                    tmp_taxa_dict = dict.fromkeys(tmp_avail_ranks, None)
                    for rank in tmp_avail_ranks:
                        if rank in tax_elem.keys():
                            if tax_elem[rank] is not None:
                                tmp_taxa_dict[rank] = (
                                    tax_elem[rank] if len(tax_elem[rank]) > 0 else None
                                )
                            else:
                                tmp_taxa_dict[rank] = None
                        else:
                            tmp_taxa_dict[rank] = None
                    tmp_adj_taxonomy[ix] = (
                        None
                        if all([taxa is None for taxa in tmp_taxa_dict.values()])
                        else tmp_taxa_dict
                    )
                else:
                    tmp_adj_taxonomy[ix] = None
        else:
            tmp_adj_taxonomy = tmp_taxonomy
            tmp_avail_ranks = dict.fromkeys(tmp_taxonomy.keys(), None)
            for ix, tax_medium in tmp_taxonomy.items():
                if isinstance(tax_medium, type(self)):
                    tmp_avail_ranks[ix] = tax_medium.get_avail_ranks()
        super().__init__(
            _data_dict=tmp_adj_taxonomy, _valid_types=self._UNIT_TYPES, **kwargs
        )
        if container_mode_test and self.singleton:
            self.__avail_ranks = next(iter(tmp_avail_ranks.values()))
        else:
            self.__avail_ranks = tuple(tmp_avail_ranks)

    def to_dataframe(
        self,
        indices: Optional[np.ndarray] = None,
        ranks: Union[str, list, None] = None,
        exclude_missing: bool = False,
    ) -> Union[pd.DataFrame, Dict[Union[str, int], Optional[pd.DataFrame]]]:
        """Convert internal data to :class:`~pandas.DataFrame` instance.

        Parameters
        ----------
        indices
            Target indices or None for all
        ranks
            Target rank(s) or None for all available
        exclude_missing
            Exclude missing data

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`~pandas.DataFrame`
            if not :term:`singleton` then return dictionary with values :meth:`.to_dataframe`
        """
        if indices is None:
            target_indices = self.index
        elif np.isscalar(indices):
            target_indices = np.asarray([indices])
        else:
            target_indices = np.asarray(indices)
        if not np.isin(target_indices, self.index).all():
            raise ValueError("`indices` are invalid.")
        if exclude_missing:
            target_indices = np.asarray(
                [ix for ix in target_indices if self.data[ix] is not None]
            )
        if self.singleton:
            if ranks is None:
                target_ranks = self.__avail_ranks
            else:
                if isinstance(ranks, str):
                    target_ranks = [ranks]
                else:
                    target_ranks = [
                        rank for rank in ranks if rank in self.__avail_ranks
                    ]
            if np.isin(target_ranks, self.__avail_ranks).all():
                product = pd.DataFrame.from_dict(
                    {
                        **self.data,
                        **{ix: {r: None for r in target_ranks} for ix in self.missing},
                    },
                    orient="index",
                ).loc[target_indices, sort_ranks(target_ranks)]
                if isinstance(ranks, str) and len(target_ranks) == 1:
                    return product.loc[:, target_ranks[0]]
                else:
                    return product
            else:
                raise ValueError("`ranks` are invalid.")
        else:
            return {
                ix: self.data[ix].to_dataframe(ranks=ranks, exclude_missing=False)
                for ix in target_indices
            }

    def get_avail_ranks(
        self, indices: Optional[np.ndarray] = None
    ) -> Union[tuple, Dict[Union[str, int], Optional[tuple]]]:
        """Get available ranks for all taxonomy elements or limited by
        `indices`

        Parameters
        ----------
        indices
            Target indices or None for all

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`~numpy.ndarray`
            if not :term:`singleton` then return dictionary with values :meth:`.get_avail_ranks`
        """
        if self.singleton:
            return self.__avail_ranks
        else:
            if indices is None:
                target_indices = self.index
            elif np.isscalar(indices):
                target_indices = np.asarray([indices])
            else:
                target_indices = np.asarray(indices)
            if not np.isin(target_indices, self.index).all():
                raise ValueError("`indices` are invalid.")
            return {ix: self.__avail_ranks[ix] for ix in target_indices}
