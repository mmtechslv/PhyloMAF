from ._metakit import FileIOBackboneMetabase
from Bio import SeqIO
from os import path
from io import StringIO,IOBase
from skbio.io.registry import sniff

class SequenceIO(FileIOBackboneMetabase):
    ''' '''
    def __init__(self, seqsrc, ftype='auto', upper=False, **kwargs):
        if isinstance(seqsrc,(tuple,list)):
            if len(set([type(src) for src in seqsrc]))==1:
                tmp_srcs = seqsrc
            else:
                raise ValueError('`seqsrc` when used as list or tuple must contain elements of same type.')
        else:
            tmp_srcs = [seqsrc]
        if all([isinstance(tmp_src,str) for tmp_src in tmp_srcs]):
            if all([path.isfile(tmp_src) for tmp_src in tmp_srcs]):
                tmp_sources = tmp_srcs
            else:
                tmp_sources = [StringIO(tmp_src) for tmp_src in tmp_srcs]
        elif all([isinstance(tmp_src,IOBase) for tmp_src in tmp_srcs]):
            tmp_sources = tmp_srcs
        else:
            raise TypeError('`seqsrc` has invalid type.')
        if ftype == 'auto':
            tmp_file_formats = {sniff(tmp_src)[0] for tmp_src in tmp_sources}
            if len(tmp_file_formats)>1:
                raise ValueError('`seqsrc` contain files of multiple types.')
            else:
                tmp_file_format = tmp_file_formats.pop()
            if tmp_file_format not in ['fasta','fastq']:
                raise ValueError('File type is not supported.')
        elif ftype.lower() in ['fasta','fastq']:
            tmp_file_format = ftype
        else:
            raise ValueError('File type is not supported.')
        self.__upper = upper
        self.__type = tmp_file_format.lower()
        self.__srcs = tmp_sources

    def __fasta_parser_simple(self,id=True,description=True,sequence=True):
        for src in self.__srcs:
            seq_parser = SeqIO.parse(src,self.__type)
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

    def __fasta_parser_biopython(self):
        for src in self.__srcs:
            seq_parser = SeqIO.parse(src, self.__type)
            for seq_record in seq_parser:
                if self.__upper:
                    yield seq_record.upper()
                else:
                    yield seq_record

    def pull_parser(self,parser='simple',**kwargs):
        '''

        Args:
          parser: (Default value = 'simple')
          **kwargs: 

        Returns:

        '''
        if parser == 'simple':
            if self.__type == 'fasta':
                return self.__fasta_parser_simple(**kwargs)
        elif parser == 'biopython':
            if self.__type == 'fasta':
                return self.__fasta_parser_biopython()
        else:
            raise ValueError('Invalid Parser.')

    @property
    def type(self):
        ''' '''
        return self.__type

    @property
    def src(self):
        ''' '''
        return self.__src
