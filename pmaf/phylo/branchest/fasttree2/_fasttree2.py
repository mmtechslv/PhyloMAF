from pmaf.phylo.branchest._metakit import BranchEstimatorBackboneMetabase
from pmaf.sequence._metakit import MultiSequenceMetabase
from tempfile import mkdtemp, NamedTemporaryFile
from os import path
from pmaf.phylo.tree._metakit import PhyloTreeMetabase
from pmaf.phylo.tree._tree import PhyloTree
import subprocess
from typing import Optional, Any


class BranchestFastTree2(BranchEstimatorBackboneMetabase):
    """Branch estimator for phylogenetic trees."""

    _cache_prefix = "fasttree_"

    def __init__(
        self, bin_fp: Optional[str] = "fasttree", cache_dir: Optional[str] = None
    ):
        """FastTree infers approximately-maximum-likelihood phylogenetic trees from alignments of nucleotide or protein sequences. :cite:t:`priceFastTreeApproximatelyMaximumLikelihood2010`

        Args:
            bin_fp: Path to 'fasttree' executable or None for default.
            cache_dir: Cache directory to use or None for seamless caching.
        """
        if cache_dir is not None:
            if path.isdir(cache_dir):
                self.__cache_dir = mkdtemp(prefix=self._cache_prefix, dir=cache_dir)
            else:
                raise NotADirectoryError("`cache_dir` must be valid directory path.")
        else:
            self.__cache_dir = mkdtemp(prefix=self._cache_prefix)
        self.__bin_fp = path.realpath(bin_fp)
        self.__last_output = None
        self.__last_error = None

    def __repr__(self):
        class_name = self.__class__.__name__
        method_name = "BranchEstimator-FastTree2"
        bin_path = self.__bin_fp
        repr_str = "<{}:[{}], Path: [{}]>".format(class_name, method_name, bin_path)
        return repr_str

    def estimate(
        self, alignment: MultiSequenceMetabase, tree: PhyloTree, **kwargs: Any
    ) -> PhyloTree:
        """Estimate branches of on fixed tree topology(param `tree`) using MSA of representative sequences(param `alignment`)

        Args:
            alignment: MSA alignment of representative sequences
            tree: Phylogenetic tree topology.
            **kwargs: Compatibility

        Returns:
            Phylogenetic tree with estimated branches

        """
        if not isinstance(alignment, MultiSequenceMetabase) and isinstance(
            tree, PhyloTreeMetabase
        ):
            raise TypeError("`alignment` or `tree` have invalid type.")
        if not alignment.is_alignment:
            raise ValueError("`alignment` must be aligned.")
        tmp_aln_fp = NamedTemporaryFile(mode="r", dir=self.__cache_dir, delete=False)
        tmp_intree_fp = NamedTemporaryFile(mode="r", dir=self.__cache_dir, delete=False)
        alignment.write(tmp_aln_fp.name)
        tree.write(tmp_intree_fp.name, tree_format=5, root_node=False)
        fasttree2_cmd = [
            self.__bin_fp,
            "-nt",
            "-nome",
            "-mllen",
            "-intree",
            tmp_intree_fp.name,
            tmp_aln_fp.name,
        ]
        print(" ".join(fasttree2_cmd))
        process = subprocess.Popen(
            fasttree2_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        tmp_outtree_str = output.decode() if isinstance(output, bytes) else output
        self.__last_output = tmp_outtree_str
        self.__last_error = error.decode() if isinstance(error, bytes) else error
        process.kill()
        return PhyloTree(tmp_outtree_str)

    @property
    def last_out(self):
        """Latest Output"""
        return self.__last_output

    @property
    def last_error(self):
        """Latest Error"""
        return self.__last_error
