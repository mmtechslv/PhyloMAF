import typing
from os import path
from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._phy_base import DatabasePhylogenyMixin
from pmaf.database._core._acs_base import DatabaseAccessionMixin
from pmaf.database._manager import DatabaseStorageManager
import pmaf.database._shared._assemblers as transformer
import pmaf.database._shared._summarizers as summarizer
import pandas as pd
import numpy as np
from typing import Any, Tuple
from pmaf.internal._typing import AnyGenericIdentifier
from pmaf.database._parsers._phylo import read_newick_tree
from ete3 import Tree
import re

regex_mrca_tags = re.compile("mrcaott[0-9]+ott[0-9]+")
regex_ott_tags = re.compile("ott([0-9]+)")


def get_tree_leafs(tree_newick_fp):
    tree_str = read_newick_tree(tree_newick_fp)
    newick_string_no_mrca_tag = re.sub(regex_mrca_tags, "", tree_str)
    newick_string_parsed = re.sub(regex_ott_tags, "\\1", newick_string_no_mrca_tag)
    tmp_tree = Tree(newick_string_parsed, format=8)
    nodes_with_names = [node.name for node in tmp_tree.iter_leaves() if node.name != ""]
    return nodes_with_names


class DatabaseOTL(
    DatabaseTaxonomyMixin, DatabasePhylogenyMixin, DatabaseAccessionMixin, DatabaseBase
):
    """Database class for OTL database
    :cite:t:`reesAutomatedAssemblyReference2017a`"""

    DATABASE_NAME = "OpenTreeOfLife"
    INVALID_TAXA = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def build_database_storage(
        cls,
        storage_hdf5_fp: str,
        taxonomy_map_csv_fp: str,
        tree_newick_fp: str,
        stamp_dict: dict,
        force: bool = False,
        chunksize: int = 500,
        delimiter: str = "|",
        **kwargs: Any
    ):
        """Factory method to build new database :term:`hdf5`

        Parameters
        ----------
        storage_hdf5_fp
            Output path for :term:`hdf5`
        taxonomy_map_csv_fp
            Path to taxonomy file
        tree_newick_fp
            Path to FASTA sequences file
        stamp_dict
            Dictionary with metadata that will be stamped to the storage
        force
            Force output file overwrite
        chunksize :
            Sequence/Alignment data processing chunk size. Longer chunks are
            faster to process but require more memory.
        delimiter
            Taxonomy map delimiter
        **kwargs
            Compatibility.

        Returns
        -------

            None if file was created successfully.
        """
        if path.exists(storage_hdf5_fp) and not force:
            raise ValueError("Storage file exists.")
        if not path.isfile(taxonomy_map_csv_fp):
            raise ValueError("Invalid taxonomy CSV/TSV file path provided.")
        if not path.isfile(tree_newick_fp):
            raise ValueError("Invalid tree Newick file path provided.")
        if isinstance(chunksize, int):
            if chunksize <= 0:
                raise ValueError("`chunksize` must be greater than zero.")
        else:
            raise TypeError("`chunksize` must be integer.")

        tmp_storage_manager = DatabaseStorageManager(
            hdf5_filepath=storage_hdf5_fp,
            storage_name=cls.DATABASE_NAME,
            force_new=force,
        )
        tax_ids_in_tree = get_tree_leafs(tree_newick_fp)

        removed_rids, novel_tids, index_mapper, tmp_recap = cls.__process_tax_acs_map(
            tmp_storage_manager, taxonomy_map_csv_fp, delimiter, tax_ids_in_tree
        )
        cls.__process_tree(tmp_storage_manager, tree_newick_fp, index_mapper)

        tmp_storage_manager.commit_to_storage(
            "stat-taxs", transformer.produce_tax_stats(tmp_storage_manager, novel_tids)
        )

        cls.__process_interxmaps(tmp_storage_manager)

        return transformer.finalize_storage_construction(
            tmp_storage_manager, stamp_dict, tmp_recap, **kwargs
        )

    @classmethod
    def __process_tax_acs_map(
        cls,
        storage_manager: DatabaseStorageManager,
        taxonomy_map_csv_fp: str,
        delimiter: str,
        tax_ids_in_tree: typing.List[str],
    ) -> Tuple[AnyGenericIdentifier, np.ndarray, pd.Series, pd.Series]:
        from pmaf.internal._extensions import cython_functions
        from pmaf.internal._constants import VALID_RANKS
        from tempfile import NamedTemporaryFile
        from collections import defaultdict

        def produce_taxonomy_prior(full_taxonomy_prior, index_mapper):
            """The *taxonomy-prior* storage element producer function."""
            tmp_taxonomy_map = full_taxonomy_prior.loc[index_mapper.index].applymap(
                lambda x: "" if pd.isna(x) else x
            )
            yield None, None
            yield transformer.reindex_frame(tmp_taxonomy_map, index_mapper)

        def produce_taxonomy_sheet(taxonomy_sheet):
            """The *taxonomy-sheet* storage element producer function."""
            yield None, None
            yield taxonomy_sheet

        def produce_sequence_accession(taxonomy_prior, index_mapper, dropped_taxa):
            """The *sequence-accession* storage element producer function."""
            if len(dropped_taxa) > 0:
                taxonomy_map_df = taxonomy_prior.drop(
                    index=index_mapper.loc[dropped_taxa].values, errors="ignore"
                )
            else:
                taxonomy_map_df = taxonomy_prior

            acc_map_series = taxonomy_map_df.loc[:, "sourceinfo"]

            def acc_rearranger(taxon_acc):
                acc_split = taxon_acc.split(",")
                acc_type_split = [acc_data.split(":") for acc_data in acc_split]
                acc_parsed = defaultdict(list)
                for acc_elem in acc_type_split:
                    if (
                        "additions" not in acc_elem[0]
                    ):  # This fixes invalid sourceinfo elements within OTT taxonomy.tsv file.
                        acc_parsed[acc_elem[0]].append(acc_elem[1])
                return {key: "|".join(values) for key, values in acc_parsed.items()}

            acc_map_arranged_dict = acc_map_series.map(acc_rearranger).to_dict()
            del acc_map_series
            total_taxid = len(acc_map_arranged_dict)
            all_acc_types = [
                list(taxon_acc.keys()) for taxon_acc in acc_map_arranged_dict.values()
            ]
            unique_acc_types = list(
                set(
                    list(
                        [
                            acc_type
                            for acc_types in all_acc_types
                            for acc_type in acc_types
                        ]
                    )
                )
            )
            del all_acc_types

            def valid_acc_generator(acc_map_dict):
                for taxid, acc_dict in acc_map_dict.items():
                    yield [taxid] + [
                        acc_dict.get(acc_type, "") for acc_type in unique_acc_types
                    ]

            accession_map_df = pd.DataFrame.from_records(
                valid_acc_generator(acc_map_arranged_dict),
                index=["index"],
                columns=["index"] + unique_acc_types,
                nrows=total_taxid,
            )
            accession_map_df.insert(
                loc=0,
                column="otl",
                value=index_mapper.reset_index()
                .set_index("index")
                .loc[accession_map_df.index, "rids"],
            )
            yield None, None
            yield accession_map_df

        def produce_metadata_db_history(transformation_details):
            """The *metadata-db-history* storage element producer function."""
            yield None, None
            yield transformation_details["changes"]

        def produce_map_rep2tid(transformation_details):
            """The *main-rep2tid* storage elemenet producer function."""
            yield None, None
            yield transformation_details["map-rep2tid"]

        full_taxonomy_map = pd.read_csv(
            taxonomy_map_csv_fp,
            index_col="uid",
            sep=delimiter,
            usecols=["uid", "parent_uid", "name", "rank", "sourceinfo", "uniqname"],
            engine="python",
            header=0,
            dtype=str,
        )
        full_taxonomy_map.index = full_taxonomy_map.index.astype(str)
        with NamedTemporaryFile() as tmp_taxonomy:
            full_taxonomy_map.to_csv(
                tmp_taxonomy.name,
                sep="|",
                columns=["parent_uid", "name", "rank"],
                index_label="uid",
            )
            tmp_ott_sheet = cython_functions.generate_taxa_list_for_ott(
                VALID_RANKS, tmp_taxonomy.name, "|"
            )
        tmp_taxonomy_sheet_master = pd.DataFrame.from_records(
            tmp_ott_sheet,
            columns=["uid", "pid"] + VALID_RANKS,
            index=["uid"],
            exclude=["pid"],
        )
        tmp_taxonomy_sheet_master.index = tmp_taxonomy_sheet_master.index.astype(
            full_taxonomy_map.index.dtype
        )
        valid_tax_ids = tmp_taxonomy_sheet_master.index[
            tmp_taxonomy_sheet_master.index.isin(tax_ids_in_tree)
        ]
        tmp_taxonomy_sheet_master = tmp_taxonomy_sheet_master.loc[valid_tax_ids]
        index_mapper = transformer.make_rid_index_mapper(
            tmp_taxonomy_sheet_master.index
        )
        taxonomy_prior = storage_manager.commit_to_storage(
            "taxonomy-prior", produce_taxonomy_prior(full_taxonomy_map, index_mapper)
        )
        taxonomy_sheet_master = transformer.reindex_frame(
            tmp_taxonomy_sheet_master, index_mapper
        )
        tmp_taxonomy_sheet, transformation_details = transformer.reconstruct_taxonomy(
            taxonomy_sheet_master, index_mapper, cls.INVALID_TAXA
        )
        removed_rids = transformation_details["removed-rids"]
        taxonomy_sheet = storage_manager.commit_to_storage(
            "taxonomy-sheet", produce_taxonomy_sheet(tmp_taxonomy_sheet)
        )
        tmp_recap = summarizer.merge_recaps(
            summarizer.recap_taxonomy_sheet(taxonomy_sheet),
            summarizer.recap_transformation(transformation_details),
        )
        tmp_recap = summarizer.append_recaps(
            tmp_recap,
            {
                "molecule-type": "N/A",
                "strand-orientation": "N/A",
                "gene": "N/A",
                "gene-target-region": "N/A",
            },
        )
        storage_manager.commit_to_storage(
            "sequence-accession",
            produce_sequence_accession(taxonomy_prior, index_mapper, removed_rids),
        )
        storage_manager.commit_to_storage(
            "metadata-db-history", produce_metadata_db_history(transformation_details)
        )
        storage_manager.commit_to_storage(
            "map-rep2tid", produce_map_rep2tid(transformation_details)
        )
        return (
            removed_rids,
            transformation_details["novel-tids"],
            index_mapper,
            tmp_recap,
        )

    @classmethod
    def __process_tree(
        cls,
        storage_manager: DatabaseStorageManager,
        tree_newick_fp: str,
        index_mapper: pd.Series,
    ):
        """Process phylogenetic tree.

        Parameters
        ----------
        storage_manager
            Active storage manager
        tree_newick_fp
            Path to Newick tree
        index_mapper
            Index renamer/mapper
        """

        def produce_tree_prior(tree_newick_fp):
            yield None, None
            yield read_newick_tree(tree_newick_fp)

        def produce_tree_parsed(tree_newick_string, index_mapper):
            yield None, None
            newick_string_no_mrca_tag = re.sub(regex_mrca_tags, "", tree_newick_string)
            newick_string_parsed = re.sub(
                regex_ott_tags, "\\1", newick_string_no_mrca_tag
            )
            tmp_tree = Tree(newick_string_parsed, format=8)
            yield transformer.reparse_tree(tmp_tree, index_mapper)

        def produce_tree_object(tree_newick_string):
            yield None, None
            yield Tree(tree_newick_string, format=2, quoted_node_names=True)

        def produce_map_tree(tree_object):
            yield None, None
            tmp_rebuilded_tree = transformer.rebuild_phylo(tree_object)
            yield transformer.make_tree_map(tmp_rebuilded_tree)

        tmp_newick_string = storage_manager.commit_to_storage(
            "tree-prior", produce_tree_prior(tree_newick_fp)
        )
        tmp_newick_parsed = storage_manager.commit_to_storage(
            "tree-parsed", produce_tree_parsed(tmp_newick_string, index_mapper)
        )
        tmp_tree_object = storage_manager.commit_to_storage(
            "tree-object", produce_tree_object(tmp_newick_parsed)
        )
        storage_manager.commit_to_storage("map-tree", produce_map_tree(tmp_tree_object))
        return

    @classmethod
    def __process_interxmaps(cls, storage_manager: DatabaseStorageManager):
        """Process interx maps.

        Parameters
        ----------
        storage_manager
            Active storage manager
        """

        def produce_map_interx_taxon(interx_maker_result):
            yield None, None
            yield interx_maker_result["map-interx-taxon"]

        def produce_map_interx_repseq(interx_maker_result):
            yield None, None
            yield interx_maker_result["map-interx-repseq"]

        tmp_interx_result = transformer.make_interxmaps(storage_manager)
        storage_manager.commit_to_storage(
            "map-interx-taxon", produce_map_interx_taxon(tmp_interx_result)
        )
        storage_manager.commit_to_storage(
            "map-interx-repseq", produce_map_interx_repseq(tmp_interx_result)
        )
        return

    @property
    def name(self):
        """Storage database name/label."""
        return self.DATABASE_NAME
