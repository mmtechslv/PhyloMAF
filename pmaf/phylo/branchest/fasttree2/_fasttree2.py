from pmaf.phylo.branchest._metakit import BranchEstimatorBackboneMetabase
from pmaf.sequence._metakit import MultiSequenceMetabase
from tempfile import mkdtemp,NamedTemporaryFile
from os import path
from pmaf.phylo.tree._metakit import PhyloTreeMetabase
from pmaf.phylo.tree._tree import PhyloTree
import subprocess
from pmaf.internal._shared import get_package_root

class BranchestFastTree2(BranchEstimatorBackboneMetabase):
    ''' '''
    __FASTTREE_BIN_FP =  path.join(get_package_root(),'_externals','FastTree2','fasttree')
    _cache_prefix = 'fasttree_'
    def __init__(self,cache_dir=None):
        if cache_dir is not None:
            if path.isdir(cache_dir):
                self.__cache_dir = mkdtemp(prefix=self._cache_prefix, dir=cache_dir)
            else:
                raise NotADirectoryError('`cache_dir` must be valid directory path.')
        else:
            self.__cache_dir = mkdtemp(prefix=self._cache_prefix)
        self.__bin_fp = path.join(path.dirname(path.realpath(__file__)),self.__FASTTREE_BIN_FP)
        self.__last_output = None
        self.__last_error = None

    def __repr__(self):
        class_name = self.__class__.__name__
        method_name = 'BranchEstimator-FastTree2'
        bin_path = path.realpath(self.__bin_fp)
        repr_str = "<{}:[{}], Path: [{}]>".format(class_name,method_name, bin_path)
        return repr_str

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
                tmp_aln_fp = NamedTemporaryFile(mode='r',dir=self.__cache_dir,delete=False)
                tmp_intree_fp = NamedTemporaryFile(mode='r', dir=self.__cache_dir,delete=False)
                alignment.write(tmp_aln_fp.name)
                tree.write(tmp_intree_fp.name,tree_format=5,root_node=False)
                fasttree2_cmd = [self.__bin_fp,"-nt", "-nome", "-mllen", '-intree',tmp_intree_fp.name, tmp_aln_fp.name]
                print(' '.join(fasttree2_cmd))
                process = subprocess.Popen(fasttree2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output, error = process.communicate()
                tmp_outtree_str = output.decode() if isinstance(output, bytes) else output
                self.__last_output = tmp_outtree_str
                self.__last_error= error.decode() if isinstance(error, bytes) else error
                process.kill()
                return PhyloTree(tmp_outtree_str)
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




