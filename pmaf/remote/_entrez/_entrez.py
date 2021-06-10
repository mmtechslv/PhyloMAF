from ._base import EntrezBase


class Entrez(EntrezBase):
    ''' '''
    def __init__(self, email, api_key=None, tool='PhyloMAF'):
        super().__init__(email, api_key, tool)

    def get_taxid_by_query(self,query):
        '''

        Args:
          query: 

        Returns:

        '''
        ret = False
        raw_data = self._request_taxid_by_query(query)
        if raw_data:
            taxid = self._get_top_taxid(raw_data)
            ret = taxid
        return ret

    def get_genome_id_by_taxid(self,taxid):
        '''

        Args:
          taxid: 

        Returns:

        '''
        ret = False
        raw_data = self._request_genomes_by_taxid(taxid)
        if raw_data:
            genome_id = self._get_top_genome_id(raw_data)
            ret = genome_id
        return ret

    def get_chromosome_id_by_genome_id(self,genome_id):
        '''

        Args:
          genome_id: 

        Returns:

        '''
        ret = False
        raw_data = self._request_chromosomes_by_genome_id(genome_id)
        if raw_data:
            chromosome_id = self._get_top_chromosome_id(raw_data)
            ret = chromosome_id
        return ret

    def get_gene_features_by_chromosome_id(self,chromosome_id,gene='rRNA'):
        '''

        Args:
          chromosome_id: 
          gene: (Default value = 'rRNA')

        Returns:

        '''
        ret = False
        raw_io = self._request_sequence_feature_table_by_acc_id(chromosome_id,True)
        if raw_io:
            gene_features = self.filter_genes_from_future_table(raw_io, gene)
            raw_io.close()
            ret = gene_features
        return ret

    def get_fasta_sequence_by_param(self, accession_id, start_pos, stop_pos, strand):
        '''

        Args:
          accession_id: 
          start_pos: 
          stop_pos: 
          strand: 

        Returns:

        '''
        ret = False
        if strand in ['1','2']:
            ret = self._request_sequence_fasta(accession_id,start_pos,stop_pos,strand)
        return ret








