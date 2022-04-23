from pmaf.pipe.agents.dockers._metakit import DockerAccessionMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
import pandas as pd
import numpy as np
from typing import Union, Any


class DockerAccessionMedium(DockerAccessionMetabase, DockerBase):
    """The :term:`docker` class responsible for handling accession numbers."""

    _UNIT_TYPES = (dict, type(None))

    def __init__(
        self,
        accessions: Union[list, pd.Series, pd.DataFrame, dict, "DockerAccessionMedium"],
        **kwargs: Any
    ):
        """Constructor.

        Parameters
        ----------
        accessions
            List-like or dict-like like accession data where values are either
            accession numbers with types :attr:`.UNIT_TYPE` (singleton) or instances of :class:`.DockerAccessionMedium`
        kwargs
            Compatibility
        """
        if isinstance(accessions, list):
            try:
                tmp_accessions = {k: {v[0]: v[1]} for k, v in enumerate(accessions)}
            except (IndexError, TypeError) as e:
                raise ValueError(
                    "`accessions` provided as list must have following format [(ACS_NAME:ACS_NO),(ACS_NAME:ACS_NO),...]."
                )
        elif isinstance(accessions, pd.Series):
            tmp_accessions = {
                kwargs.get("name", 0): {accessions.name: accessions.to_dict()}
            }
        elif isinstance(accessions, pd.DataFrame):
            tmp_accessions = accessions.to_dict(orient="index")
        elif isinstance(accessions, dict):
            if all(
                [
                    isinstance(value, (int, str, np.integer, tuple, type(None)))
                    for value in accessions.values()
                ]
            ):
                tmp_accessions = {kwargs.get("name", 0): accessions}
            else:
                tmp_accessions = accessions
        else:
            tmp_accessions = {kwargs.get("name", 0): accessions}
        container_mode_test = any(
            [isinstance(data_elem, type(self)) for data_elem in tmp_accessions.values()]
        )
        tmp_accessions_adj = dict.fromkeys(tmp_accessions.keys(), None)
        if not container_mode_test:
            tmp_sources = set()
            for ix, accs_dict in tmp_accessions.items():
                if accs_dict is not None:
                    for src, _ in accs_dict.items():
                        tmp_sources.add(src)
                    tmp_accessions_adj[ix] = (
                        None
                        if all([taxa is None for taxa in accs_dict.values()])
                        else accs_dict
                    )
                else:
                    tmp_accessions_adj[ix] = None
        else:
            tmp_sources = set()
            tmp_accessions_adj = tmp_accessions
            for ix, accs_medium in tmp_accessions.items():
                if isinstance(accs_medium, type(self)):
                    tmp_sources.update(accs_medium.sources)
        self.__sources = tuple(tmp_sources)
        super().__init__(
            _data_dict=tmp_accessions_adj, _valid_types=self._UNIT_TYPES, **kwargs
        )

    def to_identifier_by_src(
        self, source: str, exclude_missing: bool = False
    ) -> DockerIdentifierMedium:
        """Convert to instances of :class:`DockerIdentifierMedium` for target
        `source`

        Parameters
        ----------
        source
            Accession number source label. For example, "ncbi", "greengenes", etc.
        exclude_missing
            Exclude missing data

        Returns
        -------
            Instance of :class:`.DockerIdentifierMedium`
        """
        if source not in self.__sources:
            raise ValueError("`source` was not found.")
        if exclude_missing:
            target_indices = [ix for ix, elem in self.data.items() if elem is not None]
        else:
            target_indices = self.index
        tmp_identifiers = dict.fromkeys(target_indices)
        if self.singleton:
            for ix in target_indices:
                if self.data[ix] is not None:
                    if source in self.data[ix].keys():
                        if isinstance(self.data[ix][source], tuple) > 0:
                            tmp_identifiers[ix] = DockerIdentifierMedium(
                                self.data[ix][source],
                                name=ix,
                                metadata={"source": source},
                            )
                        else:
                            tmp_identifiers[ix] = self.data[ix][source]
        else:
            for ix in target_indices:
                if self.data[ix] is not None:
                    if source in self.data[ix].sources:
                        tmp_identifiers[ix] = self.data[ix].to_identifier_by_src(
                            source, exclude_missing
                        )
        new_metadata = {"source": source, "master": self.wrap_meta()}
        return DockerIdentifierMedium(
            tmp_identifiers, name=self.name, metadata=new_metadata
        )

    @property
    def sources(self):
        """List available accession number sources."""
        return self.__sources
