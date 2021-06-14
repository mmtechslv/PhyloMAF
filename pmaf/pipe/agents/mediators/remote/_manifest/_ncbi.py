from pmaf.pipe.agents.mediators._base import MediatorBase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase
from pmaf.remote._entrez._metakit import EntrezBackboneMetabase
from pmaf.pipe.agents.mediators._metakit import MediatorSequenceMetabase,MediatorTaxonomyMetabase,MediatorAccessionMetabase
from pmaf.pipe.agents.dockers._metakit import DockerIdentifierMetabase,DockerAccessionMetabase,DockerSequenceMetabase,DockerTaxonomyMetabase
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._acs_medium import DockerAccessionMedium
from pmaf.pipe.agents.dockers._mediums._seq_medium import DockerSequenceMedium
from pmaf.internal._shared import sort_ranks
from pmaf.alignment.multiple._metakit import MultiSequenceAlignerBackboneMetabase
from pmaf.internal._constants import ITS
from pmaf.internal.io._seq import SequenceIO


class NCBIMediator(MediatorBase,MediatorSequenceMetabase,MediatorTaxonomyMetabase,MediatorAccessionMetabase):
    ''' '''
    SEQ_EXTRACT_METHODS = ['asis','consensus']
    def __init__(self,entrez,
                 seq_method='asis',
                 seq_aligner=None, **kwargs):
        if not isinstance(entrez,EntrezBackboneMetabase):
            TypeError('`entrez` has invalid type.')
        if not entrez.state:
            raise ValueError('`entrez` have invalid state.')

        if isinstance(seq_method, str):
            if seq_method not in self.SEQ_EXTRACT_METHODS:
                raise ValueError('`seq_method` is unknown.')
        else:
            raise TypeError('`seq_method` has invalid type.')
        if seq_aligner is not None:
            if not isinstance(seq_aligner, MultiSequenceAlignerBackboneMetabase):
                raise TypeError('`seq_aligner` has invalid type.')

        if seq_method == 'consensus' and not seq_aligner is not None:
            raise ValueError('`seq_method` in consensus mode require valid `seq_aligner`.')
        tmp_configs = dict(seq_method=seq_method,seq_aligner=seq_aligner)
        super().__init__(_client=entrez,_configs=tmp_configs,**kwargs)

    def __repr__(self):
        class_name = self.__class__.__name__
        client_class_name  = 'Entrez API'
        state = 'Active' if self.client.state else 'Inactive'
        repr_str = "<{}:[{}], Client:[{}]>".format(class_name, state, client_class_name)
        return repr_str

    def verify_factor(self, factor):
        '''

        Args:
          factor: 

        Returns:

        '''
        if isinstance(factor,FactorBackboneMetabase):
            gene_type = factor.factors.get('gene-type', None) == 'marker'
            molecule_type = factor.factors.get('molecule-type',None) in ['DNA','RNA']
            gene_name = factor.factors.get('gene-name', None) in ['rRNA']
            gene_target = factor.factors.get('gene-target', None) in ['16S','18S','ITS']
            return all([gene_type,molecule_type,gene_name,gene_target])
        else:
            raise TypeError('`factor` has invalid type.')

    def get_sequence_by_identifier(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        if not self.verify_factor(factor):
            raise ValueError('`factor` is invalid.')
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_sequence_by_identifier(docker, factor, **kwargs)
            else:
                raise ValueError('`docker` must be singleton.')
        else:
            raise TypeError('`docker` must be instance of DockerIdentifierMetabase.')

    def get_accession_by_identifier(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        if not self.verify_factor(factor):
            raise ValueError('`factor` is invalid.')
        if isinstance(docker, DockerIdentifierMetabase):
            if docker.singleton:
                return self.__retrieve_accession_by_identifier(docker)
            else:
                raise ValueError('`docker` must be singleton.')
        else:
            raise TypeError('`docker` must be instance of DockerIdentifierMetabase.')

    def get_identifier_by_accession(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        raise NotImplementedError

    def get_identifier_by_sequence(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        raise NotImplementedError

    def get_taxonomy_by_identifier(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        raise NotImplementedError

    def get_identifier_by_taxonomy(self, docker, factor, **kwargs):
        '''

        Args:
          docker: 
          factor: 
          **kwargs: 

        Returns:

        '''
        if not self.verify_factor(factor):
            raise ValueError('`factor` is invalid.')
        if isinstance(docker, DockerTaxonomyMetabase):
            if docker.singleton:
                return self.__retrieve_identifier_by_taxonomy(docker, **kwargs)
            else:
                raise ValueError('`docker` must be singleton.')
        else:
            raise TypeError('`docker` must be instance of DockerTaxonomyMetabase.')

    def __retrieve_identifier_by_taxonomy(self,docker,**kwargs):
        tmp_identifiers = dict.fromkeys(docker.index, None)
        tmp_query_metadata = dict.fromkeys(docker.valid, None)
        for ix, taxonomy in docker.get_iterator(exclude_missing=True):
            tmp_query = self.__make_query_for_taxonomy_entry(taxonomy)
            tmp_taxid = self.client.get_taxid_by_query(tmp_query)
            if tmp_taxid:
                tmp_identifiers[ix] = tmp_taxid
                tmp_query_metadata[ix] = tmp_query
        new_metadata = {'queries': tmp_query_metadata, 'master': docker.wrap_meta()}
        return DockerIdentifierMedium(tmp_identifiers, name=docker.name, metadata=new_metadata)

    def __make_query_for_taxonomy_entry(self, taxonomy):
        taxa_dict = {k:v for k,v in taxonomy.items() if v is not None}
        ordered_ranks = sort_ranks(taxa_dict.keys())
        target_rank = ordered_ranks[-1]
        target_taxon = taxa_dict[target_rank]
        target_rank_full = ITS['r2rank'][target_rank]
        ancestors = [taxon for rank,taxon in taxa_dict.items() if rank != target_rank]
        ancestors_query = ' OR '.join(['{}[Subtree]'.format(taxon) for taxon in ancestors])
        target_query = '{}[All Names] AND {}[Rank]'.format(target_taxon, target_rank_full)
        query = '({}) AND ({})'.format(ancestors_query, target_query)
        return query

    def __retrieve_accession_by_identifier(self, docker):
        tmp_accession = dict.fromkeys(docker.index, None)
        tmp_metadata = dict.fromkeys(docker.valid, None)
        for ix, taxid in docker.get_iterator(exclude_missing=True):
            tmp_taxid_metadata = {'tax-id':taxid,'genome-id':None,'chromosome-id':None}
            tmp_genome_id = self.client.get_genome_id_by_taxid(taxid)
            if tmp_genome_id:
                tmp_taxid_metadata['genome-id'] = tmp_genome_id
                tmp_chromosome_id = self.client.get_chromosome_id_by_genome_id(tmp_genome_id)
                if tmp_chromosome_id:
                    tmp_taxid_metadata['chromosome-id'] = tmp_chromosome_id
                    tmp_accession[ix] = {'ncbi':tmp_chromosome_id}
            tmp_metadata[ix] = tmp_taxid_metadata
        new_metadata = {'verbose': tmp_metadata, 'master': docker.wrap_meta()}
        return DockerAccessionMedium(tmp_accession, name=docker.name, metadata=new_metadata)

    def __retrieve_sequence_by_identifier(self,docker, factor, **kwargs):
        tmp_sequences = dict.fromkeys(docker.index, None)
        tmp_metadata = dict.fromkeys(docker.valid, None)
        target_gene_filter = factor.factors['gene-target'].lower().strip()
        for ix, accession_no in docker.get_iterator(exclude_missing=True):
            tmp_features = self.client.get_gene_features_by_chromosome_id(accession_no, factor.factors['gene-name'])
            if tmp_features:
                tmp_copy_sequences_str = ''
                tmp_copy_metadata = []
                tmp_copy_names = []
                for feature_id, feature_details in enumerate(tmp_features):
                    feature_genes_adj = feature_details[0].lower().strip()
                    if target_gene_filter in feature_genes_adj:
                        tmp_copy_name = "{}-{}".format(str(ix),str(feature_id))
                        tmp_copy_names.append(tmp_copy_name)
                        tmp_start_pos = feature_details[1]['start']
                        tmp_end_pos = feature_details[1]['end']
                        tmp_strand = feature_details[1]['strand']
                        tmp_fasta_str = self.client.get_fasta_sequence_by_param(str(accession_no), str(tmp_start_pos), str(tmp_end_pos), str(tmp_strand))
                        tmp_copy_sequences_str += "{}\n".format(tmp_fasta_str)
                        tmp_copy_metadata.append({'start':tmp_start_pos,'end':tmp_end_pos,'strand':tmp_strand,'gene-target':feature_genes_adj,'gene-name':factor.factors['gene-name'],'accession':accession_no})
                tmp_copy_sequences_dict = dict.fromkeys(tmp_copy_names,None)
                tmp_copy_metadata_dict = dict.fromkeys(tmp_copy_names,None)
                tmp_copy_counter = 0
                for fasta_id,fasta_desc,seq_str in SequenceIO(tmp_copy_sequences_str,ftype='fasta',upper=True).pull_parser(id=True,description=True,sequence=True):
                    tmp_copy_name_x = tmp_copy_names[tmp_copy_counter]
                    tmp_copy_metadata_adj = {**tmp_copy_metadata[tmp_copy_counter],**{'fasta-id':fasta_id,'fasta-description':fasta_desc}}
                    tmp_copy_metadata_dict[tmp_copy_name_x] = tmp_copy_metadata_adj
                    tmp_copy_sequences_dict[tmp_copy_name_x] = seq_str
                    tmp_copy_counter += 1
                tmp_sequences[ix] = self.__transform_sequence_for_method(DockerSequenceMedium(tmp_copy_sequences_dict,mode=None,name=ix,metadata=tmp_copy_metadata_dict))
                tmp_metadata[ix] = {'accession':accession_no,'copy-number':len(tmp_copy_sequences_dict),'verbose':tmp_copy_metadata_dict,'gene-name':factor.factors['gene-name']}
        new_metadata = {'verbose': tmp_metadata, 'master': docker.wrap_meta()}
        return DockerSequenceMedium(tmp_sequences, mode=None, name=docker.name, metadata=new_metadata)

    def __transform_sequence_for_method(self,sequence_docker):
        if self.configs['seq_method'] == 'consensus' and isinstance(self.configs['seq_aligner'], MultiSequenceAlignerBackboneMetabase):
            if sequence_docker.count > 1:
                return self.configs['seq_aligner'].align(sequence_docker.to_multiseq()).get_consensus().text
            else:
                return next(iter(sequence_docker.data.values()))
        else:
            return sequence_docker

    @property
    def state(self):
        ''' '''
        return self.client.state