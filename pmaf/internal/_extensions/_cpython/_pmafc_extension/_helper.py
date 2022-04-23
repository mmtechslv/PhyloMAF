import math
from functools import reduce
from pmaf.internal._constants import IUPAC_AMBIGUOUS


def get_min_dtype(kmer_sizes):
    """

    Parameters
    ----------
    kmer_sizes :


    Returns
    -------

    """
    max_kmer_size = max(kmer_sizes)
    min_bits = 2 * max_kmer_size + len(kmer_sizes)
    lowest_min_int_size = math.pow(2, math.floor(math.log2(min_bits)))
    if lowest_min_int_size == min_bits:
        min_int_size = lowest_min_int_size
    else:
        min_int_size = lowest_min_int_size * 2
    return int(min_int_size)


def get_max_total_kmers(kmer_sizes):
    """

    Parameters
    ----------
    kmer_sizes :


    Returns
    -------

    """
    max_kmers_total = 0
    for kmer_size in kmer_sizes:
        max_kmers_total = max_kmers_total + 4**kmer_size
    return max_kmers_total


def get_max_kmers(kmer_sizes):
    """

    Parameters
    ----------
    kmer_sizes :


    Returns
    -------

    """
    return 4 ** max(kmer_sizes)


def verify_kmer_sizes(kmer_sizes, mem_size, mem_max, hash_size, hash_max):
    """

    Parameters
    ----------
    kmer_sizes :

    mem_size :

    mem_max :

    hash_size :

    hash_max :


    Returns
    -------

    """
    min_dtype_max = 2 ** get_min_dtype(kmer_sizes) - 1
    max_total_kmers = get_max_total_kmers(kmer_sizes)
    max_kmers_max = get_max_kmers(kmer_sizes)

    if min_dtype_max > hash_max:
        return -1
    if max_total_kmers > ((mem_max + 1) / hash_size):
        return -2
    if max_kmers_max > ((mem_max + 1) / hash_size):
        return -3
    return 0


def make_sequence_record_tuple(sequence_id, sequence_str):
    """

    Parameters
    ----------
    sequence_id :

    sequence_str :


    Returns
    -------

    """
    ambiguous_count = [
        (sequence_str.count(b), len(bb))
        for b, bb in IUPAC_AMBIGUOUS.items()
        if b in sequence_str
    ]
    total_ambiguous = (
        reduce(lambda x, y: x + y, [ae[0] for ae in ambiguous_count])
        if len(ambiguous_count) > 0
        else 0
    )
    return (sequence_id, sequence_str, len(sequence_str), total_ambiguous)
