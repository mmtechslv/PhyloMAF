from pmaf.sequence._metakit import MultiSequenceMetabase
from pmaf.sequence._multiple._multiple import MultiSequence
from pmaf.alignment._multiple._metakit import MultiSequenceAlignerBackboneMetabase
from . import _defined_aligners as aligners
from skbio import TabularMSA
from tempfile import NamedTemporaryFile

class MultiSequenceAligner(MultiSequenceAlignerBackboneMetabase):
    """ """
    def __init__(self, name=None, method='clustalw2', bin_fp=None):
        if isinstance(name,(str,type(None))):
            self.__name = name
        else:
            raise TypeError('`name` has invalid type.')
        self.__bin_fp = bin_fp
        if isinstance(method,str):
            tmp_aligner_func_name = "{}_wrapper".format(method)
            if tmp_aligner_func_name in dir(aligners):
                self.__aligner = getattr(aligners, tmp_aligner_func_name)
                self.__alinger_name = method
            else:
                raise ValueError('`method` was not found.')
        else:
            raise TypeError('`method` has invalid type.')
        self.__last_std_out = None
        self.__last_std_error = None

    def __repr__(self):
        class_name = self.__class__.__name__
        method = self.__alinger_name
        bin_path = 'Default' if self.__bin_fp is None else self.__bin_fp
        repr_str = "<{}:[{}], Path: [{}]>".format(class_name, method,bin_path)
        return repr_str

    def align(self, input, **kwargs):
        """

        Parameters
        ----------
        input :
            
        **kwargs :
            

        Returns
        -------

        """
        if isinstance(input, MultiSequenceMetabase):
            with NamedTemporaryFile(mode='w+') as tmp_fasta_io, NamedTemporaryFile(mode='r+') as tmp_aln_io:
                packed_metadata = input.buckle_for_alignment()
                input.write(tmp_fasta_io.name,format='fasta')
                tmp_fasta_io.file.seek(0)
                if self.__bin_fp is None:
                    stdout, stderr, file_format = self.__aligner(tmp_fasta_io,tmp_aln_io)
                else:
                    stdout, stderr, file_format = self.__aligner(tmp_fasta_io, tmp_aln_io,cmd_bin=self.__bin_fp)
                tmp_aln_io.file.seek(0)
                skbio_msa = TabularMSA.read(tmp_aln_io.file, format=file_format, constructor=input.skbio_mode)
                skbio_dict = skbio_msa.to_dict()
                for ix in skbio_dict.keys():
                    skbio_dict[ix].metadata['id'] = ix
                aligned_multiseq = MultiSequence.from_buckled(list(skbio_dict.values()),packed_metadata,aligned=True)
                self.__last_std_out = stdout
                self.__last_std_error = stderr
                self.__last_alignment = aligned_multiseq
                return aligned_multiseq
        else:
            raise TypeError('`multiseq` has invalid type.')

    @property
    def last_alignment(self):
        """ """
        return self.__last_alignment

    @property
    def last_std_out(self):
        """ """
        return self.__last_std_out

    @property
    def last_std_error(self):
        """ """
        return self.__last_std_error

    @property
    def aligner(self):
        """ """
        return self.__alinger_name

    @property
    def name(self):
        """ """
        return self.__name

    @property
    def bin_filepath(self):
        """ """
        return self.__bin_fp

