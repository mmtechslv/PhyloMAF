import warnings

warnings.simplefilter("ignore", category=FutureWarning)
from pmaf.internal.io._seq import SequenceIO
from pmaf.sequence._shared import (
    validate_seq_mode,
    mode_as_str,
    mode_as_skbio,
    sniff_mode,
)
from pmaf.sequence._metakit import NucleotideMetabase
from skbio.sequence import GrammaredSequence, DNA, RNA, Protein
from io import StringIO, IOBase
import copy
from numpy import isscalar
from typing import Union, Optional, Sequence, Any


class Nucleotide(NucleotideMetabase):
    """Class that represent single nucleotide sequence."""

    def __init__(
        self,
        sequence: Union[GrammaredSequence, str],
        name: Optional[str] = None,
        metadata: Optional[dict] = None,
        mode: str = "DNA",
        **kwargs: Any
    ):
        """Constructor for the :class:`.Nucleotide`.

        Parameters
        ----------
        sequence
            Sequence data
        name
            Name of the sequence instance
        metadata
            Metadata of the sequence instance
        mode
            Sequence type/mode of the new instance # TODO: Validation currently passes "protein" fix it.
        kwargs
            Compatibility
        """
        if name is None or isscalar(name):
            tmp_name = name
        else:
            raise TypeError("`name` can be any scalar or None")
        if isinstance(metadata, dict):
            tmp_metadata = metadata
        elif metadata is None:
            tmp_metadata = {}
        else:
            raise TypeError("`metadata` can be dict or None")
        if mode is not None:
            if validate_seq_mode(mode):
                tmp_mode = mode.lower()
            else:
                raise ValueError("`mode` is invalid.")
        else:
            if isinstance(sequence, GrammaredSequence):
                tmp_mode = mode_as_str(type(sequence))
            else:
                tmp_mode = None
        if isinstance(sequence, GrammaredSequence):
            tmp_sequence_str = str(sequence).upper()
            tmp_metadata = {**sequence.metadata, **tmp_metadata}
            if tmp_name is None:
                tmp_name = sequence.metadata.get("id", None)
        elif isinstance(sequence, str):
            tmp_sequence_str = sequence.upper()
        else:
            raise TypeError("`sequence` has invalid type.")
        if tmp_mode is None:
            tmp_skbio_type = sniff_mode(tmp_sequence_str)
        else:
            tmp_skbio_type = mode_as_skbio(tmp_mode)
        self.__sequence = tmp_skbio_type(tmp_sequence_str)
        self.__mode = mode_as_str(tmp_skbio_type)
        self.__skbio_mode = tmp_skbio_type
        if tmp_name is not None:
            self.__sequence.metadata["id"] = tmp_name
        self.__metadata = tmp_metadata
        self.__name = tmp_name
        self.__buckled = bool(kwargs.get("buckled", None))

    def __repr__(self):
        class_name = self.__class__.__name__
        name = self.__name if self.__name is not None else "N/A"
        length = len(self.__sequence)
        metadata_state = "Present" if len(self.__metadata) > 0 else "N/A"
        mode = self.__mode.upper() if self.__mode is not None else "N/A"
        repr_str = "<{}:[{}], Name:[{}], Mode:[{}], Metadata:[{}]>".format(
            class_name, length, name, mode, metadata_state
        )
        return repr_str

    def buckle_by_uid(self, uid: str) -> dict:
        """Buckle sequences based on unique identifier `uid`. Sequence are
        usually buckled prior to alignment in order to not loose sequence
        specific metadata  during alignment process.

        Parameters
        ----------
        uid
            Unique identifier string.

        Returns
        -------
           Packed metadata of current nucleotide instance for backup.
        """
        if not self.__buckled:
            packed_metadata = {
                "master-metadata": self.__metadata,
                "__name": self.__name,
            }
            self.__name = uid
            self.__sequence.metadata["id"] = uid
            self.__buckled = True
            return packed_metadata
        else:
            raise RuntimeError("Nucleotide instance is already buckled.")

    def unbuckle_uid(self) -> str:
        """Retrieve unique identifier assigned during buckling.

        Returns
        -------
            If instance is buckled the return the `uid`. Otherwise raise error.
        """
        if self.__buckled:
            return self.__sequence.metadata["id"]
        else:
            raise RuntimeError("Nucleotide instance is not buckled.")

    def restore_buckle(self, buckled_pack: dict) -> None:
        """Restore the buckle using packed metadata `buckle_pack`

        Parameters
        ----------
        buckled_pack
            Packed metadata backed up during bucking process

        Returns
        -------
            None if success otherwise error.
        """
        if self.__buckled:
            if isinstance(buckled_pack, dict):
                if len(buckled_pack) > 0:
                    self.__name = buckled_pack["__name"]
                    self.__sequence.metadata["id"] = buckled_pack["__name"]
                    self.__metadata.update(buckled_pack["master-metadata"])
                else:
                    ValueError("`buckled_pack` is empty.")
            else:
                TypeError("`buckled_pack` has invalid type.")
        else:
            raise RuntimeError("Nucleotide instance is not buckled.")

    def get_string_as(self, format: str = "fasta", **kwargs: Any) -> str:
        """Get string of the sequence.

        Parameters
        ----------
        format
            Format of the string to retrieve
        kwargs
            Compatibility


        Returns
        -------
            Formatted sequence data as string
        """
        with StringIO() as tmp_buffer_io:
            self.__write_by_handle(tmp_buffer_io, format=format, **kwargs)
            return tmp_buffer_io.getvalue()

    def write(
        self, file: Union[str, IOBase], format: str = "fasta", **kwargs: Any
    ) -> None:
        """Write sequence data to the file.

        Parameters
        ----------
        file
            File path or IO stream to write into
        format
            Format of the output file
        kwargs
            Compatibility
        """
        self.__write_by_handle(file, format=format, **kwargs)

    def __write_by_handle(self, file, format, mode="w", **kwargs):
        """Write into the IO handler."""
        self.__sequence.metadata = self.__metadata
        self.__sequence.metadata["id"] = self.__name
        if isinstance(file, IOBase):
            if file.writable():
                if mode[0] == "a":
                    file.seek(0, 2)
                elif mode[0] == "w":
                    file.seek(0, 0)
                else:
                    raise ValueError("`mode` has invalid value.")
            else:
                raise ValueError("`file` must be writable.")
            tmp_file = file
        elif isinstance(file, str):
            tmp_file = open(file, mode)
        else:
            raise ValueError("`file` is invalid.")
        with StringIO() as tmp_io:  # This is done to compensate skbio bug. Skbio writer does not recogine mode kwarg properly.
            self.__sequence.write(tmp_io, format=format, **kwargs)
            tmp_io.seek(0, 0)
            tmp_file.write(tmp_io.read())
        self.__sequence.metadata = {"id": self.__name}

    def complement(self):
        """Return the sequence complement as new instance."""
        seq_complement = str(self.__sequence.complement())
        return type(self)(
            seq_complement, name=self.__name, metadata=self.__metadata, mode=self.__mode
        )

    def copy(self):
        """Copy of the current instance."""
        return copy.deepcopy(self)

    @classmethod
    def read(
        cls,
        file: Any,
        name: Optional[str] = None,
        metadata: Optional[dict] = None,
        mode: str = "DNA",
        **kwargs: any
    ) -> "Nucleotide":
        """Factory class that reads the sequence data.

        Parameters
        ----------
        file
            Unspecified data for sequence.
            Can be file path, IO stream, string, etc.
        name
            Name of the sequence instance
        metadata
            Metadata for the sequence instance
        mode
            Sequence type/mode can be 'DNA' or 'RNA'
        kwargs
            Compatibility

        Returns
        -------
            Return new instance of :class:`.Nucleotide`
        """
        if isinstance(name, (str, int, type(None))):
            tmp_name = name
        else:
            raise TypeError("`name` can be str, int or None")
        if isinstance(metadata, dict):
            tmp_metadata = metadata
        elif metadata is None:
            tmp_metadata = {}
        else:
            raise TypeError("`metadata` can be dict or None")
        seq_gen = SequenceIO(file, upper=True).pull_parser(
            parser="simple", id=True, description=True, sequence=True
        )
        tmp_sequence_str = ""
        for sid, desc, seq_str in seq_gen:
            if len(tmp_sequence_str) == 0:
                tmp_sequence_str = seq_str
                if not "description" in tmp_metadata.keys():
                    tmp_metadata.update({"description": desc})
                if tmp_name is None:
                    tmp_name = sid
            else:
                raise ValueError(
                    "`sequence` must contain only one sequence. For _multiple sequence reads use MultiSequence."
                )
        return cls(
            tmp_sequence_str, name=tmp_name, metadata=tmp_metadata, mode=mode, **kwargs
        )

    @property
    def skbio(self) -> GrammaredSequence:
        """The :mod:`skbio` representation of the sequence as
        :class:`skbio.sequence.GrammaredSequence`"""
        return self.__sequence

    @property
    def text(self) -> str:
        """Sequence as string."""
        return str(self.__sequence)

    @property
    def metadata(self) -> dict:
        """Sequence instance metadata."""
        return self.__metadata

    @property
    def mode(self) -> str:
        """Sequence instance mode/type."""
        return self.__mode

    @property
    def skbio_mode(self) -> Union[DNA, RNA, Protein]:
        """The :mod:`skbio` mode of the sequence."""
        return self.__skbio_mode

    @property
    def length(self) -> int:
        """Length of the sequence."""
        return len(self.__sequence)

    @property
    def name(self) -> str:
        """Name of the sequence instance."""
        return self.__name

    @name.setter
    def name(self, value):
        """Name of the instance."""
        self.__name = value

    @property
    def is_buckled(self) -> bool:
        """Is sequence instance is buckled or not."""
        return self.__buckled
