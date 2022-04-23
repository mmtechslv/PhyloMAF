#!/usr/bin/env python3
from re import compile

###Following constants should not be modified. PMAF_ITS  links internal and external representation of values
ITS = {
    "lineage": "Consensus Lineage",
    "r2Rank": {
        "d": "Domain",
        "k": "Kingdom",
        "p": "Phylum",
        "c": "Class",
        "o": "Order",
        "f": "Family",
        "g": "Genus",
        "s": "Species",
    },
    "r2rank": {
        "d": "domain",
        "k": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species",
    },
    "rank2r": {
        "domain": "d",
        "kingdom": "k",
        "phylum": "p",
        "class": "c",
        "order": "o",
        "family": "f",
        "genus": "g",
        "species": "s",
    },
    "rank2Rank": {
        "domain": "Domain",
        "kingdom": "Kingdom",
        "phylum": "Phylum",
        "class": "Class",
        "order": "Order",
        "family": "Family",
        "genus": "Genus",
        "species": "Species",
    },
    "Rank2r": {
        "Domain": "d",
        "Kingdom": "k",
        "Phylum": "p",
        "Class": "c",
        "Order": "o",
        "Family": "f",
        "Genus": "g",
        "Species": "s",
    },
}

IUPAC_AMBIGUOUS = {
    "R": ["A", "G"],
    "Y": ["C", "T"],
    "S": ["G", "C"],
    "W": ["A", "T"],
    "K": ["G", "T"],
    "M": ["A", "C"],
    "B": ["C", "G", "T"],
    "D": ["A", "G", "T"],
    "H": ["A", "C", "T"],
    "V": ["A", "C", "G"],
    "N": ["A", "C", "T", "G"],
}

IUPAC_BASES = [
    "A",
    "C",
    "T",
    "G",
    "R",
    "Y",
    "S",
    "W",
    "K",
    "M",
    "B",
    "D",
    "H",
    "V",
    "N",
]
IUPAC_NON_AMBIGUOUS_BASES = ["A", "T", "G", "C"]

# PMAF_MAIN_RANKS list of main taxonomic ranks used in Jadval. Do not modify. Order is important!
VALID_RANKS = ["d", "k", "p", "c", "o", "f", "g", "s"]
MAIN_RANKS = VALID_RANKS[:-1]

DEFAULT_METADATA = {
    "study-name": None,
    "authors": None,
    "year": None,
    "rel-abun-mode": False,
}

jRegexGG = compile(
    "([kdpcofgs]{1})[_]{2}([^;_]*)[;]?"
)  # Catches both  rank and taxon for greengenes
jRegexQIIME = compile("([^\s;]+?)[_]{2}([^;]+)")
jRegexSINTAX = compile("[kdpcofgs]{1}[:]{1}([^:,;]*)[,|;]?")  # Fix

DEFAULT_DATE_FORMAT = "%m/%d/%y"
DEFAULT_DATETIME_FORMAT = "%m/%d/%y %H:%M"
DEFAULT_TIME_FORMAT = "%H:%M:%S"


BIOM_TAXONOMY_NAMES = [
    "taxon",
    "taxonomy",
    "lineage",
    "lineages",
    "taxa",
    "consensus lineages",
    "consensuslineages",
]
AVAIL_TAXONOMY_NOTATIONS = ["greengenes", "silva", "sintax", "qiime"]
# ERROR CODES dict of all Jadval Error Code Descriptions
_ERROR_CODES = {
    1: "Generic Error",  # generate_lineages_from_taxa,
    2: "Error while performing primary lineage correlations",  # correlate_lineages
    3: "Cutting Lineages Failed",  # cut_lineages
    4: "Error While Reading CSV file",  # read_csv
    5: "Saving Instance State Failed",  # save_state
    6: "Loading Instance State Failed",  # load_state
    7: "Loading of Tree File Failed",  # load_tree
    8: "Tree Pruning Failed",  # prune_tree_for_taxa_ids,
    9: "Can't get available ranks for initiated taxonomy",  # get_avail_ranks
    10: "Error while fixing missing taxa",  # _fix_missing_taxa
    11: "Failed to reconstruct internal lineages",  # reconstruct_internal_lineages
    12: "Error during _local loading",  # load_taxonomy_database
    13: "Failed to initiate taxonomy map",  # __load_taxonomy_map
    14: "Failed to initiate internal taxonomy dataframe",  # __init_internal_taxonomy
    15: "Error Loading OTU Table",  # load_OTU_table
    16: "Error! OTU Table must be initiated first",  # load_OTU_lineages
    17: "Failed to Check State of Initiation",  # check_init
    18: "Failed to load OTU lineages",  # load_OTU_lineages
    19: "Failed to get taxonomy by OTU labels",  # get_taxonomy_by_otu_label
    20: "Failed to get taxonomy by OTU ids",  # get_taxonomy_by_otu_id
    21: "Failed to reconstruct internal lineages.",  # reconstruct_internal_lineages
    22: "Failed to drop OTUs for given IDs.",  # drop_otus_by_ids
    23: "Failed to drop OTUs for given labels.",  # drop_otus_by_labels
    24: "Failed to drop OTUs without taxonomy.",  # drop_otus_without_taxa
    25: "Failed to drop OTUs without given rank(s).",  # drop_otus_without_ranks
    26: "Error while merging duplicated taxa.",  # merge_duplicated_taxa
    27: "Error while merging OTUs by rank.",  # merge_otus_by_rank
    28: "Error loading given taxonomic _local.",  # load_database
    29: "Failed to generate OTU-Taxon correlations.",  # generate_taxa_correlations
    30: "Failed to reconstruct instance for new OTU IDs.",  # reconstruct_for_otu_ids
    31: "Failed to retrieve custom FeatureTable for required taxonomic _local.",  # retrieve_custom
    32: "Failed to get active taxonomic _local of instance.",  # get_active_taxonomic_db
    33: "Error while generating OTU table CSV file.",  # save_as_csv
    34: "Error while exporting FeatureTable data.",  # export_data
    35: "Failed to set new internal IDS.",  # __set_internal_ids
    36: "Failed to construct taxonomy from lineages",  # __construct_taxonomy_from_lineages
    37: "Failed to derive new taxonomy for given taxonomic _local.",  # __derive_taxonomy_db
    38: "Failed to record <prior ID - new ID> group relations",  # __record_group_relations
    39: "Failed to reassign <OTU ID - OTU Label> associations",  # __reassign_label_assoc
    40: "Failed to record removed data to self.lost_otus",  # __record_removed_taxa
    41: "Failed to remove OTU IDs and OTU labels self.label_assoc",  # __remove_labels_by_ids
    42: "Failed to drop taxa by OTU IDs",  # __drop_taxa
    44: "Failed to retrieve complete Jadval table",  # pmaf
    45: "Failed to retrieve lineages",  # lineages
    46: "Failed to retrieve id-label Series",  # LabelById
    47: "Failed to retrieve label-id Series",  # IdByLabel
    48: "Failed to retrieve info of initial loadings",  # loader_info
    49: "Failed to retrieve phylogenetic tree (ete3 Tree Object) ",  # phylo_tree
    50: "Failed to retrieve active taxonomic _local type",  # taxonomy_db_type
    51: "Failed to retrieve active taxonomic _local name",  # taxonomy_db_name
    52: "Failed to create new directory.",  # ensure_new_dir
    53: "Failed to make a copy.",  # copy
    54: "Error occured during pattern search.",  # search
    55: "Failed to get list of internal OTU ids.",  # get_ids
    56: "Failed to get list of OTU labels.",  # get_labels
    57: "Cannot merge FeatureTables with same study names.",
}

_WARNING_CODES = {1: "Generic Warning"}
