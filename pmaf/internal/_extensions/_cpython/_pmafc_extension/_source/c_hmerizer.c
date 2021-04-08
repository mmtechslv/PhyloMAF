#include <stdio.h>
#include <stdlib.h>
#include "c_hmerizer.h"

// Following are IUPAC ambiguous base branches that are used for ambiguous map generation.
const char *IUPAC_R = "AG";
const char *IUPAC_Y = "CT";
const char *IUPAC_S = "GC";
const char *IUPAC_W = "AT";
const char *IUPAC_K = "GT";
const char *IUPAC_M = "AC";
const char *IUPAC_B = "CGT";
const char *IUPAC_D = "AGT";
const char *IUPAC_H = "ACT";
const char *IUPAC_V = "ACG";
const char *IUPAC_N = "ACTG";
const char *IUPAC_AMBIGUOUS = "RYSWKMBDHVN";


MAXKMERS_INT upow(int base, int power)
{
    MAXKMERS_INT result = 1;
    int power_i;
    for (power_i=0; power_i < power; power_i++)
    {
        result *= (MAXKMERS_INT)base;
    }
    return result;
}

// This is secondary helper function that was used to make record element.
PMAF_CEXT_ERROR make_record_element(STRUCT_SEQ_RECORD_ELEM **record_element, unsigned long seq_id, char* seq_str, int seq_len, int seq_tab)
{
    *record_element = (STRUCT_SEQ_RECORD_ELEM *)malloc(sizeof(STRUCT_SEQ_RECORD_ELEM));
    if (*record_element == NULL) { return ERR_MEMALC_RECORD_ELEMENT; }

    (*record_element)->seq_id = seq_id;
    (*record_element)->seq_str = seq_str;
    (*record_element)->seq_len = seq_len;
    (*record_element)->seq_tab = seq_tab;

    return ERR_NO_ERROR;
}

// This is the function that generates pre-hashed and packed non-ambiguous bases from given ambiguous_branch.
HASHMASK_WORD hashmask_ambiguous_base(const char *ambiguous_branch,int total_base)
{
    int amb_branch_i;
    HASHMASK_WORD hash_buffer,hash_mask_buffer;
    hash_mask_buffer = 0;
    for (amb_branch_i = 0; amb_branch_i < total_base; amb_branch_i++)
    {
        hash_buffer = (HASHMASK_WORD)ambiguous_branch[amb_branch_i];
        hash_buffer = (hash_buffer >> 1) & 3;
        hash_mask_buffer = hash_mask_buffer << 2;
        hash_mask_buffer = hash_mask_buffer | hash_buffer;
    }
    return hash_mask_buffer;
}

// This is primary function that generates ambiguous map from the original sequence.
// Ambiguous map is a STRUCT_MAP_ELEM array that contain STRUCT_MAP_ELEM struct element for each ambiguous base within sequence.
// Each STRUCT_MAP_ELEM contain the position of the ambiguous base, total number of non-ambiguous bases as well as its pre-hashed and packed non-ambiguous bases.
PMAF_CEXT_ERROR make_ambiguous_map(STRUCT_MAP_ELEM **ambiguous_map_start, char *seq_str,int seq_len,int seq_tab)
{
    STRUCT_MAP_ELEM *ambiguous_map;
    char ab;
    int seq_str_i;
    *ambiguous_map_start = (STRUCT_MAP_ELEM *)malloc(seq_tab * sizeof(STRUCT_MAP_ELEM));
    if (*ambiguous_map_start == NULL) { return ERR_MEMALC_AMBIGUOUS_MAP; }
    ambiguous_map = *ambiguous_map_start;
    for(seq_str_i = 0; seq_str_i < seq_len; seq_str_i++)
    {
        ab = seq_str[seq_str_i];
        switch(ab)
        {
            case 'R':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_R,2);
                ambiguous_map++;
                break;
            case 'Y':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_Y,2);
                ambiguous_map++;
                break;
            case 'S':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_S,2);
                ambiguous_map++;
                break;
            case 'W':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_W,2);;
                ambiguous_map++;
                break;
            case 'K':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_K,2);;
                ambiguous_map++;
                break;
            case 'M':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 2;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_M,2);;
                ambiguous_map++;
                break;
            case 'B':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 3;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_B,3);;
                ambiguous_map++;
                break;
            case 'D':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 3;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_D,3);;
                ambiguous_map++;
                break;
            case 'H':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 3;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_H,3);;
                ambiguous_map++;
                break;
            case 'V':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 3;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_V,3);;
                ambiguous_map++;
                break;
            case 'N':
                ambiguous_map->pos = seq_str_i;
                ambiguous_map->total = 4;
                ambiguous_map->branch = hashmask_ambiguous_base(IUPAC_N,4);;
                ambiguous_map++;
                break;
        }
    }
    return ERR_NO_ERROR;
}

// This is main function that produces whole sequence hashmask from the provided ambiguous_map.
// Function simply breaks each base of `char` data type into `HASHMASK_WORD` data type. For non-ambiguous bases this is straightforward operation that simply encodes that ASCII code in two bits and stores in HASHMASK_WORD.
// But in order to efficiently parse hashmask sequence, it was decided to mask ambiguous bases with array positions of ambiguous_map struct array.
// However, in order to precisely differentiate simple base from masked 256 value is added to each ambiguous base positions within hashmask or HASHMASK_WORD array.
// This approach should explain why HASHMASK_WORD is prefered in hasmask insead of HASHBASE_BYTE.
PMAF_CEXT_ERROR make_sequence_hashmask(HASHMASK_WORD **sequence_hashmask, char *seq_str, STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int seq_tab)
{
    int seq_str_i, seq_tab_i;
    HASHMASK_WORD hash_buffer;
    *sequence_hashmask = (HASHMASK_WORD *)malloc(seq_len*sizeof(HASHMASK_WORD));
    if (*sequence_hashmask == NULL) { return ERR_MEMALC_HASHMASK; }
    for(seq_str_i = 0; seq_str_i < seq_len; seq_str_i++)
    {
        hash_buffer  = (HASHMASK_WORD)seq_str[seq_str_i];
        hash_buffer = (hash_buffer >> 1) & 3;
        (*sequence_hashmask)[seq_str_i] = hash_buffer;
    }
    for (seq_tab_i = 0; seq_tab_i < seq_tab; seq_tab_i++)
    {
        (*sequence_hashmask)[ambiguous_map[seq_tab_i].pos] = 256 + seq_tab_i;//Safeguard. Guarantie that kmerize_hash_sequence_for_ksize() function will not make any mistake during rapid branch identification.
    }
    return ERR_NO_ERROR;
}

// Following function iterates over whole sequence hashmask starting from seq_offset and ending with seq_offset + kmer_size.
// Doing so it finds masked ambiguous_map positions from hashmask which are supposed to be larger than 255 by design and then recalculates total number of deambigated sub-kmer sequences.
// Previous approach was to precalculate all possible total subseqs for whole sequence but that approach failed since some sequences may have to many ambiguous bases that could produce very large numbers way beyond any datatype can store.
// Hence, this approach only focuses on single kmer so it also limited by kmer. So if any kmer contain such a combination of ambiguous bases that in a factorial manner produces total subseqs number larger than size_t data type then this parsing will fail and produce memory error.
MAXKMERS_INT calc_total_subseqs(HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, int seq_offset, int kmer_size)
{
    int  seq_str_i;
    MAXKMERS_INT total_seq_count = 1;
    for (seq_str_i=seq_offset;seq_str_i<(seq_offset+kmer_size);seq_str_i++)
    {
        if (sequence_hashmask[seq_str_i]>255)
        {
            total_seq_count *= ambiguous_map[sequence_hashmask[seq_str_i] - 256].total;
        }
    }
    return total_seq_count;
}

// Following function takes whole sequence hashmask and deambiguates part of the hashmask that start with seq_offset and ends with seq_offset + kmer_size
// Since total number of subseqs is precalculated from ambiguous mask. This function it does not count generated kmers.
// This function theoretically can is limited by size_t. So in cases where all bases in kmer is ambiguous it should deambiguate it.
void deambiguate_hashmask(HASHBASE_BYTE **kmer_hashmask_array, HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, MAXKMERS_INT total_subseqs, int seq_offset, int kmer_size)
{
    int kmer_i, tab_i, ami;
    MAXKMERS_INT kmer_total_i, bsi_segment_step, bsi_segment_start, cumprod_aml, bsi_segment_i, bse_segment_end, bsi;
    HASHMASK_WORD hashmask_base_buffer, hashmask_branch_buffer, hashmask_branch_base_buffer;

    cumprod_aml = 1;
    for (kmer_i = 0;kmer_i<kmer_size;kmer_i++)
    {
        hashmask_base_buffer = sequence_hashmask[seq_offset+kmer_i];
        if (hashmask_base_buffer>255)
        {
            tab_i = (int)hashmask_base_buffer - 256;
            hashmask_branch_buffer = ambiguous_map[tab_i].branch;
            cumprod_aml = cumprod_aml*ambiguous_map[tab_i].total;
            bsi_segment_step = total_subseqs/cumprod_aml;
            bsi_segment_start = 0;
            ami = 0;
            for(bsi_segment_i=0;bsi_segment_i<cumprod_aml;bsi_segment_i++)
            {
                hashmask_branch_base_buffer = (hashmask_branch_buffer >> (2*ami)) & 3;
                bse_segment_end = bsi_segment_start + bsi_segment_step;
                for(bsi=bsi_segment_start;bsi<bse_segment_end;bsi++)
                {
                    kmer_hashmask_array[bsi][kmer_i] = (HASHBASE_BYTE)hashmask_branch_base_buffer;
                }
                bsi_segment_start = bse_segment_end;
                ami = ami + 1;
                if (ami == ambiguous_map[tab_i].total)
                {
                    ami = 0;
                }
            }
        }
        else
        {
            for (kmer_total_i = 0; kmer_total_i < total_subseqs; kmer_total_i++)
            {
                kmer_hashmask_array[kmer_total_i][kmer_i] = (HASHBASE_BYTE)hashmask_base_buffer;
            }
        }
    }

    return;
}

//Following function takes as input hashmask array of all possible deambugauted kmers and transforms them into packed hash values of size HASH_INT
void hashmerize_hashmask_kmer(HASH_INT *hash_array, HASHBASE_BYTE **kmer_hashmask_array, MAXKMERS_INT total_subseqs, int kmer_size)
{
    int kmer_i;
    MAXKMERS_INT kmer_total_i;
    HASH_INT tmp_hmer_ref,tmp_hmer_target;
    for (kmer_total_i = 0; kmer_total_i < total_subseqs; kmer_total_i++)
    {
        tmp_hmer_ref = 0;
        for (kmer_i=0; kmer_i<kmer_size; kmer_i++)
        {
            tmp_hmer_target = (HASH_INT)kmer_hashmask_array[kmer_total_i][kmer_i];
            tmp_hmer_ref = tmp_hmer_ref << 2;
            tmp_hmer_ref = tmp_hmer_ref | tmp_hmer_target;
        }
        tmp_hmer_ref = tmp_hmer_ref + (HASH_INT)upow(2,2*kmer_size);
        hash_array[kmer_total_i] = tmp_hmer_ref;
    }
    return;
}

// Following functions adds new hash values to primary hash array and increases hash counter by added hash values.
void append_hash_to_array(STRUCT_HMER_PACK_ELEM  *ref_hash_pack_array, MAXKMERS_INT  *ref_hash_count, HASH_INT *hash_array, unsigned long hmer_pos, MAXKMERS_INT hash_count)
{
    int hash_exist;
    MAXKMERS_INT ref_hash_i,hash_i,ref_hash_count_current;

    ref_hash_count_current = *ref_hash_count;

    for (hash_i = 0;hash_i < hash_count; hash_i++)
    {
        hash_exist = 0;
        for (ref_hash_i=0; ref_hash_i < ref_hash_count_current; ref_hash_i++)
        {
            if (ref_hash_pack_array[ref_hash_i].hmer == hash_array[hash_i])
            {
                hash_exist = 1;
                break;
            }
        }
        if (!hash_exist)
        {
            ref_hash_pack_array[*ref_hash_count].hmer = hash_array[hash_i];
            ref_hash_pack_array[*ref_hash_count].first_pos = hmer_pos;
            ref_hash_pack_array[*ref_hash_count].last_pos = hmer_pos;
            *ref_hash_count = (*ref_hash_count) + 1;
        }
        else
        {
            ref_hash_pack_array[ref_hash_i].last_pos = hmer_pos;
        }
    }
    return;
}

// Calculate maximum number of possible subseqs. Reduce overhead and memory fragmentation.
void calc_memory_buffer_limits(MAXKMERS_INT *max_total_subseqs, int *max_kmer_size, HASHMASK_WORD *sequence_hashmask,STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int *kmer_sizes, int kmer_size_total)
{
    int total_kmers, kmer_size_i, seq_str_i;
    MAXKMERS_INT total_subseqs;
    *max_total_subseqs = 1;
    *max_kmer_size = 0;
    for (kmer_size_i = 0;kmer_size_i < kmer_size_total;kmer_size_i++)
    {
        if (*max_kmer_size < kmer_sizes[kmer_size_i])
        {
            *max_kmer_size = kmer_sizes[kmer_size_i];
        }
        total_kmers = seq_len - kmer_sizes[kmer_size_i] + 1;
        for (seq_str_i=0;seq_str_i<total_kmers;seq_str_i++)
        {
            total_subseqs = calc_total_subseqs(sequence_hashmask,ambiguous_map,seq_str_i,kmer_sizes[kmer_size_i]);
            if (*max_total_subseqs<total_subseqs)
            {
                *max_total_subseqs = total_subseqs;
            }
        }
    }
    return;
}

// Initiate kmer_hashmask_array and hash_array for deambiguate_hashmask and hashmerize_hashmask_kmer, respectively. 
PMAF_CEXT_ERROR allocate_memory_buffer(HASHBASE_BYTE ***kmer_hashmask_array, HASH_INT **hash_array, MAXKMERS_INT max_total_subseqs,int max_kmer_size)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    MAXKMERS_INT total_subseqs_i;

    *kmer_hashmask_array = (HASHBASE_BYTE **)calloc(max_total_subseqs,sizeof(HASHBASE_BYTE *));
    if (*kmer_hashmask_array == NULL) { return ERR_MEMALC_DEAMBIG; }
    *hash_array = (HASH_INT *)calloc(max_total_subseqs,sizeof(HASH_INT));
    if (*hash_array == NULL) { return ERR_MEMALC_HASHMERIZE; }
    for (total_subseqs_i = 0; total_subseqs_i<max_total_subseqs; total_subseqs_i++)
    {
        (*kmer_hashmask_array)[total_subseqs_i] = (HASHBASE_BYTE *)malloc(max_kmer_size*sizeof(HASHBASE_BYTE *));
        if ((*kmer_hashmask_array)[total_subseqs_i] == NULL) { return ERR_MEMALC_DEAMBIG; }
    }
    return err_code;
}

void kmerize_hashmask_sequence_for_ksize(HASHBASE_BYTE **kmer_hashmask_array, HASH_INT *hash_array, STRUCT_HMER_PACK_ELEM *ref_hash_pack_array, MAXKMERS_INT *ref_hash_count, HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int kmer_size)
{
    unsigned long total_kmers, seq_str_i;
    MAXKMERS_INT total_subseqs;
    total_kmers = seq_len - kmer_size + 1;
    
    for (seq_str_i=0;seq_str_i<total_kmers;seq_str_i++)
    {
        total_subseqs = calc_total_subseqs(sequence_hashmask,ambiguous_map,seq_str_i,kmer_size);
        deambiguate_hashmask(kmer_hashmask_array, sequence_hashmask, ambiguous_map, total_subseqs, seq_str_i, kmer_size);
        hashmerize_hashmask_kmer(hash_array, kmer_hashmask_array, total_subseqs, kmer_size);
        append_hash_to_array(ref_hash_pack_array, ref_hash_count, hash_array, seq_str_i, total_subseqs);
    }
    return;
}

MAXKMERS_INT calc_total_theoretical_kmers(int *kmer_sizes, int kmer_size_total)
{
    int kmer_size_i;
    MAXKMERS_INT max_kmers = 0;
    for (kmer_size_i=0;kmer_size_i<kmer_size_total;kmer_size_i++)
    {
        max_kmers += upow(4,kmer_sizes[kmer_size_i]);
    }
    return max_kmers;
}


PMAF_CEXT_ERROR make_primer_element_from_record_element(STRUCT_PRM_RECORD_ELEM **primer_element, STRUCT_SEQ_RECORD_ELEM *record_element)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    STRUCT_MAP_ELEM *ambiguous_map;
    HASHMASK_WORD *sequence_hashmask;
    HASHBASE_BYTE **primer_hashmask_array_buffer;
    HASH_INT *hash_array_buffer;
    MAXKMERS_INT total_subseqs, total_subseqs_i;

    err_code = make_ambiguous_map(&ambiguous_map , record_element->seq_str,record_element->seq_len,record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); return err_code;}
    err_code = make_sequence_hashmask(&sequence_hashmask, record_element->seq_str, ambiguous_map, record_element->seq_len, record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); free(sequence_hashmask); return err_code;}
    
    total_subseqs = calc_total_subseqs(sequence_hashmask,ambiguous_map,0,record_element->seq_len);

    primer_hashmask_array_buffer = (HASHBASE_BYTE **)calloc(total_subseqs,sizeof(HASHBASE_BYTE *));
    if (primer_hashmask_array_buffer == NULL) { return ERR_MEMALC_DEAMBIG; }
    hash_array_buffer = (HASH_INT *)calloc(total_subseqs,sizeof(HASH_INT));
    if (hash_array_buffer == NULL) { return ERR_MEMALC_HASHMERIZE; }
    for (total_subseqs_i = 0; total_subseqs_i<total_subseqs; total_subseqs_i++)
    {
        primer_hashmask_array_buffer[total_subseqs_i] = (HASHBASE_BYTE *)malloc(record_element->seq_len*sizeof(HASHBASE_BYTE *));
        if (primer_hashmask_array_buffer[total_subseqs_i] == NULL) { return ERR_MEMALC_DEAMBIG; }
    }

    deambiguate_hashmask(primer_hashmask_array_buffer, sequence_hashmask, ambiguous_map, total_subseqs, 0, record_element->seq_len);
    hashmerize_hashmask_kmer(hash_array_buffer, primer_hashmask_array_buffer, total_subseqs, record_element->seq_len);

    *primer_element = (STRUCT_PRM_RECORD_ELEM *)malloc(sizeof(STRUCT_PRM_RECORD_ELEM));
    if (*primer_element == NULL) { free(primer_element); free(ambiguous_map); free(sequence_hashmask); free(primer_hashmask_array_buffer); free(hash_array_buffer); return ERR_MEMALC_PRIMER_ELEMENT; }

    (*primer_element)->primer_len = record_element->seq_len;
    (*primer_element)->primer_hash_array = hash_array_buffer;
    (*primer_element)->primer_hash_total = total_subseqs;
    (*primer_element)->primer_id = record_element->seq_id;

    free(ambiguous_map);
    free(sequence_hashmask);
    for (total_subseqs_i = 0; total_subseqs_i<total_subseqs;total_subseqs_i++)
    {
        free(primer_hashmask_array_buffer[total_subseqs_i]);
    }
    free(primer_hashmask_array_buffer);

    return err_code;
}


MAXKMERS_INT count_primers_in_hash_array(STRUCT_PRM_RECORD_ELEM *primer_element, HASH_INT *kmer_hash_array, MAXKMERS_INT total_hash)
{
    MAXKMERS_INT primer_match_counter, total_kmer_hash_i, total_primer_hash_i;

    primer_match_counter = 0;
    for (total_kmer_hash_i = 0; total_kmer_hash_i < total_hash; total_kmer_hash_i++)
    {
        for (total_primer_hash_i = 0; total_primer_hash_i < (primer_element->primer_hash_total); total_primer_hash_i++)
        {
            if ((kmer_hash_array[total_kmer_hash_i]) == (primer_element->primer_hash_array[total_primer_hash_i]))
            {
                primer_match_counter++;
            }
        }
    }
    return primer_match_counter;
}

PMAF_CEXT_ERROR run_primer_testing(STRUCT_SEQ_PRM_STATE_ELEM **record_primer_state, STRUCT_PRM_RECORD_ELEM **primer_element_array, STRUCT_SEQ_RECORD_ELEM *record_element, int total_primers)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    STRUCT_MAP_ELEM *ambiguous_map;
    HASHMASK_WORD *sequence_hashmask;
    MAXKMERS_INT total_subseqs, total_matched_primer;
    MAXKMERS_INT primer_max_allowed_subseqs;
    int total_kmers, seq_str_i, total_primer_i, primer_length, first_primer_pos_buffer, max_primer_size;

    HASHBASE_BYTE **kmer_hashmask_array_buffer;
    HASH_INT *hash_array_buffer;
    MAXKMERS_INT max_total_subseqs, max_total_i;
 
    err_code = make_ambiguous_map(&ambiguous_map , record_element->seq_str,record_element->seq_len,record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); return err_code;}
    err_code = make_sequence_hashmask(&sequence_hashmask, record_element->seq_str, ambiguous_map, record_element->seq_len, record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); free(sequence_hashmask); return err_code;}

    max_total_subseqs = 1;
    max_primer_size = 0;
    for (total_primer_i = 0;total_primer_i < total_primers; total_primer_i++)
    {
        primer_length = primer_element_array[total_primer_i]->primer_len;

        if (max_primer_size < primer_length)
        {
            max_primer_size = primer_length;
        }
        
        if (primer_length >= 16)
        { 
            primer_max_allowed_subseqs = upow(4,(primer_length/2));
        }
        else
        { 
            primer_max_allowed_subseqs = upow(4,primer_length);
        }

        total_kmers = record_element->seq_len - primer_length + 1;
        for (seq_str_i=0;seq_str_i<total_kmers;seq_str_i++)
        {
            total_subseqs = calc_total_subseqs(sequence_hashmask,ambiguous_map,seq_str_i,primer_length);
            if ((max_total_subseqs<total_subseqs) & (total_subseqs<primer_max_allowed_subseqs))
            {
                max_total_subseqs = total_subseqs;
            }
        }
    }

    err_code = allocate_memory_buffer(&kmer_hashmask_array_buffer,&hash_array_buffer,max_total_subseqs,max_primer_size);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); free(sequence_hashmask); return err_code;}

    *record_primer_state = (STRUCT_SEQ_PRM_STATE_ELEM *)malloc(sizeof(STRUCT_SEQ_PRM_STATE_ELEM));
    if (*record_primer_state == NULL) { free(ambiguous_map); free(sequence_hashmask); free(kmer_hashmask_array_buffer); free(hash_array_buffer); return ERR_MEMALC_PRIMER_STATE_ELEMENT;}
    (*record_primer_state)->primer_state_array = (STRUCT_PRM_STATE_ELEM *)malloc(total_primers*sizeof(STRUCT_PRM_STATE_ELEM));
    if ((*record_primer_state)->primer_state_array == NULL) { free(ambiguous_map); free(sequence_hashmask); free(kmer_hashmask_array_buffer); free(hash_array_buffer); return ERR_MEMALC_PRIMER_STATE_ELEMENT;}

    (*record_primer_state)->seq_id = record_element->seq_id;

    for (total_primer_i = 0; total_primer_i < total_primers; total_primer_i++)
    {
        total_matched_primer = 0;
        first_primer_pos_buffer = -1;
        primer_length = primer_element_array[total_primer_i]->primer_len;
        total_kmers = record_element->seq_len - primer_length + 1;
        // Following condition prevents hasmerizaion of long repetitive N bases.
        if (primer_length >= 16)
        { 
            primer_max_allowed_subseqs = upow(4,(primer_length/2)); 
        }
        else
        {
            primer_max_allowed_subseqs = upow(4,primer_length); 
        }
        for (seq_str_i=0;seq_str_i<total_kmers;seq_str_i++)
        {
            total_subseqs = calc_total_subseqs(sequence_hashmask,ambiguous_map,seq_str_i,primer_length);
            if (total_subseqs<primer_max_allowed_subseqs)
            {
                deambiguate_hashmask(kmer_hashmask_array_buffer, sequence_hashmask, ambiguous_map, total_subseqs, seq_str_i, primer_length);
                hashmerize_hashmask_kmer(hash_array_buffer, kmer_hashmask_array_buffer, total_subseqs, primer_length);
                total_matched_primer += count_primers_in_hash_array(primer_element_array[total_primer_i],hash_array_buffer,total_subseqs);
                // If first primer is matched then record the position and break the lookup.
                if ((total_matched_primer > 0) && (first_primer_pos_buffer < 0))
                {
                    first_primer_pos_buffer = seq_str_i;
                    break;
                }
            }
        }
        (*record_primer_state)->primer_state_array[total_primer_i].primer_id = primer_element_array[total_primer_i]->primer_id;
        (*record_primer_state)->primer_state_array[total_primer_i].primer_state = total_matched_primer;
        (*record_primer_state)->primer_state_array[total_primer_i].primer_first_pos = (first_primer_pos_buffer < 0) ? (0) : (unsigned long)first_primer_pos_buffer;
    }

    free(ambiguous_map);
    free(sequence_hashmask);
    for (max_total_i = 0; max_total_i<max_total_subseqs;max_total_i++)
    {
        free(kmer_hashmask_array_buffer[max_total_i]);
    }
    free(kmer_hashmask_array_buffer);
    free(hash_array_buffer);

    return err_code;
}

PMAF_CEXT_ERROR parse_record_element(STRUCT_SEQ_HMER_ELEM **parsed_record, STRUCT_SEQ_RECORD_ELEM *record_element, int *kmer_sizes, int kmer_size_total)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    STRUCT_MAP_ELEM *ambiguous_map;
    HASHMASK_WORD *sequence_hashmask;
    STRUCT_HMER_PACK_ELEM *ref_hash_pack_array;
    HASHBASE_BYTE **kmer_hashmask_array_buffer;
    HASH_INT *hash_array_buffer;
    MAXKMERS_INT max_total_subseqs, max_total_kmers, max_total_i, ref_hash_count = 0;
    int kmer_size_i, max_kmer_size;
    max_total_kmers = calc_total_theoretical_kmers(kmer_sizes,kmer_size_total);
    ref_hash_pack_array = (STRUCT_HMER_PACK_ELEM *)malloc(max_total_kmers*sizeof(STRUCT_HMER_PACK_ELEM));
    if (ref_hash_pack_array == NULL) { return ERR_MEMALC_PARSER_TOTAL;}
    err_code = make_ambiguous_map(&ambiguous_map , record_element->seq_str,record_element->seq_len,record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); return err_code;}
    err_code = make_sequence_hashmask(&sequence_hashmask, record_element->seq_str, ambiguous_map, record_element->seq_len, record_element->seq_tab);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); free(sequence_hashmask); return err_code;}

    calc_memory_buffer_limits(&max_total_subseqs, &max_kmer_size,sequence_hashmask, ambiguous_map, record_element->seq_len, kmer_sizes, kmer_size_total);
    err_code = allocate_memory_buffer(&kmer_hashmask_array_buffer,&hash_array_buffer,max_total_subseqs,max_kmer_size);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map); free(sequence_hashmask); return err_code;}
    for (kmer_size_i = 0;kmer_size_i< kmer_size_total;kmer_size_i++)
    {
        kmerize_hashmask_sequence_for_ksize(kmer_hashmask_array_buffer,hash_array_buffer, ref_hash_pack_array, &ref_hash_count, sequence_hashmask, ambiguous_map, record_element->seq_len, kmer_sizes[kmer_size_i]);
    }
    free(ambiguous_map);
    free(sequence_hashmask);
    for (max_total_i = 0; max_total_i<max_total_subseqs;max_total_i++)
    {
        free(kmer_hashmask_array_buffer[max_total_i]);
    }
    free(kmer_hashmask_array_buffer);
    free(hash_array_buffer);
    *parsed_record = (STRUCT_SEQ_HMER_ELEM *)malloc(sizeof(STRUCT_SEQ_HMER_ELEM));
    if (*parsed_record == NULL) { return ERR_MEMALC_PARSER_HMER_ELEMENT; }
    (*parsed_record)->seq_id = record_element->seq_id;
    (*parsed_record)->hmer_pack_array = (STRUCT_HMER_PACK_ELEM *)realloc(ref_hash_pack_array,ref_hash_count*sizeof(STRUCT_HMER_PACK_ELEM));
    (*parsed_record)->hmer_total = ref_hash_count;
    return err_code;
}

PMAF_CEXT_ERROR parse_record_element_chunk(STRUCT_SEQ_HMER_ELEM ***parsed_record_chunk, STRUCT_SEQ_RECORD_ELEM **record_element_chunk, int *kmer_sizes, int kmer_size_total, int chunksize)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    STRUCT_MAP_ELEM **ambiguous_map_array;
    HASHMASK_WORD **sequence_hashmask_array;
    STRUCT_HMER_PACK_ELEM *ref_hash_pack_array;
    HASHBASE_BYTE **kmer_hashmask_array_buffer;
    HASH_INT *hash_array_buffer;
    MAXKMERS_INT max_total_subseqs,max_total_kmers, max_total_i, ref_hash_i, ref_hash_count, max_total_subseqs_chunk = 0;
    int chunksize_i, kmer_size_i, max_kmer_size;

    max_total_kmers = calc_total_theoretical_kmers(kmer_sizes,kmer_size_total);
    ref_hash_pack_array = (STRUCT_HMER_PACK_ELEM *)malloc(max_total_kmers*sizeof(STRUCT_HMER_PACK_ELEM));
    if (ref_hash_pack_array == NULL) { return ERR_MEMALC_PARSER_TOTAL;}

    ambiguous_map_array = (STRUCT_MAP_ELEM **)malloc(chunksize*sizeof(STRUCT_MAP_ELEM *));
    if (ambiguous_map_array == NULL) { return ERR_MEMALC_PARSER_AMBIGUOUS_CHUNK; }
    sequence_hashmask_array = (HASHMASK_WORD **)malloc(chunksize*sizeof(HASHMASK_WORD *));
    if (sequence_hashmask_array == NULL) { return ERR_MEMALC_PARSER_HASHMASK_CHUNK;}
    *parsed_record_chunk = (STRUCT_SEQ_HMER_ELEM **)malloc(chunksize*sizeof(STRUCT_SEQ_HMER_ELEM *));
    if (*parsed_record_chunk == NULL) { return ERR_MEMALC_PARSER_HMER_CHUNK;}

    for (chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        err_code = make_ambiguous_map(&ambiguous_map_array[chunksize_i] , record_element_chunk[chunksize_i]->seq_str,record_element_chunk[chunksize_i]->seq_len,record_element_chunk[chunksize_i]->seq_tab);
        if (err_code != ERR_NO_ERROR) { free(ambiguous_map_array[chunksize_i]); return err_code;}
        err_code = make_sequence_hashmask(&sequence_hashmask_array[chunksize_i], record_element_chunk[chunksize_i]->seq_str, ambiguous_map_array[chunksize_i], record_element_chunk[chunksize_i]->seq_len, record_element_chunk[chunksize_i]->seq_tab);
        if (err_code != ERR_NO_ERROR) { free(ambiguous_map_array[chunksize_i]); free(sequence_hashmask_array[chunksize_i]); return err_code;}
        calc_memory_buffer_limits(&max_total_subseqs, &max_kmer_size,sequence_hashmask_array[chunksize_i], ambiguous_map_array[chunksize_i], record_element_chunk[chunksize_i]->seq_len, kmer_sizes, kmer_size_total);
        if (max_total_subseqs_chunk<max_total_subseqs)
        {
            max_total_subseqs_chunk = max_total_subseqs;
        }
        (*parsed_record_chunk)[chunksize_i] = (STRUCT_SEQ_HMER_ELEM *)malloc(sizeof(STRUCT_SEQ_HMER_ELEM));
        if (*parsed_record_chunk == NULL) { free(ambiguous_map_array[chunksize_i]); free(sequence_hashmask_array[chunksize_i]); return ERR_MEMALC_PARSER_HMER_CHUNK_ELEM;}
    }
   
    err_code = allocate_memory_buffer(&kmer_hashmask_array_buffer,&hash_array_buffer,max_total_subseqs_chunk,max_kmer_size);
    if (err_code != ERR_NO_ERROR) { free(ambiguous_map_array); free(sequence_hashmask_array); return err_code;}
    for (chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        ref_hash_count = 0;
        for (kmer_size_i = 0;kmer_size_i< kmer_size_total;kmer_size_i++)
        {
            kmerize_hashmask_sequence_for_ksize(kmer_hashmask_array_buffer, hash_array_buffer, ref_hash_pack_array, &ref_hash_count, sequence_hashmask_array[chunksize_i], ambiguous_map_array[chunksize_i], record_element_chunk[chunksize_i]->seq_len, kmer_sizes[kmer_size_i]);
        }
        (*parsed_record_chunk)[chunksize_i]->seq_id = record_element_chunk[chunksize_i]->seq_id;
        (*parsed_record_chunk)[chunksize_i]->hmer_pack_array = (STRUCT_HMER_PACK_ELEM *)malloc(ref_hash_count*sizeof(STRUCT_HMER_PACK_ELEM));
        for (ref_hash_i=0; ref_hash_i < ref_hash_count; ref_hash_i++)
        {
            (*parsed_record_chunk)[chunksize_i]->hmer_pack_array[ref_hash_i] = ref_hash_pack_array[ref_hash_i];
        }
        (*parsed_record_chunk)[chunksize_i]->hmer_total = ref_hash_count;
    }

    for (chunksize_i = 0; chunksize_i < chunksize; chunksize_i++)
    {
        free(ambiguous_map_array[chunksize_i]);
        free(sequence_hashmask_array[chunksize_i]);
    }
    for (max_total_i = 0; max_total_i<max_total_subseqs_chunk;max_total_i++)
    {
        free(kmer_hashmask_array_buffer[max_total_i]);
    }
    free(kmer_hashmask_array_buffer);
    free(hash_array_buffer);
    free(ambiguous_map_array);
    free(sequence_hashmask_array);
    return err_code;

}


PMAF_CEXT_ERROR parse_theoretical_record_elements(HASH_INT **parsed_hash_array, char **kmer_array, int kmer_size, MAXKMERS_INT chunksize)
{
    PMAF_CEXT_ERROR err_code = ERR_NO_ERROR;
    MAXKMERS_INT seq_i;
    int seq_str_i;
    HASHBASE_BYTE hashbase_buffer;
    HASHBASE_BYTE *hashmask_kmer_buffer;
    HASH_INT hash_buffer, ref_hash_buffer;
    hashmask_kmer_buffer = (HASHBASE_BYTE *)malloc(kmer_size*sizeof(HASHBASE_BYTE));
    if (hashmask_kmer_buffer == NULL) { return ERR_MEMALC_THEORETICAL_PARSER;}
    *parsed_hash_array = (HASH_INT *)calloc(chunksize, sizeof(HASH_INT));
    if (*parsed_hash_array == NULL) { return ERR_MEMALC_THEORETICAL_PARSER;}
    for (seq_i = 0; seq_i < chunksize; seq_i++)
    {
        for (seq_str_i = 0; seq_str_i < kmer_size; seq_str_i++)
        {
            hashbase_buffer = (HASHBASE_BYTE)kmer_array[seq_i][seq_str_i];
            hashbase_buffer = (hashbase_buffer >> 1) & 3;
            hashmask_kmer_buffer[seq_str_i] = hashbase_buffer;
        }

        ref_hash_buffer = 0;
        for (seq_str_i=0; seq_str_i<kmer_size; seq_str_i++)
        {
            hash_buffer = (HASH_INT)hashmask_kmer_buffer[seq_str_i];
            ref_hash_buffer = ref_hash_buffer << 2;
            ref_hash_buffer = ref_hash_buffer | hash_buffer;
        }
        ref_hash_buffer = ref_hash_buffer + (HASH_INT)upow(2,2*kmer_size);
        (*parsed_hash_array)[seq_i] = ref_hash_buffer;
    }
    free(hashmask_kmer_buffer);
    return err_code;
}


