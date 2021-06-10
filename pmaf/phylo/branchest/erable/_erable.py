from pmaf.phylo.branchest._metakit import BranchEstimatorBackboneMetabase
from pmaf.sequence._metakit import MultiSequenceMetabase
from skbio.sequence.distance import hamming
from tempfile import mkdtemp,NamedTemporaryFile
from os import path
import pandas as pd
from io import StringIO
from pmaf.phylo.tree._metakit import PhyloTreeMetabase
from pmaf.phylo.tree._tree import PhyloTree
import subprocess
from pmaf.internal._shared import get_package_root

class BranchestERABLE(BranchEstimatorBackboneMetabase):
    ''' '''
    __ERABLE_BIN_FP = path.join(get_package_root(),'_externals','ERaBLE','erable')
    _cache_prefix = 'erable_'
    def __init__(self,cache_dir=None):
        if cache_dir is not None:
            if path.isdir(cache_dir):
                self.__cache_dir = mkdtemp(prefix=self._cache_prefix, dir=cache_dir)
            else:
                raise NotADirectoryError('`cache_dir` must be valid directory path.')
        else:
            self.__cache_dir = mkdtemp(prefix=self._cache_prefix)
        self.__bin_fp = path.join(path.dirname(path.realpath(__file__)),self.__ERABLE_BIN_FP)
        self.__last_output = None
        self.__last_error = None
        self.__last_rates = None

    def __repr__(self):
        class_name = self.__class__.__name__
        method_name = 'BranchEstimator-ERaBLE'
        bin_path = path.realpath(self.__bin_fp)
        repr_str = "<{}:[{}], Path: [{}]>".format(class_name,method_name, bin_path)
        return repr_str

    def _make_input_matrix(self,multiseq):
        '''

        Args:
          multiseq: 

        Returns:

        '''
        seq_names = multiseq.index
        dist = pd.DataFrame(index=seq_names, columns=seq_names, dtype='f')
        for sid_i, seq_i in multiseq.get_iter('skbio'):
            for sid_j, sed_j in multiseq.get_iter('skbio'):
                dist.loc[sid_i, sid_j] = hamming(seq_i, sed_j)
        tmp_io = StringIO()
        total_multiseqs = str(1)
        tmp_io.write("{}\n\n".format(total_multiseqs))
        seq_name = "%Sequence {}".format(str(multiseq.name))
        tmp_io.write("{}\n".format(seq_name))
        seq_details = "{} {}".format(str(multiseq.count), str(multiseq.sequences[0].length))
        tmp_io.write("{}\n".format(seq_details))
        dist_matrix = "{}".format(dist.to_string(header=False))
        tmp_io.write("{}\n".format(dist_matrix))
        tmp_io.seek(0,0)
        return tmp_io.read()


    def estimate(self, alignment, tree, **kwargs):
        '''

        Args:
          alignment: 
          tree: 
          **kwargs: 

        Returns:

        '''
        if isinstance(alignment,MultiSequenceMetabase) and isinstance(tree,PhyloTreeMetabase):
            if alignment.is_alignment:
                tmp_matrix_str = self._make_input_matrix(alignment)
                tmp_matrix_fp = NamedTemporaryFile(mode='w',dir=self.__cache_dir,delete=False)
                tmp_tree_fp = NamedTemporaryFile(mode='w', dir=self.__cache_dir,delete=False)
                tmp_matrix_fp.write(tmp_matrix_str)
                tmp_matrix_fp.flush()
                tree.write(tmp_tree_fp.name,tree_format=5,root_node=False)
                erable_cmd = [self.__bin_fp,"-i", tmp_matrix_fp.name, '-t', tmp_tree_fp.name]
                print(' '.join(erable_cmd))
                process = subprocess.Popen(erable_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                self.__last_output = output.decode() if isinstance(output, bytes) else output
                self.__last_error= error.decode() if isinstance(error, bytes) else error
                process.kill()
                tmp_new_tree_fp = '{}.lengths.nwk'.format(tmp_matrix_fp.name)
                tmp_new_rates_fp = '{}.rates.txt'.format(tmp_matrix_fp.name)
                with open(tmp_new_tree_fp,'r') as newick_file, open(tmp_new_rates_fp,'r') as rates_file:
                    self.__last_rates = rates_file.read()
                    return PhyloTree(newick_file.read())
            else:
                raise ValueError('`alignment` must be aligned.')
        else:
            raise TypeError('`alignment` or `tree` have invalid type.' )

    @property
    def last_out(self):
        ''' '''
        return self.__last_output
    @property
    def last_error(self):
        ''' '''
        return self.__last_error

    @property
    def last_rates(self):
        ''' '''
        return self.__last_rates





