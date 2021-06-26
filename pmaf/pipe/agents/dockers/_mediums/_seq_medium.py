from pmaf.pipe.agents.dockers._metakit import DockerSequenceMetabase
from pmaf.pipe.agents.dockers._base import DockerBase
from pmaf.internal.io._seq import SequenceIO
from pmaf.sequence._multiple._multiple import MultiSequence
from pmaf.sequence._sequence._nucleotide import Nucleotide
from pmaf.sequence._metakit import (
    SequenceBackboneMetabase,
    MultiSequenceMetabase,
    NucleotideMetabase,
)
from pmaf.internal._shared import get_stats_for_sequence_record_df
from pmaf.sequence._shared import validate_seq_mode, validate_seq_grammar
from pmaf.internal._extensions._cpython._pmafc_extension._helper import (
    make_sequence_record_tuple,
)
import pandas as pd
import numpy as np
from collections import defaultdict
from typing import Optional, Union, Any, Dict

# TODO: Constructor is extremely ugly fix it after getting testing working.
class DockerSequenceMedium(DockerSequenceMetabase, DockerBase):
    """The :term:`docker` class responsible for handling sequence data."""

    _UNIT_TYPES = (str, type(None))

    def __init__(
        self,
        sequences: Union[
            str,
            MultiSequenceMetabase,
            NucleotideMetabase,
            pd.DataFrame,
            pd.Series,
            dict,
            list,
            "DockerSequenceMedium",
        ],
        mode: str = "DNA",
        aligned: Optional[bool] = None,
        **kwargs: Any
    ):  # TODO: Fix `aligned` make it only bool
        """Constructor.

        Parameters
        ----------
        sequences
            List-like or dict-like like sequence data where values are either
            sequences with types :attr:`.UNIT_TYPE` (singleton) or instances of :class:`.DockerSequenceMedium`
        kwargs
            Compatibility
        """
        if mode is not None:
            if validate_seq_mode(mode):
                mode_fixed = mode.lower()
            else:
                raise ValueError("`mode` is invalid.")
        else:
            mode_fixed = None
        if isinstance(sequences, self._UNIT_TYPES):
            tmp_sequences = defaultdict(str)
            seqio = SequenceIO(sequences, upper=True)
            for seq_id, seq_str in seqio.pull_parser(id=True, sequence=True):
                if validate_seq_grammar(seq_str, type):
                    tmp_sequences[seq_id] = seq_str
                else:
                    raise ValueError(
                        "`sequences` file contain sequences with invalid grammar."
                    )
        elif isinstance(sequences, MultiSequenceMetabase):
            tmp_sequences = {seq.name: seq for seq in sequences.sequences}
        elif isinstance(sequences, NucleotideMetabase):
            tmp_sequences = {sequences.name: sequences}
        elif isinstance(sequences, pd.DataFrame):
            tmp_sequences = sequences.loc[:, "sequence"].to_dict()
        elif isinstance(sequences, pd.Series):
            tmp_sequences = sequences.to_dict()
        elif isinstance(sequences, dict):
            tmp_sequences = sequences
        elif isinstance(sequences, list):
            tmp_sequences = {k: v for k, v in enumerate(sequences)}
        else:
            raise TypeError("`sequences` has invalid type.")
        if all(
            [
                isinstance(sequence, (SequenceBackboneMetabase, type(None)))
                for sequence in tmp_sequences.values()
            ]
        ):
            tmp_sequences_valid = {
                seq_id: seqs
                for seq_id, seqs in tmp_sequences.items()
                if seqs is not None
            }
            if len(tmp_sequences_valid) > 0:
                tmp_seq_modes_test = set(
                    [sequence.mode for sequence in tmp_sequences_valid.values()]
                    + ([mode_fixed] if mode_fixed is not None else [])
                )
                if len(tmp_seq_modes_test) != 1:
                    raise ValueError(
                        "`sequences` and/or specified mode does not match."
                    )
                if mode_fixed is None:
                    mode_fixed = tmp_seq_modes_test.pop()
                if all(
                    [
                        isinstance(sequence, MultiSequenceMetabase)
                        for sequence in tmp_sequences_valid.values()
                    ]
                ):
                    tmp_seq_algn_test = set(
                        [
                            sequence.is_alignment
                            for sequence in tmp_sequences_valid.values()
                        ]
                        + ([aligned] if aligned is not None else [])
                    )
                    if aligned is not None:
                        tmp_aligned = bool(aligned)
                        if len(tmp_seq_algn_test) != 1:
                            raise ValueError(
                                "`sequences` and/or specified alignment states does not match"
                            )
                    else:
                        tmp_aligned = tmp_seq_algn_test.pop()
                    tmp_sequences_adj = dict.fromkeys(tmp_sequences.keys(), None)
                    tmp_metadata_new = {}
                    for seq_id, seqs in tmp_sequences_valid.items():
                        tmp_sequences_adj[seq_id] = type(self)(
                            seqs,
                            mode=seqs.mode,
                            aligned=tmp_aligned,
                            name=seqs.name,
                            metadata=seqs.metadata,
                        )  # FIXME: FIND THE REASON OF THIS ISSUE
                elif all(
                    [
                        isinstance(sequence, NucleotideMetabase)
                        for sequence in tmp_sequences_valid.values()
                    ]
                ):
                    if aligned:
                        if (
                            len(
                                set(
                                    [
                                        sequence.length
                                        for sequence in tmp_sequences_valid.values()
                                    ]
                                )
                            )
                            == 1
                        ):
                            tmp_aligned = True
                        else:
                            raise ValueError(
                                "`sequences` must have same length if aligned."
                            )
                    else:
                        tmp_aligned = aligned
                    tmp_sequences_adj = dict.fromkeys(tmp_sequences.keys(), None)
                    tmp_metadata_new = {
                        "master-metadata": dict.fromkeys(tmp_sequences_valid.keys())
                    }
                    for seq_id, seqs in tmp_sequences_valid.items():
                        tmp_sequences_adj[seq_id] = seqs.text
                        tmp_metadata_new["master-metadata"][seq_id] = seqs.metadata
                else:
                    print([type(sequence) for sequence in tmp_sequences_valid.values()])
                    raise TypeError("`sequences` is not supported.")
            else:
                tmp_metadata_new = {}
                tmp_aligned = aligned
                tmp_sequences_adj = tmp_sequences
        else:
            tmp_metadata_new = {}
            tmp_aligned = aligned
            tmp_sequences_adj = tmp_sequences

        container_mode_test = any(
            [
                isinstance(data_elem, type(self))
                for data_elem in tmp_sequences_adj.values()
            ]
        )
        if container_mode_test:
            tmp_aligned_test = set()
            tmp_mode_test = set()
            for ix, tax_medium in tmp_sequences_adj.items():
                if isinstance(tax_medium, type(self)):
                    tmp_aligned_test.add(bool(tax_medium.aligned))
                    tmp_mode_test.add(
                        tax_medium.mode.lower() if tax_medium.mode is not None else None
                    )
            if tmp_aligned is not None:
                tmp_aligned_test.add(bool(tmp_aligned))
            if mode_fixed is not None:
                tmp_mode_test.add(mode_fixed)
            if len(tmp_aligned_test) > 1 or len(tmp_mode_test) > 1:
                raise ValueError(
                    "`sequences` must have same attributes for container usage."
                )
            tmp_aligned_adj = tmp_aligned_test.pop()
            tmp_mode = tmp_mode_test.pop()
        else:
            tmp_aligned_adj = tmp_aligned
            tmp_mode = mode_fixed
        tmp_metadata = {**tmp_metadata_new, **kwargs.pop("metadata", {})}
        super().__init__(
            _data_dict=tmp_sequences_adj,
            _valid_types=self._UNIT_TYPES,
            metadata=tmp_metadata,
            **kwargs
        )
        self.__mode = tmp_mode
        self.__aligned = bool(tmp_aligned_adj)

    @property
    def mode(self):
        """Mode/type of the sequence."""
        return self.__mode

    @property
    def aligned(self):
        """Whether sequences are alignments or not."""
        return self.__aligned

    def to_multiseq(
        self, indices: Optional[np.ndarray] = None
    ) -> Union[MultiSequence, Dict[Union[str, int], Optional[MultiSequence]]]:
        """Convert internal data to :class:`.MultiSequence` instance.

        Parameters
        ----------
        indices
            Target indices or None for all

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`.MultiSequence`
            if not :term:`singleton` then return dictionary with values :meth:`.to_multiseq`
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
            tmp_sequences = []
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_sequences.append(
                        Nucleotide(
                            self.data[ix],
                            name=ix,
                            mode=self.__mode,
                            metadata={"taxid": ix},
                        )
                    )
            return MultiSequence(
                tmp_sequences,
                name=self.name,
                metadata=self.metadata,
                internal_id="taxid",
                aligned=self.__aligned,
            )
        else:
            tmp_sequences_dict = dict.fromkeys(target_indices, None)
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_sequences_dict[ix] = self.data[ix].to_multiseq()
            return (
                next(iter(tmp_sequences_dict.values()))
                if np.isscalar(indices)
                else tmp_sequences_dict
            )

    def get_records(
        self, indices: Optional[np.ndarray] = None, exclude_missing: bool = False
    ) -> Union[tuple, Dict[Union[str, int], Optional[tuple]]]:
        """Get sequence records produced by :func:`.make_sequence_record_tuple`

        Parameters
        ----------
        indices
            Target element indices
        exclude_missing
            Exclude misssing data

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the sequence record tuples
            if not :term:`singleton` then return dictionary with values :meth:`.get_records`
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
            tmp_records = []
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_records.append(make_sequence_record_tuple(ix, self.data[ix]))
            return tmp_records
        else:
            tmp_records_dict = dict.fromkeys(target_indices, None)
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_records_dict[ix] = self.data[ix].get_records(
                        exclude_missing=exclude_missing
                    )
            return (
                next(iter(tmp_records_dict.values()))
                if np.isscalar(indices)
                else tmp_records_dict
            )

    def get_stats(
        self, indices: Optional[np.ndarray] = None, exclude_missing: bool = False
    ) -> Union[pd.DataFrame, Dict[Union[str, int], Optional[pd.DataFrame]]]:
        """Get sequence statistics.

        Parameters
        ----------
        indices
            Target indices or None for all
        exclude_missing
            Exclude missing data

        Returns
        -------
            If :term:`docker` is :term:`singleton` then return the :class:`pandas.DataFrame`
            if not :term:`singleton` then return dictionary with values :meth:`.get_stats`
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
            tmp_records = []
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_records.append(make_sequence_record_tuple(ix, self.data[ix]))
            tmp_records_df = pd.DataFrame.from_records(
                tmp_records, columns=["rid", "sequence", "length", "tab"], index=["rid"]
            )
            return get_stats_for_sequence_record_df(tmp_records_df)
        else:
            tmp_stats_dict = dict.fromkeys(target_indices, None)
            for ix in target_indices:
                if self.data[ix] is not None:
                    tmp_stats_dict[ix] = self.data[ix].get_stats(
                        exclude_missing=exclude_missing
                    )
            return (
                next(iter(tmp_stats_dict.values()))
                if np.isscalar(indices)
                else tmp_stats_dict
            )
