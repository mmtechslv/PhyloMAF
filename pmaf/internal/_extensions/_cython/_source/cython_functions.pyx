import csv
from collections import defaultdict

DEF TAXON_LIST_LEN = 10

cpdef list generate_taxa_list_for_ott(list passed_ranks,str file_path,str sep):
    rank2i = {'domain':2,'kingdom':3,'phylum':4,'class':5,'order':6,'family':7,'genus':8,'species':9,'no rank - terminal':9}
    rank2r = {'domain':'d','kingdom':'k','phylum':'p','class':'c','order':'o','family':'f','genus':'g','species':'s','no rank - terminal':'s'}
    cdef list passed_ranks_full = [long_r for long_r, short_r in rank2r.items() if short_r in passed_ranks]
    cdef list taxa_list = []
    taxa_map = defaultdict(list)
    cdef list header = []
    cdef short i_uid = 0
    cdef short i_pid = 0
    cdef short i_name = 0
    cdef short i_rank = 0
    cdef object file_reader = None
    cdef str pid = ''
    cdef list tmp_parent_taxon = []
    cdef bint let_pid_fix = True
    with open(file_path,'r') as file_handle:
        file_reader = csv.reader(file_handle,delimiter=sep)
        header = next(file_reader)
        i_uid = header.index('uid')
        i_pid = header.index('parent_uid')
        i_name = header.index('name')
        i_rank = header.index('rank')
        for line in file_reader:
            taxa_map[line[i_uid]] = line
            taxon_list = [None]*TAXON_LIST_LEN 
            if line[i_rank] in passed_ranks_full:
                taxon_list[rank2i[line[i_rank]]] = line[i_name]
                taxon_list[0] = line[i_uid]
                taxon_list[1] = line[i_pid]
                taxa_list.append(taxon_list)
                
    for taxon_elem in taxa_list:
        uid = taxon_elem[0]
        pid = taxon_elem[1]
        let_pid_fix = True
        while pid != '':
            tmp_parent_taxon = taxa_map[pid]
            if tmp_parent_taxon[i_rank] in passed_ranks_full:
                taxon_elem[rank2i[tmp_parent_taxon[i_rank]]] = tmp_parent_taxon[i_name]
                taxon_elem[1] = pid if let_pid_fix else taxon_elem[1]
                let_pid_fix = False
            pid = tmp_parent_taxon[i_pid]
            
    return taxa_list


cpdef list generate_lineages_from_taxa_list(list taxa_list,bint add_preffix,list passed_ranks):
    cdef int ranks_num = len(passed_ranks)
    cdef int taxa_num = len(taxa_list)
    cdef list new_lineages = [None]*len(taxa_list)
    cdef str tmp_lineage = ''
    cdef str tmp_rank = ''
    for i_taxa in range(taxa_num):
        tmp_lineage = ''
        tmp_rank = ''
        for i_rank in range(ranks_num):
            if taxa_list[i_taxa][i_rank]:
                tmp_rank = passed_ranks[i_rank] + '__' + taxa_list[i_taxa][i_rank] + '; '
            else:
                tmp_rank = passed_ranks[i_rank] + '__' + '; ' if add_preffix else '';
                
            tmp_lineage = tmp_lineage + tmp_rank  # Add succeeding rank to lineage
        new_lineages[i_taxa] =  tmp_lineage[:-2]
    return new_lineages
