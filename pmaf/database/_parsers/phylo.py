import ete3
import re

def read_newick_tree(newick_fp):
    '''

    Args:
      newick_fp: 

    Returns:

    '''
    with open(newick_fp, 'r') as tree_file:
        newick_string = tree_file.read()
    return newick_string
