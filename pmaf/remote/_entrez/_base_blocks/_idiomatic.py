import csv
from io import StringIO
class IdiomaticBase():
    ''' '''
    def __init__(self):
        pass


    def _get_top_chromosome_id(self,chromosome_raw):
        '''

        Args:
          chromosome_raw: 

        Returns:

        '''
        ret = False
        target_id = chromosome_raw[0]["LinkSetDb"][0]['Link'][0]['Id'] if len(chromosome_raw[0]["LinkSetDb"][0]['Link']) > 0 else ret
        ret = target_id
        return ret

    def _get_top_genome_id(self,genome_raw):
        '''

        Args:
          genome_raw: 

        Returns:

        '''
        ret = False
        target_id = genome_raw[0]["LinkSetDb"][0]['Link'][0]['Id'] if len(genome_raw[0]["LinkSetDb"]) > 0 else ret
        ret = target_id
        return ret

    def _get_top_taxid(self,tax_raw):
        '''

        Args:
          tax_raw: 

        Returns:

        '''
        ret = False
        target_id = tax_raw['IdList'][0] if len(tax_raw['IdList']) > 0 else ret
        ret = target_id
        return ret

    def filter_genes_from_future_table(self,seq_raw_io,gene):
        '''

        Args:
          seq_raw_io: 
          gene: 

        Returns:

        '''
        ret = False
        rrna_locus_list = []
        csv_reader = csv.reader(seq_raw_io, delimiter='\t')
        next(csv_reader)
        tmp_locus = {}
        rna_detect = False
        for row in csv_reader:
            row_len = len(row)
            if row_len > 3:
                if rna_detect:
                    if 'product' in row:
                        rrna_locus_list.append([row[4], tmp_locus])
                        tmp_locus = {}
                        rna_detect = False
            if row_len == 3:
                if row[2] == gene:
                    rna_detect = True
                    positive_strand = True if (int(row[0]) < int(row[1])) else False
                    tmp_locus['start'] = row[0] if positive_strand else row[1]
                    tmp_locus['end'] = row[1] if positive_strand else row[0]
                    tmp_locus['strand'] = '1' if positive_strand else '2'
                else:
                    rna_detect = False
        if len(rrna_locus_list)>0:
            ret = rrna_locus_list
        return ret





