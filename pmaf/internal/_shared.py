import csv
import pandas as pd
import numpy as np
import os
import dateparser
from ._constants import MAIN_RANKS, VALID_RANKS, IUPAC_AMBIGUOUS, IUPAC_BASES, jRegexGG,jRegexSINTAX,jRegexQIIME
from ._extensions import _cython as CyMethods
import statistics
from itertools import groupby,chain,islice
from pathlib import Path

def get_package_root():
    return str(Path(__file__).parent.parent)

def to_array(data):
    if np.isscalar(data):
        return np.asarray([data])
    elif pd.api.types.is_list_like(data):
        return np.asarray(data)
    else:
        return np.asarray([])


def get_stats_for_sequence_record_df(sequence_record_df):
    reps_ex_columns = list(IUPAC_AMBIGUOUS.keys())
    reps_ex_buffer = {col: [] for col in reps_ex_columns}
    reps_columns = ['length', 'tab', 'complexity', 'amb_mean', 'amb_rep_mean', 'amb_repmax_mean', 'amb_repmin_mean'] + ["{}_total".format(col) for col in IUPAC_BASES] + ["{}_repmax".format(col) for col in reps_ex_columns] + ["{}_repmin".format(col) for col in reps_ex_columns]

    def process_rep(rep_series):
        complexity_level = 0
        abase_count = []
        for b, bb in IUPAC_AMBIGUOUS.items():
            total_abases = rep_series['sequence'].count(b)
            abase_count.append(total_abases)
            complexity_level = complexity_level + total_abases * len(bb)
            if total_abases > 0:
                base_reps = [len(list(y)) for (c, y) in groupby(rep_series['sequence']) if c == b]
                reps_ex_buffer[b] = [max(base_reps), min(base_reps)]
            else:
                reps_ex_buffer[b] = [0, 0]
        base_count_list = [rep_series['sequence'].count(b) for b in IUPAC_BASES]
        amb_repmax_list = [reps_ex_buffer[col][0] for col in reps_ex_columns]
        amb_repmin_list = [reps_ex_buffer[col][1] for col in reps_ex_columns]
        amb_mean = statistics.mean(abase_count)
        amb_repmax_mean = statistics.mean(amb_repmax_list)
        amb_repmin_mean = statistics.mean(amb_repmin_list)
        amb_rep_mean = statistics.mean([amb_repmax_mean, amb_repmin_mean])
        return [rep_series['length'], rep_series['tab'], complexity_level, amb_mean, amb_rep_mean, amb_repmax_mean, amb_repmin_mean] + base_count_list + amb_repmax_list + amb_repmin_list

    sequence_stats = sequence_record_df.apply(process_rep, axis=1, result_type='expand')
    sequence_stats.columns = reps_columns
    return sequence_stats



def chunk_generator(iterable, chunksize):
    iterator = iter(iterable)
    while True:
        chunk = tuple(islice(iterator, chunksize))
        if not chunk:
            break
        yield chunk
    # for i in range(0, len(items), chunksize):
    #     yield items[i:i + chunksize]

def get_datetime(datetime_str,format=None):
    if format is not None:
        ret = dateparser.parse(datetime_str,date_formats=format)
    else:
        ret = dateparser.parse(datetime_str)
    if ret is None:
        ret = False
    return ret


def validate_ranks(ranks,refranks=MAIN_RANKS):
    ret = False
    if all(map(lambda rank: rank in refranks, ranks)):
        ret = True
    return ret

def extract_valid_ranks(ranks, refranks=MAIN_RANKS):
    ret = False
    valid_ranks = [rank for rank in ranks if rank in refranks]
    if len(valid_ranks)>0:
        ret = valid_ranks
    return ret




def get_rank_upto(ranks,ter_rank,include_terminal=False):
    """Generates list of ranks from `ranks` terminated at `ter_rank`

    Args:
        ranks (list): List of ranks
        ter_rank (str): Terminal rank

    Returns:
        (list): List of ranks
    """
    ret = []
    tmp_ranks = list(ranks)
    if ter_rank in tmp_ranks:
        ter_index = tmp_ranks.index(ter_rank) + 1 if include_terminal else tmp_ranks.index(ter_rank)
        if ter_index != 0:
            ret = tmp_ranks[:ter_index]
    return ret

def sort_ranks(ranks):
    ret = False
    ranks = list(ranks) if not isinstance(ranks,list) else ranks
    if len(ranks)>0:
        ret = [rank for rank in MAIN_RANKS if rank in ranks]
    return ret



def ensure_list(var):
    """Makes sure that `var` is a list

    Args:
        var (list like): List like object

    Returns:
        (list): `var` as list
    """
    return var if type(var) is list else [var]


def is_table_taxa_alike(feature_table1,feature_table2):
    """This method checks if `feature_table2` instance contains same taxonomy as
    `feature_table1`

    Args:
        feature_table1 (pmaf._feature.FeatureTable): First FeatureTable
        feature_table2 (pmaf._feature.FeatureTable): Second FeatureTable

    Returns:
        (bool): True if taxonomies are same. False otherwise
    """
    feature_table1_lineage_sorted = feature_table1.taxonomy.loc[:,'lineage'].sort_values(axis=0).reset_index(drop=True)
    feature_table2_lineage_sorted = feature_table2.taxonomy.loc[:,'lineage'].sort_values(axis=0).reset_index(drop=True)
    return feature_table1_lineage_sorted.equals(feature_table2_lineage_sorted)

def indentify_taxon_notation(taxon_string):
    """Identifies taxonomic notation from `taxon_string` . Currently available
    conventions are Greengenens, sintax and SILVA

    Examples:
        >>> test_taxon_string = 'c__Bacilli; o__Lactobacillales; f__Lactobacillaceae; g__Lactobacillus; s__Lactobacillusbrevis'
        >>> print(indentify_taxon_notation(test_taxon_string))
        'greengenes'

    Args:
        taxon_string (str): String with taxonomy/lineage to test

    Returns:
        (str): 'greengenes' or 'sintax' or 'silva'
    """
    if jRegexGG.search(taxon_string):
        return 'greengenes'
    elif jRegexSINTAX.search(taxon_string):
        return 'sintax'
    elif jRegexQIIME.search(taxon_string):
        return 'qiime'
    else:
        return False

def generate_lineages_from_taxa(in_taxa,missing_rank=False,desired_ranks=False,drop_ranks=False): #missing_rank - if True will include rank preffix(such as "s__") even if rank is missing or among drop_ranks; desired_ranks - list of desired ranks; drop_ranks - list of undesired ranks that should be removed, this parameter is useless if missing_rank is set to False
    """Generate consensus lineages in Greengenes convention format from taxonomy
    dataframe like `FeatureTable._internal_taxonomy`

    Args:
        in_taxa (pandas.DataFrame): pandas DataFrame like
            `FeatureTable._internal_taxonomy`
        missing_rank (bool): If True will generate prefix like s__ or d__
        desired_ranks (list or bool): List of desired ranks to generate. If
            False then will generate all main ranks
        drop_ranks (list or bool): List of ranks to drop from desired ranks.
            This parameter only useful if `missing_rank` is True

    Returns:
        (pandas.Series): Series with generated consensus lineages and
        corresponding IDs as Series index
    """
    if desired_ranks and not all(e in VALID_RANKS for e in desired_ranks):
        print('Impossible characters found in desired_ranks. Please use: ' + ','.join(VALID_RANKS))
        return False
    make_ranks = [rank for rank in VALID_RANKS if rank in desired_ranks] if desired_ranks else MAIN_RANKS
    pass_taxa_df = in_taxa.loc[:, make_ranks]
    if drop_ranks:
        pass_taxa_df.iloc[:][drop_ranks] = None
    pass_taxa_list = pass_taxa_df.values.tolist()
    new_lineages = CyMethods.rapid_lineage_generator(pass_taxa_list, missing_rank, make_ranks)
    return pd.Series(index=pass_taxa_df.index, data=new_lineages)

def cut_lineages(in_lineages,levels):
    """Supplementary function for cutting ranks both ends of lineages with
    Greengenes convention

    Args:
        in_lineages (pandas.Series): pandas Series of lineages and IDs as index
        levels (int): Level to cut. 1 will cut from the beginning of the string.
            Negative sign will reverse algorithm and will cut from the end.

    Returns:
        (pandas.Series): New lineages
    """
    lineages = list(in_lineages.values)
    lineage_indices = list(in_lineages.index)
    iReverse = True if levels<0 else False
    levels = abs(levels)
    new_lineages = []
    for taxon_lineage in lineages:
        tmp_lineage = taxon_lineage
        for level in range(levels):
            tmp_lineage = tmp_lineage[(tmp_lineage.find(';')+2):] if (not iReverse) else tmp_lineage[:-(tmp_lineage[::-1].find(';')+1)]
        new_lineages.append(tmp_lineage)
    new_lineages_series = pd.Series(data=new_lineages,index=lineage_indices)
    return new_lineages_series

def ensure_new_dir(dir_name):
    """Creates new directory if it does not exist. If it does exist then it
    checks if existing directory was generated via this function if it does it
    reads counter prefix in directory name and creates new directory with
    increment

    Args:
        dir_name (str): Directory name to check

    Returns:
        (str|bool): Path to new directory or False.
    """
    new_path_result = False
    if os.path.exists(dir_name):
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
            new_path_result = dir_name
        else:
            if '-' in dir_name:
                sep_i = len(dir_name) - dir_name[::-1].index('-') - 1
                no_str = dir_name[sep_i + 1:]
                try:
                    cur_no = int(no_str)
                except ValueError:
                    cur_no = None
            else:
                cur_no = None
            dir_name = dir_name+'-' if cur_no is None else dir_name[:sep_i+1]
            n_i = 1 if cur_no is None else cur_no
            while os.path.exists(dir_name+str(n_i)):
                n_i += 1
            os.mkdir(dir_name+str(n_i))
            new_path_result = dir_name+str(n_i)
    else:
        os.mkdir(dir_name)
        new_path_result = dir_name
    return new_path_result

def read_csv(file_path,sep=',', quote='"'):
    """Reads CSV/TSV file and returns content as list

    Args:
        file_path (str): Path to CSV/TSV the file
        sep (str): Delimiter of CSV/TSV file
        quote (str): Quoting of CSV/TSV file

    Returns:
        (list): Content of the CSV/TSV file
    """
    file_content = []
    with open(file_path, 'r') as feature_file:
        feature_file_reader = csv.reader(feature_file, delimiter=sep, quotechar=quote)
        for row in feature_file_reader:
            file_content.append(row)
    return file_content

def write_csv(iContent,file_path,sep=',', quote='"'):
    """Writes content to CSV/TSV file

    Args:
        iContent (list): Content to write
        file_path (str): Path to CSV/TSV the file
        sep (str): Delimiter of CSV/TSV file
        quote (str): Quoting of CSV/TSV file

    Returns:
        (bool): True if write was successful. False otherwise
    """
    with open(file_path, 'w') as write_file:
        file_writer = csv.writer(write_file, delimiter=sep, quotechar=quote)
        return file_writer.writerows(iContent)
    return False
