from pmaf.phylo.branchest._metakit import BranchEstimatorBackboneMetabase
from pmaf.sequence._metakit import MultiSequenceMetabase
from skbio.sequence.distance import hamming
from tempfile import mkdtemp, NamedTemporaryFile
from os import path
import pandas as pd
from io import StringIO
from pmaf.phylo.tree._metakit import PhyloTreeMetabase
from pmaf.phylo.tree._tree import PhyloTree
import subprocess
from typing import Optional, Any


class BranchestERABLE(BranchEstimatorBackboneMetabase):
    """Branch estimator for phylogenetic trees."""

    _cache_prefix = "erable_"

    def __init__(
        self, bin_fp: Optional[str] = "erable", cache_dir: Optional[str] = None
    ):
        """ERaBLE phylogenetic tree estimator on fixed tree topology. :cite:t:`binetFastAccurateBranch2016`

        Args:
            bin_fp: Path to 'erable' executable or None for default.
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
        self.__last_rates = None

    def __repr__(self):
        class_name = self.__class__.__name__
        method_name = "BranchEstimator-ERaBLE"
        repr_str = "<{}:[{}], Path: [{}]>".format(
            class_name, method_name, self.__bin_fp
        )
        return repr_str

    def _make_input_matrix(self, multiseq: MultiSequenceMetabase) -> str:
        """Creates hamming distance matrix from `multiseq` sequence alignment.

        Args:
          multiseq: Aligned representative sequences.

        Returns:
            Input string for ERaBLE executive.

        """
        seq_names = multiseq.index
        dist = pd.DataFrame(index=seq_names, columns=seq_names, dtype="f")
        for sid_i, seq_i in multiseq.get_iter("skbio"):
            for sid_j, sed_j in multiseq.get_iter("skbio"):
                dist.loc[sid_i, sid_j] = hamming(seq_i, sed_j)
        tmp_io = StringIO()
        total_multiseqs = str(1)
        tmp_io.write("{}\n\n".format(total_multiseqs))
        seq_name = "%Sequence {}".format(str(multiseq.name))
        tmp_io.write("{}\n".format(seq_name))
        seq_details = "{} {}".format(
            str(multiseq.count), str(multiseq.sequences[0].length)
        )
        tmp_io.write("{}\n".format(seq_details))
        dist_matrix = "{}".format(dist.to_string(header=False))
        tmp_io.write("{}\n".format(dist_matrix))
        tmp_io.seek(0, 0)
        return tmp_io.read()

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
        tmp_matrix_str = self._make_input_matrix(alignment)
        tmp_matrix_fp = NamedTemporaryFile(mode="w", dir=self.__cache_dir, delete=False)
        tmp_tree_fp = NamedTemporaryFile(mode="w", dir=self.__cache_dir, delete=False)
        tmp_matrix_fp.write(tmp_matrix_str)
        tmp_matrix_fp.flush()
        tree.write(tmp_tree_fp.name, tree_format=5, root_node=False)
        erable_cmd = [
            self.__bin_fp,
            "-i",
            tmp_matrix_fp.name,
            "-t",
            tmp_tree_fp.name,
        ]
        print(" ".join(erable_cmd))
        process = subprocess.Popen(
            erable_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        self.__last_output = output.decode() if isinstance(output, bytes) else output
        self.__last_error = error.decode() if isinstance(error, bytes) else error
        process.kill()
        tmp_new_tree_fp = "{}.lengths.nwk".format(tmp_matrix_fp.name)
        tmp_new_rates_fp = "{}.rates.txt".format(tmp_matrix_fp.name)
        with open(tmp_new_tree_fp, "r") as newick_file, open(
            tmp_new_rates_fp, "r"
        ) as rates_file:
            self.__last_rates = rates_file.read()
            return PhyloTree(newick_file.read())

    @property
    def last_out(self):
        """Lastest Output"""
        return self.__last_output

    @property
    def last_error(self):
        """Latest Error"""
        return self.__last_error

    @property
    def last_rates(self):
        """Latest Rates Product"""
        return self.__last_rates
