import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase
import pandas as pd
import numpy as np
from pmaf.internal.io._seq import SequenceIO
from pmaf.internal._extensions._cpython._pmafc_extension._helper import (
    make_sequence_record_tuple,
)
from pmaf.internal._shared import get_stats_for_sequence_record_df
from pmaf.biome.essentials._base import EssentialBackboneBase
from pmaf.sequence._sequence._nucleotide import Nucleotide
from pmaf.sequence._multiple._multiple import MultiSequence
from typing import Union, Optional, Tuple, Any
from pmaf.internal._typing import AnyGenericIdentifier, Mapper


class RepSequence(EssentialBackboneBase, EssentialFeatureMetabase):
    """An `essential` class for handling feature sequence data."""

    def __init__(
        self,
        sequences: Union[str, MultiSequence, pd.DataFrame, pd.Series],
        **kwargs: Any
    ) -> None:
        """Constructor for :class:`.RepSequence`

        Parameters
        ----------
        sequences
             Sequence data
        kwargs
            Compatibility
        """
        super().__init__(**kwargs)
        tmp_sequences = []
        if isinstance(sequences, str):
            seqio = SequenceIO(sequences, upper=True)
            seqio_gen = seqio.pull_parser(id=True, description=True, sequence=True)
            for rid, desc, seq in seqio_gen:
                seq_rec = make_sequence_record_tuple(rid, seq) + (desc,)
                tmp_sequences.append(seq_rec)
        elif isinstance(sequences, MultiSequence):
            for seq in sequences.sequences:
                seq_rec = make_sequence_record_tuple(seq.name, str(seq.text)) + ("",)
                tmp_sequences.append(seq_rec)
        elif isinstance(sequences, pd.DataFrame):
            for rid, seq in sequences.loc[:, "sequence"].iteritems():
                seq_rec = make_sequence_record_tuple(rid, seq) + ("",)
                tmp_sequences.append(seq_rec)
        elif isinstance(sequences, pd.Series):
            for rid, seq in sequences.iteritems():
                seq_rec = make_sequence_record_tuple(rid, seq) + ("",)
                tmp_sequences.append(seq_rec)
        else:
            raise TypeError("`sequences` has unsupported type.")
        seq_record_df = pd.DataFrame.from_records(
            tmp_sequences,
            columns=["rid", "sequence", "length", "tab", "description"],
            index=["rid"],
        )
        self.__sequence_df = pd.concat(
            [
                seq_record_df[["sequence", "description"]],
                get_stats_for_sequence_record_df(seq_record_df),
            ],
            axis=1,
        )

    def _remove_features_by_id(
        self, ids: AnyGenericIdentifier, **kwargs: Any
    ) -> Optional[AnyGenericIdentifier]:
        """Remove features by `ids` and ratify action.

        Parameters
        ----------
        ids
            Feature identifiers
        kwargs
            Compatibility
        """
        tmp_ids = np.asarray(ids, dtype=self.__sequence_df.index.dtype)
        if len(tmp_ids) > 0:
            self.__sequence_df.drop(tmp_ids, inplace=True)
        return self._ratify_action("_remove_features_by_id", ids, **kwargs)

    def _merge_features_by_map(
        self, map_dict: Mapper, **kwargs: Any
    ) -> Optional[Mapper]:
        """Merge features and ratify action. THIS METHOD IS INCOMPLETE.

        Parameters
        ----------
        map_dict
            Map to use for merging
        kwargs
            Compatibility
        """
        print(
            "ASSUME ALIGNED SEQUENCES! :))"
        )  # TODO: This method must align sequences.
        return self._ratify_action("_merge_features_by_map", map_dict, **kwargs)

    def copy(self) -> "RepSequence":
        """Copy of the instance."""
        return type(self)(
            sequences=self.__sequence_df.loc[:, "sequence"],
            metadata=self.metadata,
            name=self.name,
        )

    def get_subset(
        self, rids: Optional[AnyGenericIdentifier] = None, *args: Any, **kwargs: Any
    ) -> "RepSequence":
        """Get subset of the :class:`.RepSequence`.

        Parameters
        ----------
        rids
            Feature identifiers.
        args
            Compatibility
        kwargs
            Compatibility

        Returns
        -------
            class:`.RepSequence`
        """
        if rids is None:
            target_rids = self.xrid
        else:
            target_rids = np.asarray(rids).astype(self.__sequence_df.index.dtype)
        if not self.xrid.isin(target_rids).sum() == len(target_rids):
            raise ValueError("Invalid feature ids are provided.")
        return type(self)(
            sequences=self.__sequence_df.loc[target_rids, "sequence"],
            metadata=self.metadata,
            name=self.name,
        )

    def to_multiseq(self) -> MultiSequence:
        """Creates an instance of
        :class:`~pmaf.sequence._multiple._multiple.MultiSequence` containing
        sequences.

        Returns
        -------
            class:`~pmaf.sequence._multiple._multiple.MultiSequence`
        """
        tmp_sequences = []
        for ix, seq, desc in self.__sequence_df[
            :, ["sequence", "describtion"]
        ].itertuples():
            tmp_sequences.append(
                Nucleotide(seq, name=None, metadata={"description": desc})
            )
        return MultiSequence(
            tmp_sequences, name=self.name, metadata=self.metadata, internal_id="taxid"
        )

    def _export(self, *args, **kwargs: Any) -> Tuple[MultiSequence, dict]:
        """Present only for backward compatibility with other `essentials`."""

        return self.to_multiseq(), kwargs

    def export(
        self, output_fp: str, *args, _add_ext: bool = False, **kwargs: Any
    ) -> None:
        """Exports the FASTA sequences into the specified file.

        Parameters
        ----------
        output_fp
            Export filepath
        args
            Compatibility
        _add_ext
            Add file extension or not.
        kwargs
            Compatibility
        """
        tmp_export, rkwarg = self._export(*args, **kwargs)
        if _add_ext:
            tmp_export.write("{}.fasta".format(output_fp), **rkwarg)
        else:
            tmp_export.write(output_fp, **rkwarg)

    @property
    def data(self) -> pd.DataFrame:
        """:class:`pandas.DataFrame` with sequence data"""
        return self.__sequence_df

    @property
    def xrid(self) -> pd.Index:
        """Feature identifiers."""
        return self.__sequence_df.index
