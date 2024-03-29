from os import path
from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._seq_base import DatabaseSequenceMixin
from pmaf.database._core._phy_base import DatabasePhylogenyMixin
from pmaf.database._core._acs_base import DatabaseAccessionMixin
from pmaf.database._manager import DatabaseStorageManager
import pmaf.database._shared._assemblers as transformer
import pmaf.database._shared._summarizers as summarizer
from pmaf.internal.io._seq import SequenceIO
import numpy as np
import pandas as pd
from typing import Any, Tuple
from pmaf.internal._typing import AnyGenericIdentifier


class DatabaseGTDB(
    DatabaseTaxonomyMixin,
    DatabaseSequenceMixin,
    DatabasePhylogenyMixin,
    DatabaseAccessionMixin,
    DatabaseBase,
):
    """Database class for GTDB database
    :cite:t:`parksCompleteDomaintospeciesTaxonomy2020`"""

    DATABASE_NAME = "GTDP"
    INVALID_TAXA = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def build_database_storage(
        cls,
        storage_hdf5_fp: str,
        taxonomy_map_csv_fp: str,
        tree_newick_fp: str,
        sequence_fasta_fp: str,
        metadata_csv_fp: str,
        stamp_dict: dict,
        force: bool = False,
        chunksize: int = 500,
        **kwargs: Any
    ) -> None:
        """Factory method to build new database :term:`hdf5`

        Parameters
        ----------
        storage_hdf5_fp
            Output path for :term:`hdf5` file
        taxonomy_map_csv_fp
            Path to taxonomy file
        tree_newick_fp
            Path to Newick tree file
        sequence_fasta_fp
            Path to FASTA sequences file
        stamp_dict
            Dictionary with metadata that will be stamped to the database
        force
            Force output file overwrite
        chunksize
            Sequence/Alignment data processing chunk size. Longer chunks are
            faster to process but require more memory.
        **kwargs
            Compatibility.

        Returns
        -------

            None if file was created successfully.
        """
        if path.exists(storage_hdf5_fp) and not force:
            raise ValueError("Storage file exists.")
        if isinstance(taxonomy_map_csv_fp, (list, tuple)):
            if not all(
                [
                    path.isfile(taxonomy_map_csv_fp)
                    for taxonomy_map_csv_fp in taxonomy_map_csv_fp
                ]
            ):
                raise ValueError("Invalid taxonomy CSV/TSV file path provided.")
        else:
            raise TypeError("`taxonomy_map_csv_fp` must be tuple or list.")
        if isinstance(metadata_csv_fp, (list, tuple)):
            if not all(
                [path.isfile(metadata_csv_fp) for metadata_csv_fp in metadata_csv_fp]
            ):
                raise ValueError("Invalid metadata CSV/TSV file path provided.")
        else:
            raise TypeError("`metadata_csv_fp` must be tuple or list.")
        if isinstance(tree_newick_fp, (list, tuple)):
            if not all(
                [path.isfile(tree_newick_fp) for tree_newick_fp in tree_newick_fp]
            ):
                raise ValueError("Invalid tree Newick file path provided.")
        else:
            raise TypeError("`tree_newick_fp` must be tuple or list.")
        if isinstance(sequence_fasta_fp, (list, tuple)):
            if not all(
                [
                    path.isfile(sequence_fasta_fp)
                    for sequence_fasta_fp in sequence_fasta_fp
                ]
            ):
                raise ValueError("Invalid sequence FASTA file path provided.")
        else:
            raise TypeError("`sequence_fasta_fp` must be tuple or list")
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

        valid_ids = np.asarray(
            [
                sid[0]
                for sid in SequenceIO(sequence_fasta_fp).pull_parser(
                    parser="simple", id=True, description=False, sequence=False
                )
            ]
        )

        removed_rids, novel_tids, index_mapper, tmp_recap = cls.__process_tax_map(
            tmp_storage_manager, taxonomy_map_csv_fp, valid_ids
        )
        cls.__process_acs(
            tmp_storage_manager, metadata_csv_fp, index_mapper, removed_rids
        )
        cls.__process_tree(tmp_storage_manager, tree_newick_fp, index_mapper)

        tmp_recap = cls.__process_sequence(
            tmp_storage_manager,
            index_mapper,
            removed_rids,
            tmp_recap,
            sequence_fasta_fp,
            chunksize,
        )

        tmp_storage_manager.commit_to_storage(
            "stat-reps", transformer.produce_rep_stats(tmp_storage_manager, chunksize)
        )
        tmp_storage_manager.commit_to_storage(
            "stat-taxs", transformer.produce_tax_stats(tmp_storage_manager, novel_tids)
        )

        cls.__process_interxmaps(tmp_storage_manager)

        return transformer.finalize_storage_construction(
            tmp_storage_manager, stamp_dict, tmp_recap, **kwargs
        )

    @classmethod
    def __process_tax_map(
        cls,
        storage_manager: DatabaseStorageManager,
        taxonomy_map_csv_fp: str,
        valid_ids: np.ndarray,
    ) -> Tuple[AnyGenericIdentifier, np.ndarray, pd.Series, pd.Series]:
        """Process taxonomy only.

        Parameters
        ----------
        storage_manager
            Active storage manager
        taxonomy_map_csv_fp
            Path to taxonomy map
        valid_ids
            Valid reference identifiers to keep

        Returns
        -------

            Results of the process that need to be passed to builder.
        """
        from pmaf.database._parsers._qiime import (
            read_qiime_taxonomy_map,
            parse_qiime_taxonomy_map,
        )

        def produce_taxonomy_prior(tmp_taxonomy_prior, index_mapper):
            """The *taxonomy-prior* storage element producer function."""
            yield None, None
            yield transformer.reindex_frame(tmp_taxonomy_prior, index_mapper)

        def produce_taxonomy_sheet(taxonomy_sheet):
            """The *taxonomy-sheet* storage element producer function."""
            yield None, None
            yield taxonomy_sheet

        def produce_metadata_db_history(transformation_details):
            """The *metadata-db-history* storage element producer function."""
            yield None, None
            yield transformation_details["changes"]

        def produce_map_rep2tid(transformation_details):
            """The *main-rep2tid* storage elemenet producer function."""
            yield None, None
            yield transformation_details["map-rep2tid"]

        full_taxonomy_prior = pd.concat(
            [read_qiime_taxonomy_map(tax_map_fp) for tax_map_fp in taxonomy_map_csv_fp],
            axis=0,
        )
        tmp_taxonomy_prior = full_taxonomy_prior.loc[valid_ids]
        index_mapper = transformer.make_rid_index_mapper(tmp_taxonomy_prior.index)
        taxonomy_prior = storage_manager.commit_to_storage(
            "taxonomy-prior", produce_taxonomy_prior(tmp_taxonomy_prior, index_mapper)
        )
        tmp_taxonomy_sheet_master = parse_qiime_taxonomy_map(taxonomy_prior)
        taxonomy_sheet, transformation_details = transformer.reconstruct_taxonomy(
            tmp_taxonomy_sheet_master, index_mapper, cls.INVALID_TAXA
        )
        removed_rids = transformation_details["removed-rids"]
        storage_manager.commit_to_storage(
            "taxonomy-sheet", produce_taxonomy_sheet(taxonomy_sheet)
        )
        tmp_recap = summarizer.merge_recaps(
            summarizer.recap_taxonomy_sheet(taxonomy_sheet),
            summarizer.recap_transformation(transformation_details),
        )
        tmp_recap = summarizer.append_recaps(
            tmp_recap,
            {
                "molecule-type": "DNA",
                "strand-orientation": "forward",
                "gene": "rRNA",
                "gene-target-region": "16S",
            },
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
    def __process_acs(
        cls,
        storage_manager: DatabaseStorageManager,
        metadata_csv_fp: str,
        index_mapper: pd.Series,
        dropped_taxa: np.ndarray,
    ) -> None:
        """Process accession numbers.

        Parameters
        ----------
        storage_manager
            Active storage manager
        metadata_csv_fp
            File path to metadata file
        index_mapper
            Index renamer/mapper
        dropped_taxa
            Taxa that was previously dropped
        """

        def produce_sequence_accession(valid_metadata, index_mapper, dropped_taxa):
            """The *sequence-accession8 storage element producer function."""
            yield None, None
            id_to_drop = valid_metadata.index[valid_metadata.index.isin(dropped_taxa)]
            tmp_gtdp_acs = (
                index_mapper.drop(index=dropped_taxa, errors="ignore")
                .reset_index(name="nrids")
                .set_index("nrids")
            )
            tmp_accessions = transformer.reindex_frame(
                valid_metadata.drop(index=id_to_drop, errors="ignore"), index_mapper
            )
            tmp_accessions.insert(loc=0, column="gtdb", value=tmp_gtdp_acs.values)
            yield tmp_accessions

        total_metadata = pd.concat(
            [
                pd.read_csv(metadata_csv_fp, sep="\t", index_col=0, na_values="none")
                for metadata_csv_fp in metadata_csv_fp
            ],
            axis=0,
        )
        valid_metadata = total_metadata.loc[
            index_mapper.index, ["ncbi_genbank_assembly_accession", "ncbi_taxid"]
        ]
        valid_metadata.columns = ["ncbi-genbank", "ncbi-taxid"]
        storage_manager.commit_to_storage(
            "sequence-accession",
            produce_sequence_accession(valid_metadata, index_mapper, dropped_taxa),
        )
        return

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
            Active storage element
        tree_newick_fp
            Path to Newick tree
        index_mapper
            Index renamer/mapper
        """
        from ete3 import Tree

        def produce_tree_prior(merged_tree):
            """The *tree-prior* storage element producer function."""
            yield None, None
            yield merged_tree.write(format=2)

        def produce_tree_parsed(tree_newick_string, index_mapper):
            """The *tree-parsed* storage element producer function."""
            yield None, None
            tmp_tree = Tree(tree_newick_string, format=2)
            yield transformer.reparse_tree(tmp_tree, index_mapper)

        def produce_tree_object(tree_newick_string):
            """The *tree-object* storage element producer function."""
            yield None, None
            yield Tree(tree_newick_string, format=2, quoted_node_names=True)

        def produce_map_tree(tree_object):
            """The *map-tree* storage element producer function."""
            yield None, None
            tmp_rebuilded_tree = transformer.rebuild_phylo(tree_object)
            yield transformer.make_tree_map(tmp_rebuilded_tree)

        merged_tree = Tree(name="root")
        for tree_fp in tree_newick_fp:
            merged_tree.add_child(child=Tree(tree_fp, format=1, quoted_node_names=True))

        tmp_newick_string = storage_manager.commit_to_storage(
            "tree-prior", produce_tree_prior(merged_tree)
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
    def __process_sequence(
        cls,
        storage_manager: DatabaseStorageManager,
        index_mapper: pd.Series,
        removed_rids: np.ndarray,
        prior_recap: pd.Series,
        sequence_fasta_fp: str,
        chunksize: int,
    ) -> pd.Series:
        """Process sequence data.

        Parameters
        ----------
        storage_manager
            Active storage manager
        index_mapper
            Index renamer/mapper
        removed_rids
            Identifiers that must be removed
        prior_recap
            Previous recap data
        sequence_fasta_fp
            Path to FASTA file
        chunksize
            Size of processing chunks

        Returns
        -------

            Results of the process that need to be passed to the builder
        """
        from pmaf.database._parsers._qiime import parse_qiime_sequence_generator

        def produce_sequence_representative(
            sequence_fasta_fp, index_mapper, dropped_taxa, chunksize
        ):
            sequence_parser = parse_qiime_sequence_generator(
                sequence_fasta_fp, chunksize, False
            )
            preparse_info, first_chunk = next(sequence_parser)
            yield preparse_info.copy()
            preparse_info["max_rows"] = preparse_info["max_rows"] - len(dropped_taxa)
            preparse_info.pop("min_sequence")
            yield preparse_info, transformer.reindex_frame(
                first_chunk.drop(index=dropped_taxa, errors="ignore"), index_mapper
            )
            for next_chunk in sequence_parser:
                yield transformer.reindex_frame(
                    next_chunk.drop(index=dropped_taxa, errors="ignore"), index_mapper
                )

        repseq_wrapped_parser = produce_sequence_representative(
            sequence_fasta_fp, index_mapper, removed_rids, chunksize
        )
        tmp_repseq_details = next(repseq_wrapped_parser)
        storage_manager.commit_to_storage(
            "sequence-representative", repseq_wrapped_parser
        )

        tmp_recap = summarizer.merge_recaps(
            prior_recap, summarizer.recap_sequence_info(tmp_repseq_details)
        )
        return tmp_recap

    @classmethod
    def __process_interxmaps(cls, storage_manager: DatabaseStorageManager):
        """Process interx maps.

        Parameters
        ----------
        storage_manager
            Active storage maanger
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
        """Database name/label."""
        return self.DATABASE_NAME
