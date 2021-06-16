from os import path
from pmaf.database._core._base import DatabaseBase
from pmaf.database._core._tax_base import DatabaseTaxonomyMixin
from pmaf.database._core._seq_base import DatabaseSequenceMixin
from pmaf.database._core._phy_base import DatabasePhylogenyMixin
from pmaf.database._core._acs_base import DatabaseAccessionMixin
from pmaf.database._manager import DatabaseStorageManager
import pmaf.database._shared._assemblers as transformer
import pmaf.database._shared._summarizers as summarizer

class DatabaseGreengenes(DatabaseTaxonomyMixin,DatabaseSequenceMixin,DatabasePhylogenyMixin,DatabaseAccessionMixin,DatabaseBase):
    ''' '''
    DATABASE_NAME = 'Greengenes'
    INVALID_TAXA = 'uncultured'
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def build_database_storage(cls, storage_hdf5_fp,taxonomy_map_csv_fp, tree_newick_fp, sequence_fasta_fp, sequence_alignment_fasta_fp,stamp_dict, force=False, chunksize=500, **kwargs):
        '''

        Args:
          storage_hdf5_fp: 
          taxonomy_map_csv_fp: 
          tree_newick_fp: 
          sequence_fasta_fp: 
          sequence_alignment_fasta_fp: 
          stamp_dict: 
          force: (Default value = False)
          chunksize: (Default value = 500)
          **kwargs: 

        Returns:

        '''
        if path.exists(storage_hdf5_fp) and not force:
            raise ValueError('Storage file exists.')
        if not path.isfile(taxonomy_map_csv_fp):
            raise ValueError('Invalid taxonomy CSV/TSV file path provided.')
        if not path.isfile(tree_newick_fp):
            raise ValueError('Invalid tree Newick file path provided.')
        if not path.isfile(sequence_fasta_fp):
            raise ValueError('Invalid sequence FASTA file path provided.')
        if not path.isfile(sequence_alignment_fasta_fp):
            raise ValueError('Invalid alignment FASTA file path provided.')
        if isinstance(chunksize,int):
            if chunksize<=0:
                raise ValueError('`chunksize` must be greater than zero.')
        else:
            raise TypeError('`chunksize` must be integer.')

        tmp_storage_manager = DatabaseStorageManager(hdf5_filepath=storage_hdf5_fp, storage_name=cls.DATABASE_NAME, force_new=force)

        removed_rids,novel_tids, index_mapper, tmp_recap = cls.__process_tax_acs_map(tmp_storage_manager, taxonomy_map_csv_fp)
        cls.__process_tree(tmp_storage_manager, tree_newick_fp, index_mapper)

        tmp_recap = cls.__process_sequence(tmp_storage_manager, index_mapper, removed_rids, tmp_recap, sequence_fasta_fp, sequence_alignment_fasta_fp, chunksize)

        tmp_storage_manager.commit_to_storage('stat-reps', transformer.produce_rep_stats(tmp_storage_manager, chunksize))
        tmp_storage_manager.commit_to_storage('stat-taxs', transformer.produce_tax_stats(tmp_storage_manager, novel_tids))

        cls.__process_interxmaps(tmp_storage_manager)

        return transformer.finalize_storage_construction(tmp_storage_manager, stamp_dict, tmp_recap, **kwargs)

    @classmethod
    def __process_tax_acs_map(cls, storage_manager, taxonomy_map_csv_fp):
        from pmaf.database._parsers._qiime import read_qiime_taxonomy_map, parse_qiime_taxonomy_map
        def produce_taxonomy_prior(tmp_taxonomy_prior, index_mapper):
            '''

            Args:
              tmp_taxonomy_prior: 
              index_mapper: 

            Returns:

            '''
            yield None, None
            yield transformer.reindex_frame(tmp_taxonomy_prior, index_mapper)

        def produce_taxonomy_sheet(taxonomy_sheet):
            '''

            Args:
              taxonomy_sheet: 

            Returns:

            '''
            yield None, None
            yield taxonomy_sheet

        def produce_sequence_accession(index_mapper, dropped_taxa):
            '''

            Args:
              index_mapper: 
              dropped_taxa: 

            Returns:

            '''
            yield None, None
            tmp_accessions = index_mapper.drop(index=dropped_taxa, errors='ignore').reset_index(name='nrids').set_index('nrids')
            tmp_accessions.columns = ['greengenes']
            yield tmp_accessions

        def produce_metadata_db_history(transformation_details):
            '''

            Args:
              transformation_details: 

            Returns:

            '''
            yield None, None
            yield transformation_details['changes']

        def produce_map_rep2tid(transformation_details):
            '''

            Args:
              transformation_details: 

            Returns:

            '''
            yield None, None
            yield transformation_details['map-rep2tid']

        tmp_taxonomy_prior = read_qiime_taxonomy_map(taxonomy_map_csv_fp)
        index_mapper = transformer.make_rid_index_mapper(tmp_taxonomy_prior.index)
        taxonomy_prior = storage_manager.commit_to_storage('taxonomy-prior',produce_taxonomy_prior(tmp_taxonomy_prior,index_mapper))
        tmp_taxonomy_sheet_master = parse_qiime_taxonomy_map(taxonomy_prior)
        taxonomy_sheet, transformation_details = transformer.reconstruct_taxonomy(tmp_taxonomy_sheet_master,index_mapper,cls.INVALID_TAXA)
        removed_rids = transformation_details['removed-rids']
        storage_manager.commit_to_storage('taxonomy-sheet', produce_taxonomy_sheet(taxonomy_sheet))
        tmp_recap = summarizer.merge_recaps(summarizer.recap_taxonomy_sheet(taxonomy_sheet), summarizer.recap_transformation(transformation_details))
        tmp_recap = summarizer.append_recaps(tmp_recap,{'molecule-type':'DNA','strand-orientation':'forward','gene':'rRNA','gene-target-region':'16S'})
        storage_manager.commit_to_storage('sequence-accession', produce_sequence_accession(index_mapper,removed_rids))
        storage_manager.commit_to_storage('metadata-db-history', produce_metadata_db_history(transformation_details))
        storage_manager.commit_to_storage('map-rep2tid', produce_map_rep2tid(transformation_details))
        return removed_rids,transformation_details['novel-tids'], index_mapper, tmp_recap

    @classmethod
    def __process_tree(cls,storage_manager,tree_newick_fp,index_mapper):
        from pmaf.database._parsers._phylo import read_newick_tree
        from ete3 import Tree

        def produce_tree_prior(tree_newick_fp):
            '''

            Args:
              tree_newick_fp: 

            Returns:

            '''
            yield None, None
            yield read_newick_tree(tree_newick_fp)

        def produce_tree_parsed(tree_newick_string, index_mapper):
            '''

            Args:
              tree_newick_string: 
              index_mapper: 

            Returns:

            '''
            yield None, None
            tmp_tree = Tree(tree_newick_string, format=0)
            yield transformer.reparse_tree(tmp_tree, index_mapper)

        def produce_tree_object(tree_newick_string):
            '''

            Args:
              tree_newick_string: 

            Returns:

            '''
            yield None, None
            yield Tree(tree_newick_string, format=2,quoted_node_names=True)

        def produce_map_tree( tree_object):
            '''

            Args:
              tree_object: 

            Returns:

            '''
            yield None, None
            tmp_rebuilded_tree = transformer.rebuild_phylo(tree_object)
            yield transformer.make_tree_map(tmp_rebuilded_tree)

        tmp_newick_string = storage_manager.commit_to_storage('tree-prior', produce_tree_prior(tree_newick_fp))
        tmp_newick_parsed = storage_manager.commit_to_storage('tree-parsed', produce_tree_parsed(tmp_newick_string,index_mapper))
        tmp_tree_object = storage_manager.commit_to_storage('tree-object', produce_tree_object(tmp_newick_parsed))
        storage_manager.commit_to_storage('map-tree', produce_map_tree(tmp_tree_object))

        return

    @classmethod
    def __process_sequence(cls,storage_manager, index_mapper, removed_rids, prior_recap, sequence_fasta_fp, sequence_alignment_fasta_fp, chunksize):
        from pmaf.database._parsers._qiime import parse_qiime_sequence_generator
        def produce_sequence_representative(sequence_fasta_fp, index_mapper, dropped_taxa, chunksize):
            '''

            Args:
              sequence_fasta_fp: 
              index_mapper: 
              dropped_taxa: 
              chunksize: 

            Returns:

            '''
            sequence_parser = parse_qiime_sequence_generator(sequence_fasta_fp, chunksize, False)
            preparse_info, first_chunk = next(sequence_parser)
            yield preparse_info.copy()
            preparse_info['max_rows'] = preparse_info['max_rows'] - len(dropped_taxa)
            preparse_info.pop('min_sequence')
            yield preparse_info, transformer.reindex_frame(first_chunk.drop(index=dropped_taxa, errors='ignore'), index_mapper)
            for next_chunk in sequence_parser:
                yield transformer.reindex_frame(next_chunk.drop(index=dropped_taxa, errors='ignore'), index_mapper)

        def produce_sequence_aligned(sequence_alignment_fasta_fp, index_mapper, dropped_taxa, chunksize):
            '''

            Args:
              sequence_alignment_fasta_fp: 
              index_mapper: 
              dropped_taxa: 
              chunksize: 

            Returns:

            '''
            sequence_parser = parse_qiime_sequence_generator(sequence_alignment_fasta_fp, chunksize, True)
            preparse_info, first_chunk = next(sequence_parser)
            yield preparse_info.copy()
            preparse_info['max_rows'] = preparse_info['max_rows'] - len(dropped_taxa)
            preparse_info.pop('min_sequence')
            yield preparse_info, transformer.reindex_frame(first_chunk.drop(index=dropped_taxa, errors='ignore'), index_mapper)
            for next_chunk in sequence_parser:
                yield transformer.reindex_frame(next_chunk.drop(index=dropped_taxa, errors='ignore'), index_mapper)

        repseq_wrapped_parser = produce_sequence_representative(sequence_fasta_fp,index_mapper,removed_rids,chunksize)
        tmp_repseq_details = next(repseq_wrapped_parser)
        storage_manager.commit_to_storage('sequence-representative', repseq_wrapped_parser)

        alignment_wrapped_parser = produce_sequence_aligned(sequence_alignment_fasta_fp,index_mapper,removed_rids,chunksize)
        tmp_alignment_details = next(alignment_wrapped_parser)
        storage_manager.commit_to_storage('sequence-aligned', alignment_wrapped_parser)

        tmp_recap = summarizer.merge_recaps(prior_recap, summarizer.recap_sequence_info(tmp_repseq_details, tmp_alignment_details))
        return tmp_recap

    @classmethod
    def __process_interxmaps(cls, storage_manager):
        def produce_map_interx_taxon(interx_maker_result):
            '''

            Args:
              interx_maker_result: 

            Returns:

            '''
            yield None, None
            yield interx_maker_result['map-interx-taxon']

        def produce_map_interx_repseq(interx_maker_result):
            '''

            Args:
              interx_maker_result: 

            Returns:

            '''
            yield None, None
            yield interx_maker_result['map-interx-repseq']

        tmp_interx_result = transformer.make_interxmaps(storage_manager)
        storage_manager.commit_to_storage('map-interx-taxon', produce_map_interx_taxon(tmp_interx_result))
        storage_manager.commit_to_storage('map-interx-repseq', produce_map_interx_repseq(tmp_interx_result))
        return

    @property
    def name(self):
        ''' '''
        return self.DATABASE_NAME






