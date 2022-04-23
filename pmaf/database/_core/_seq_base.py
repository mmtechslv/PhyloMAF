import pandas as pd

from pmaf.database._metakit import DatabaseSequenceMetabase
from pmaf.sequence import Nucleotide, MultiSequence, MultiSequenceStream
import numpy as np
from pmaf.internal._typing import AnyGenericIdentifier
from typing import Optional, Tuple, Generator, Any, Union


class DatabaseSequenceMixin(DatabaseSequenceMetabase):
    """Mixin class for handling sequence data."""

    def get_sequence_by_tid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        subs: bool = False,
        iterator: bool = True,
        like: str = "multiseq",
        chunksize: int = 100,
    ) -> Union[Generator, Any]:
        """Get representative sequence for :term:`tids`

        Parameters
        ----------
        ids
            Target :term:`tids`
        subs :
            Whether to include :term:`subs`
        iterator :
            Whether to produce chunked generator. Default is True
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        chunksize :
            Chunk size. Default 100 records per chunk.

        Returns
        -------
            Depends on `like` parameter.
        """
        if self.storage_manager.state == 1:
            repseq_map_gen = self.find_rid_by_tid(ids, subs, True)
            if iterator:
                return {
                    tid: self._iter_repseq_by_rid(rid_list, like, tid, False, chunksize)
                    for tid, rid_list in repseq_map_gen
                }
            else:
                return {
                    tid: next(
                        self._iter_repseq_by_rid(rid_list, like, tid, False, None)
                    )[1]
                    for tid, rid_list in repseq_map_gen
                }
        else:
            raise RuntimeError("Storage is closed.")

    def get_alignment_by_tid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        subs: bool = False,
        iterator: bool = True,
        like: str = "multiseq",
        chunksize: int = 100,
    ) -> Union[Generator, Any]:
        """Get representative alignments for :term:`tids`

        Parameters
        ----------
        ids
            Target :term:`tids`
        subs :
            Whether to include :term:`subs`
        iterator :
            Whether to produce chunked generator. Default is True
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        chunksize :
            Chunk size. Default 100 records per chunk.

        Returns
        -------
            Depends on `like` parameter
            .
        """
        if self.storage_manager.state == 1:
            repseq_map_gen = self.find_rid_by_tid(ids, subs, True)
            if iterator:
                return {
                    tid: self._iter_repseq_by_rid(rid_list, like, tid, True, chunksize)
                    for tid, rid_list in repseq_map_gen
                }
            else:
                return {
                    tid: next(
                        self._iter_repseq_by_rid(rid_list, like, tid, True, None)
                    )[1]
                    for tid, rid_list in repseq_map_gen
                }
        else:
            raise RuntimeError("Storage is closed.")

    def get_sequence_by_rid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        iterator: bool = True,
        like: str = "multiseq",
        chunksize: int = 300,
    ) -> Union[Generator, Any]:
        """Get representative sequence for :term:`rids`

        Parameters
        ----------
        ids
            Target :term:`rids`
        iterator :
            Whether to produce chunked generator. Default is True
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        chunksize :
            Chunk size. Default 300 records per chunk.

        Returns
        -------
            Depends on `like` parameter.
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = np.asarray(self.xrid)
            else:
                target_ids = np.asarray(ids)
            if iterator:
                return self._iter_repseq_by_rid(
                    target_ids, like, None, False, chunksize
                )
            else:
                return next(
                    self._iter_repseq_by_rid(target_ids, like, None, False, None)
                )[1]
        else:
            raise RuntimeError("Storage is closed.")

    def get_alignment_by_rid(
        self,
        ids: Optional[AnyGenericIdentifier] = None,
        iterator: bool = True,
        like: str = "multiseq",
        chunksize: int = 300,
    ) -> Union[Generator, Any]:
        """Get representative alignments for :term:`rids`

        Parameters
        ----------
        ids
            Target :term:`rids`
        iterator :
            Whether to produce chunked generator. Default is True
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        chunksize :
            Chunk size. Default 300 records per chunk.

        Returns
        -------
            Depends on `like` parameter.
        """
        if self.storage_manager.state == 1:
            if ids is None:
                target_ids = np.asarray(self.xrid)
            else:
                target_ids = np.asarray(ids)
            if iterator:
                return self._iter_repseq_by_rid(target_ids, like, None, True, chunksize)
            else:
                return next(
                    self._iter_repseq_by_rid(target_ids, like, None, True, None)
                )[1]
        else:
            raise RuntimeError("Storage is closed.")

    def _retrieve_repseq_by_rid(
        self,
        repseq_ids: AnyGenericIdentifier,
        like: str,
        seq_name: str,
        alignment: bool,
    ) -> Any:
        """

        Parameters
        ----------
        repseq_ids
            Target :term:`rids`
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        seq_name
            Sequence object name (for 'multiseq')
        alignment
            Indicate whether alignments should be retrieved

        Returns
        -------
            Depend on the result of `like` parameter

        """
        if len(repseq_ids) > 0:
            tmp_repseq_df = self.storage_manager.get_element_data_by_ids(
                "sequence-representative" if not alignment else "sequence-aligned",
                repseq_ids,
            )
            if like == "multiseq":
                tmp_repseq_transformed = tmp_repseq_df.apply(
                    lambda seq: Nucleotide(
                        seq["sequence"],
                        name=int(seq.name),
                        mode="DNA",
                        metadata=seq[seq.index != "sequence"].to_dict(),
                    ),
                    axis=1,
                ).values.tolist()
                return MultiSequence(
                    tmp_repseq_transformed,
                    name=seq_name,
                    aligned=False if not alignment else True,
                )
            elif like == "stream":
                tmp_seq_stream = MultiSequenceStream(
                    name=seq_name,
                    expected_rows=len(repseq_ids),
                    aligned=False if not alignment else True,
                )
                tmp_repseq_transformed = tmp_repseq_df.apply(
                    lambda seq: Nucleotide(
                        seq["sequence"],
                        name=int(seq.name),
                        mode="DNA",
                        metadata=seq[seq.index != "sequence"].to_dict(),
                    ),
                    axis=1,
                ).values.tolist()
                tmp_multiseq = MultiSequence(
                    tmp_repseq_transformed,
                    name=seq_name,
                    aligned=False if not alignment else True,
                )
                tmp_seq_stream.extend_multiseq(tmp_multiseq)
                return tmp_seq_stream
            elif like == "asis":
                return tmp_repseq_df
            elif like == "seqlist":
                tmp_repseq_transformed = tmp_repseq_df.apply(
                    lambda seq: Nucleotide(
                        seq["sequence"],
                        name=int(seq.name),
                        metadata=seq[seq.index != "sequence"].to_dict(),
                    ),
                    axis=1,
                ).values.tolist()
                return tmp_repseq_transformed
            elif like == "tuples":
                tmp_repseq_transformed = tuple(
                    zip(
                        tmp_repseq_df.index.tolist(),
                        *zip(*tmp_repseq_df.values.tolist())
                    )
                )
                return tmp_repseq_transformed
        else:
            return None

    def _iter_repseq_by_rid(
        self,
        repseq_ids: AnyGenericIdentifier,
        like: str,
        seq_name: str,
        alignment: bool,
        chunksize: int,
    ):
        """Iterator for target data.

        Parameters
        ----------
        repseq_ids
            Target :term:`rids`
        like
            Result type can be 'multiseq'(default), 'stream', 'asis', 'seqlist' or 'tuples'.
        seq_name
            Sequence name if `multiseq`
        alignment
            Indicate whether alignments should be retrieved.
        chunksize
            Size of chunks to yield

        Yields
        -------
            ('Chunk Rids', 'Chunk Sequence Data')
        """
        if len(repseq_ids) > 0:
            chunksize_fixed = chunksize if chunksize is not None else len(repseq_ids)
            rid_chunks = [
                repseq_ids[i : i + chunksize_fixed]
                for i in range(0, len(repseq_ids), chunksize_fixed)
            ]
            for rid_chunk in rid_chunks:
                yield tuple(rid_chunk), self._retrieve_repseq_by_rid(
                    rid_chunk,
                    like,
                    int(seq_name) if seq_name is not None else seq_name,
                    alignment,
                )
        else:
            yield None, None
