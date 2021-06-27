import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from shutil import copyfile
from pmaf.sequence._metakit import (
    MultiSequenceMetabase,
    MultiSequenceStreamBackboneMetabase,
)
from pmaf.sequence._multiple._multiple import MultiSequence
from pmaf.sequence import _shared as seq_shared
from random import random
from pmaf.sequence._sequence._nucleotide import Nucleotide
from pmaf.sequence._metakit import NucleotideMetabase
from Bio import SeqIO
import tempfile
import pandas as pd
import tables
import pickle
import os


class MultiSequenceStream(MultiSequenceStreamBackboneMetabase):
    """:meta private:"""

    _temp_filename_suffix_maker = lambda self, path_with_preffix: "{}_pmaf_{}".format(
        path_with_preffix, str(round(100000000 * random()))
    )
    _supported_compression_libraries = ["zlib", "lzo", "bzip2", "blosc"]
    _default_seq_encoding = "ascii"
    _default_complevel = 5
    _default_path_list = ["/seq", "/meta", "/info"]
    _default_info_node_path = "/info/dump"
    _default_seqs_node_path = "/seq/seqs"
    _default_meta_node_path = "/meta/metas"

    def __init__(
        self,
        filepath=None,
        expected_rows=1000,
        mode="DNA",
        aligned=False,
        name=None,
        compressor=False,
    ):
        self._name = ""
        self._mode = None
        self._stream_filepath = None
        self._stream_storer = None
        self._temp_state = True if filepath is None else False
        self._stream_map = pd.Series(dtype=str)
        self._last_seq_length = None
        self._aligned = False
        self._compressor = None
        self._expected_rows = None
        restore_state = False
        if isinstance(aligned, bool):
            self._aligned = aligned
        else:
            raise TypeError("`aligned` must have bool type")
        if isinstance(expected_rows, int):
            if expected_rows > 0:
                self._expected_rows = expected_rows
            else:
                raise ValueError("`expected_rows` must be positive number")
        else:
            raise TypeError("`expected_rows` must have int type")
        if isinstance(compressor, str):
            if compressor in self._supported_compression_libraries:
                self._compressor = compressor
            else:
                raise ValueError(
                    "Compressor is not supported. Please use one of {}".format(
                        ",".join(self._supported_compression_libraries)
                    )
                )
        elif compressor == False:
            self._compressor = False
        else:
            raise TypeError("`compressor` must have string type. ")
        if isinstance(name, str):
            self._name = name
        elif name is None:
            pass
        else:
            raise TypeError("Name can be only string or None.")
        if isinstance(mode, str):
            if seq_shared.validate_seq_mode(mode):
                self._mode = mode.lower()
        else:
            raise ValueError("Sequence mode can only be 'DNA', 'RNA' or 'Protein'")
        if isinstance(filepath, str):
            self._stream_filepath = os.path.abspath(filepath)
            if os.path.exists(self._stream_filepath):
                restore_state = True
        elif filepath is None:
            tmp_temp_filepath = self._temp_filename_suffix_maker(
                os.path.join(tempfile.gettempdir(), tempfile.gettempprefix())
            )
            while os.path.exists(tmp_temp_filepath):
                tmp_temp_filepath = self._temp_filename_suffix_maker(
                    os.path.join(tempfile.gettempdir(), tempfile.gettempprefix())
                )
            self._stream_filepath = tmp_temp_filepath
        else:
            raise ValueError("`filepath` is invalid.")
        if restore_state:
            if not self._restore_init():
                raise RuntimeError("Cannot load file.")
        else:
            if not self._init_seq_stream_storer():
                raise RuntimeError("Cannot be initiate file.")

    def __repr__(self):
        class_name = self.__class__.__name__
        name = self._name if self._name is not None else "N/A"
        count = len(self._stream_map)
        stream_filepath = self._stream_filepath
        aligned = "Yes" if self._aligned else "No"
        repr_str = "<{}: {}, Total Sequences: {}, Filepath: {}, Aligned: {}>".format(
            class_name, name, count, stream_filepath, aligned
        )
        return repr_str

    def __exit__(self, exc_type, exc_value, traceback):
        if self._temp_state:
            os.unlink(self._stream_filepath)
        return

    def _init_seq_stream_storer(self):
        """"""
        ret = False
        try:
            tmp_filters = (
                tables.Filters(
                    complib=self._compressor, complevel=self._default_complevel
                )
                if self._compressor
                else None
            )
            tmp_stream_store = tables.open_file(
                self._stream_filepath, mode="a", title=self._name, filters=tmp_filters
            )
            tmp_stream_store.create_group("/", "seq", "Raw sequences")
            tmp_stream_store.create_vlarray(
                "/seq",
                "seqs",
                atom=tables.VLStringAtom(),
                expectedrows=self._expected_rows,
            )
            tmp_stream_store.create_group("/", "meta", "Sequence metadata")
            tmp_stream_store.create_vlarray(
                "/meta",
                "metas",
                atom=tables.ObjectAtom(),
                expectedrows=self._expected_rows,
            )
            tmp_stream_store.create_group("/", "info", "Instance attributes")
            tmp_stream_store.create_vlarray(
                "/info", "dump", atom=tables.ObjectAtom(), expectedrows=1
            )
            self._stream_storer = tmp_stream_store
            ret = True
        except:
            pass
        return ret

    def _restore_init(self):
        """"""
        ret = False
        try:
            tmp_stream_store_read = tables.open_file(self._stream_filepath, mode="r")
            group_list = []
            for group in tmp_stream_store_read.walk_groups():
                group_list.append(group._v_pathname)
            if all([group in group_list for group in self._default_path_list]):
                tmp_instance_dict_bytes = tmp_stream_store_read.get_node(
                    self._default_info_node_path
                ).read()[0]
                tmp_instance_dict = pickle.loads(tmp_instance_dict_bytes)
                self.__dict__.update(tmp_instance_dict)
                tmp_stream_store_read.close()
                tmp_filters = (
                    tables.Filters(
                        complib=self._compressor, complevel=self._default_complevel
                    )
                    if self._compressor
                    else None
                )
                tmp_stream_store = tables.open_file(
                    self._stream_filepath, mode="a", filters=tmp_filters
                )
                self._stream_storer = tmp_stream_store
                ret = True
        except:
            pass
        return ret

    def close(self, copy_filepath=None):
        """

        Parameters
        ----------
        copy_filepath :
            (Default value = None)

        Returns
        -------

        """
        tmp_instance_dict = {
            k: v
            for k, v in self.__dict__.items()
            if k not in ["_stream_filepath", "_stream_storer"]
        }
        tmp_instance_dict_bytes = pickle.dumps(tmp_instance_dict)
        self._stream_storer.get_node(self._default_info_node_path).remove()
        self._stream_storer.create_vlarray(
            "/info", "dump", atom=tables.ObjectAtom(), expectedrows=1
        )
        self._stream_storer.get_node(self._default_info_node_path).append(
            tmp_instance_dict_bytes
        )
        self._stream_storer.close()
        if copy_filepath is not None and isinstance(copy_filepath, str):
            if not os.path.exists(copy_filepath):
                copyfile(self._stream_filepath, copy_filepath)
            else:
                raise FileExistsError()
        if self._temp_state:
            os.unlink(self._stream_filepath)
        return

    def get_sequence_by_acc(self, acc_number):
        """

        Parameters
        ----------
        acc_number :


        Returns
        -------

        """
        ret = None
        if acc_number in self._stream_map.index:
            ret = self._get_sequence_by_acc_id(acc_number)
        return ret

    def get_multiseq_by_accs(self, acc_numbers):
        """

        Parameters
        ----------
        acc_numbers :


        Returns
        -------

        """
        ret = None
        if isinstance(acc_numbers, list):
            if len(acc_numbers) > 0:
                if self._stream_map.index.isin(acc_numbers).sum() == len(acc_numbers):
                    seq_list = []
                    for name in acc_numbers:
                        seq_list.append(self._get_sequence_by_acc_id(name))
                    ret = MultiSequence(
                        seq_list,
                        name=self._name,
                        aligned=self._aligned,
                        metadata={"accession-numbers": "; ".join(acc_numbers)},
                    )
        return ret

    def iter_sequences(self):
        """"""
        for acc_num in self._stream_map.index.values.tolist():
            yield self._get_sequence_by_acc_id(acc_num)

    def write_all_to_fasta(self, fasta_fp, write_in_chunks=100):
        """

        Parameters
        ----------
        fasta_fp :

        write_in_chunks :
            (Default value = 100)

        Returns
        -------

        """
        if not os.path.exists(fasta_fp):
            if isinstance(write_in_chunks, int):
                if write_in_chunks >= 0:
                    chunks = (
                        len(self._stream_map)
                        if write_in_chunks == 0
                        else write_in_chunks
                    )
                    from Bio.Seq import Seq

                    with open(fasta_fp, "a") as fasta_handle:
                        chunk_counter = chunks
                        records_chunk = []
                        for sequence in self.iter_sequences():
                            tmp_record_metadata = (
                                sequence.metadata["description"]
                                if "description" in sequence.metadata.keys()
                                else self._name
                            )
                            next_record = SeqIO.SeqRecord(
                                Seq(sequence.text),
                                sequence.name,
                                description=tmp_record_metadata,
                            )
                            if chunk_counter > 1:
                                records_chunk.append(next_record)
                                chunk_counter = chunk_counter - 1
                            else:
                                records_chunk.append(next_record)
                                chunk_counter = chunks
                                SeqIO.write(records_chunk, fasta_handle, "fasta")
                                records_chunk = []
                        if chunk_counter > 0:
                            SeqIO.write(records_chunk, fasta_handle, "fasta")
            else:
                raise TypeError("`write_in_chunks` must be integer.")
        else:
            raise FileExistsError("Target file must not exists.")
        return

    def _get_sequence_by_acc_id(self, accid):
        """

        Parameters
        ----------
        accid :


        Returns
        -------

        """
        seqid = self._accid_to_seqid(accid)
        seq_str = self._retrieve_seq_by_seqid(seqid)
        seq_meta_pack = self._retrieve_meta_by_seqid(seqid)
        tmp_seq = Nucleotide(seq_str, accid, mode=self._mode)
        tmp_seq.restore_buckle(seq_meta_pack)
        return tmp_seq

    def _accid_to_seqid(self, accid):
        """

        Parameters
        ----------
        accid :


        Returns
        -------

        """
        return self._stream_map[accid]

    def _retrieve_seq_by_seqid(self, seqid):
        """

        Parameters
        ----------
        seqid :


        Returns
        -------

        """
        tmp_seq_bytes = self._stream_storer.get_node(self._default_seqs_node_path)[
            seqid
        ]
        return tmp_seq_bytes.decode(self._default_seq_encoding)

    def _retrieve_meta_by_seqid(self, seqid):
        """

        Parameters
        ----------
        seqid :


        Returns
        -------

        """
        tmp_meta_bytes = self._stream_storer.get_node(self._default_meta_node_path)[
            seqid
        ]
        return pickle.loads(tmp_meta_bytes)

    def append_sequence(self, sequence):
        """

        Parameters
        ----------
        sequence :


        Returns
        -------

        """
        if isinstance(sequence, NucleotideMetabase):
            if isinstance(sequence, Nucleotide):
                if sequence.mode == self._mode:
                    if (sequence.name is not None) and (
                        sequence.name not in self._stream_map.index
                    ):
                        if self._verify_sequence(sequence.text):
                            self._append_sequence(sequence)
                            self._stream_storer.flush()
                        else:
                            raise ValueError("Sequences do not have same length.")
                    else:
                        raise ValueError(
                            "Sequence name must be unique and have legnth > 0."
                        )
                else:
                    raise ValueError("All sequences must have same mode.")
        else:
            raise TypeError("`sequence` have invalid type.")

    def _append_sequence(self, sequence_instance):
        """

        Parameters
        ----------
        sequence_instance :


        Returns
        -------

        """
        tmp_metadata = sequence_instance.buckle_for_uid(self._name)
        tmp_seq_str = sequence_instance.text
        seqid = self._insert_seq_vlarray(tmp_seq_str)
        metaid = self._insert_meta_vlarray(tmp_metadata)
        if seqid == metaid:
            self._stream_map[str(sequence_instance.name)] = seqid
        else:
            raise RuntimeError(
                "Impossible condition. Stream file might have been externally modified!"
            )
        return

    def extend_multiseq(self, multiseq):
        """

        Parameters
        ----------
        multiseq :


        Returns
        -------

        """
        if isinstance(multiseq, MultiSequenceMetabase):
            if multiseq.count > 0:
                if multiseq.mode == self._mode:
                    for sequence in multiseq.sequences:
                        if (sequence.name is None) or (
                            sequence.name in self._stream_map.index
                        ):
                            raise ValueError(
                                "Sequence name must be unique and have legnth > 0."
                            )
                        if not self._verify_sequence(sequence.text):
                            raise ValueError("Sequences do not have same length.")
                    self._append_multiseq(multiseq)
                    self._stream_storer.flush()
                else:
                    raise ValueError("All sequences must have same mode.")
        else:
            raise TypeError("`multiseq` have invalid type.")

    def _append_multiseq(self, multiseq):
        """

        Parameters
        ----------
        multiseq :


        Returns
        -------

        """
        for sequence in multiseq.sequences:
            self._append_sequence(sequence)
        return

    def append_string(self, name, mode, sequence_str, metadata_dict={}):
        """

        Parameters
        ----------
        name :

        mode :

        sequence_str :

        metadata_dict :
            (Default value = {})

        Returns
        -------

        """
        if (
            isinstance(name, str)
            and isinstance(sequence_str, str)
            and isinstance(metadata_dict, dict)
            and isinstance(mode, str)
        ):
            if mode == self._mode:
                if len(name) > 0 and (name not in self._stream_map.index):
                    if self._verify_sequence(sequence_str):
                        self._append_sequence_str(name, sequence_str, metadata_dict)
                        self._stream_storer.flush()
                    else:
                        raise ValueError("Sequences do not have same length.")
                else:
                    raise ValueError(
                        "Sequence name must be unique and have legnth > 0."
                    )
            else:
                raise ValueError("All sequences must have same mode.")
        else:
            raise TypeError("Invalid parameter types.")
        return

    def _append_sequence_str(self, seq_name, sequence_str, metadata_dict):
        """

        Parameters
        ----------
        seq_name :

        sequence_str :

        metadata_dict :


        Returns
        -------

        """
        seqid = self._insert_seq_vlarray(sequence_str)
        metaid = self._insert_meta_vlarray(metadata_dict)
        if seqid == metaid:
            self._stream_map[seq_name] = seqid
        else:
            raise RuntimeError(
                "Impossible condition. Stream file might have been externally modified!"
            )
        return

    def _insert_seq_vlarray(self, seq_data):
        """

        Parameters
        ----------
        seq_data :


        Returns
        -------

        """
        self._last_seq_length = len(seq_data)
        seq_data_bytes = seq_data.encode(self._default_seq_encoding)
        self._stream_storer.get_node(self._default_seqs_node_path).append(
            seq_data_bytes
        )
        return self._stream_storer.get_node(self._default_seqs_node_path).nrows - 1

    def _insert_meta_vlarray(self, metadata):
        """

        Parameters
        ----------
        metadata :


        Returns
        -------

        """
        metadata_bytes = pickle.dumps(metadata)
        self._stream_storer.get_node(self._default_meta_node_path).append(
            metadata_bytes
        )
        return self._stream_storer.get_node(self._default_meta_node_path).nrows - 1

    def _verify_sequence(self, seq_str):
        """

        Parameters
        ----------
        seq_str :


        Returns
        -------

        """
        ret = True
        if self._aligned:
            if self._last_seq_length is not None:
                if self._last_seq_length == len(seq_str):
                    ret = False
        return ret

    @property
    def name(self):
        """"""
        return self._name

    @property
    def mode(self):
        """"""
        return self._mode

    @property
    def count(self):
        """"""
        return len(self._stream_map)

    @property
    def summarize(self):
        """"""
        return

    @property
    def accession_numbers(self):
        """"""
        return self._stream_map.index.tolist()
