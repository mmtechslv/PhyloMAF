def read_newick_tree(newick_fp: str):
    """ Read Newick Tree"""
    with open(newick_fp, "r") as tree_file:
        newick_string = tree_file.read()
    return newick_string
