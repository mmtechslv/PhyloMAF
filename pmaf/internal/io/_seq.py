from pmaf.internal.io._metakit import FileIOBackboneMetabase
from Bio import SeqIO, SeqRecord
from os import path
from io import StringIO, IOBase
from skbio.io.registry import sniff
from typing import Union, Any, Sequence, Generator


class SequenceIO(FileIOBackboneMetabase):
    """Primary sequence data parser."""

    def __init__(
        self,
        seqsrc: Union[Sequence[str], str, IOBase],
        ftype: str = "auto",
        upper: bool = False,
        **kwargs: Any
    ):
        """Constructor for :class:`~.SequenceIO`.

        Parameters
        ----------
        seqsrc
            Can be one of following:
            - Path to sequence FASTA file with defined format(`ftype`).
            - List of paths to sequence files with defined format(`ftype`).
            - String with sequence data in defined format(`ftype`).
            - Opened IO instance(must inherit :class:`.IOBase`
        ftype
            Format of the sequence data like FASTA, FASTQ, etc.
            Default is "auto" - constructor will attempt to guess the type.
        upper
            Convert :term:`IUPAC` bases to uppercase.
        kwargs
            Compatibility.
        """
        if isinstance(seqsrc, (tuple, list)):
            if len(set([type(src) for src in seqsrc])) == 1:
                tmp_srcs = seqsrc
            else:
                raise ValueError(
                    "`seqsrc` when used as list or tuple must contain elements of same type."
                )
        else:
            tmp_srcs = [seqsrc]
        if all([isinstance(tmp_src, str) for tmp_src in tmp_srcs]):
            if all([path.isfile(tmp_src) for tmp_src in tmp_srcs]):
                tmp_sources = tmp_srcs
            else:
                tmp_sources = [StringIO(tmp_src) for tmp_src in tmp_srcs]
        elif all([isinstance(tmp_src, IOBase) for tmp_src in tmp_srcs]):
            tmp_sources = tmp_srcs
        else:
            raise TypeError("`seqsrc` has invalid type.")
        if ftype == "auto":
            tmp_file_formats = {sniff(tmp_src)[0] for tmp_src in tmp_sources}
            if len(tmp_file_formats) > 1:
                raise ValueError("`seqsrc` contain files of _multiple types.")
            else:
                tmp_file_format = tmp_file_formats.pop()
            if tmp_file_format not in ["fasta", "fastq"]:
                raise ValueError("File type is not supported.")
        elif ftype.lower() in ["fasta", "fastq"]:
            tmp_file_format = ftype
        else:
            raise ValueError("File type is not supported.")
        self.__upper = upper
        self.__type = tmp_file_format.lower()
        self.__srcs = tmp_sources

    def __fasta_parser_simple(
        self, id: bool = True, description: bool = True, sequence: bool = True
    ) -> Generator[tuple, None, None]:
        """Simplest parser/generator for sequence data.

        Parameters
        ----------
        id
            Yield sequence identifier
        description
            Yield sequence description
        sequence
            Yield the sequence string

        Yields
        ------
            ([id, description, sequence])
        """
        for src in self.__srcs:
            seq_parser = SeqIO.parse(src, self.__type)
            for seq_record in seq_parser:
                tmp_product = []
                if id:
                    tmp_product.append(seq_record.id)
                if description:
                    tmp_product.append(seq_record.description)
                if sequence:
                    if self.__upper:
                        tmp_product.append(str(seq_record.seq.upper()))
                    else:
                        tmp_product.append(str(seq_record.seq))
                yield tuple(tmp_product)

    def __fasta_parser_biopython(self) -> Generator:
        """BioPython parser/generator for sequence data.

        Yields
        ------
            Sequence record as :class:`~SeqRecord`.
        """
        for src in self.__srcs:
            seq_parser = SeqIO.parse(src, self.__type)
            for seq_record in seq_parser:
                if self.__upper:
                    yield seq_record.upper()
                else:
                    yield seq_record

    def pull_parser(self, parser: str = "simple", **kwargs: Any) -> Generator:
        """Create and get sequence parser/generator.

        Parameters
        ----------
        parser
            Requested parser type.
        **kwargs
            Compatibility

        Returns
        -------
            New instance of parser/generator for sequence data.
        """
        if parser == "simple":
            if self.__type == "fasta":
                return self.__fasta_parser_simple(**kwargs)
        elif parser == "biopython":
            if self.__type == "fasta":
                return self.__fasta_parser_biopython()
        else:
            raise ValueError("Invalid Parser.")

    @property
    def type(self) -> str:
        """Type of the sequence data."""
        return self.__type

    @property
    def src(self) -> Any:
        """Sequence source data."""
        return self.__srcs
