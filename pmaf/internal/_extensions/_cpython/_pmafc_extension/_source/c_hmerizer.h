#include <stddef.h>
typedef unsigned long long int HASH_INT;
typedef size_t MAXKMERS_INT;
typedef unsigned short HASHMASK_WORD;
typedef unsigned char HASHBASE_BYTE;

typedef enum _PMAF_CEXT_ERROR PMAF_CEXT_ERROR;
typedef struct _STRUCT_MAP_ELEM STRUCT_MAP_ELEM;
typedef struct _STRUCT_SEQ_RECORD_ELEM STRUCT_SEQ_RECORD_ELEM;
typedef struct _STRUCT_SEQ_HMER_ELEM STRUCT_SEQ_HMER_ELEM;
typedef struct _STRUCT_HMER_PACK_ELEM STRUCT_HMER_PACK_ELEM;
typedef struct _STRUCT_PRM_RECORD_ELEM STRUCT_PRM_RECORD_ELEM;
typedef struct _STRUCT_PRM_STATE_ELEM STRUCT_PRM_STATE_ELEM;
typedef struct _STRUCT_SEQ_PRM_STATE_ELEM STRUCT_SEQ_PRM_STATE_ELEM;


enum _PMAF_CEXT_ERROR{
    ERR_NO_ERROR,
    ERR_MEMALC_RECORD_ELEMENT,
    ERR_MEMALC_AMBIGUOUS_MAP,
    ERR_MEMALC_HASHMASK,
    ERR_MEMALC_DEAMBIG,
    ERR_MEMALC_HASHMERIZE,
    ERR_MEMALC_PARSER_TOTAL,
    ERR_MEMALC_PARSER_HMER_ELEMENT,
    ERR_MEMALC_THEORETICAL_PARSER,
    ERR_PY_TOTAL_KMERS_EXCEED,
    ERR_PY_SOME_KMER_EXCEED,
    ERR_MEMALC_PRIMER_ELEMENT,
    ERR_MEMALC_PRIMER_STATE_ELEMENT,
    ERR_MEMALC_PARSER_AMBIGUOUS_CHUNK,
    ERR_MEMALC_PARSER_HASHMASK_CHUNK,
    ERR_MEMALC_PARSER_HMER_CHUNK,
    ERR_MEMALC_PARSER_HMER_CHUNK_ELEM
};

struct _STRUCT_MAP_ELEM{
    int pos;
    int total;
    HASHMASK_WORD branch;
};

struct _STRUCT_SEQ_RECORD_ELEM{
    unsigned long seq_id;
    char *seq_str;
    int seq_len;
    int seq_tab;
};

struct _STRUCT_PRM_RECORD_ELEM{
    unsigned long primer_id;
    int primer_len;
    MAXKMERS_INT primer_hash_total;
    HASH_INT *primer_hash_array;
};

struct _STRUCT_PRM_STATE_ELEM{
    unsigned long primer_id;
    unsigned long primer_first_pos;
    MAXKMERS_INT primer_state;
};

struct _STRUCT_SEQ_PRM_STATE_ELEM{
    unsigned long seq_id;
    STRUCT_PRM_STATE_ELEM *primer_state_array;
};

struct _STRUCT_HMER_PACK_ELEM{
    HASH_INT hmer;
    unsigned long first_pos;
    unsigned long last_pos;
};

struct _STRUCT_SEQ_HMER_ELEM{
    unsigned long seq_id;
    MAXKMERS_INT hmer_total;
    STRUCT_HMER_PACK_ELEM *hmer_pack_array;
};

MAXKMERS_INT upow(int base, int power);

PMAF_CEXT_ERROR make_record_element(STRUCT_SEQ_RECORD_ELEM **record_element, unsigned long seq_id, char* seq_str, int seq_len, int seq_tab);

HASHMASK_WORD hashmask_ambiguous_base(const char *ambiguous_branch,int total_base);

PMAF_CEXT_ERROR make_ambiguous_map(STRUCT_MAP_ELEM **ambiguous_map_start,char *seq_str,int seq_len,int seq_tab);

PMAF_CEXT_ERROR make_sequence_hashmask(HASHMASK_WORD **sequence_hashmask, char *seq_str, STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int seq_tab);

MAXKMERS_INT calc_total_subseqs(HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, int seq_offset, int seq_stop);

void calc_memory_buffer_limits(MAXKMERS_INT *max_total_subseqs, int *max_kmer_size, HASHMASK_WORD *sequence_hashmask,STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int *kmer_sizes, int kmer_size_total);

PMAF_CEXT_ERROR allocate_memory_buffer(HASHBASE_BYTE ***kmer_hashmask_array, HASH_INT **hash_array, MAXKMERS_INT max_total_subseqs,int max_kmer_size);

void deambiguate_hashmask(HASHBASE_BYTE **kmer_hashmask_array, HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, MAXKMERS_INT total_subseqs, int seq_offset, int kmer_size);

void hashmerize_hashmask_kmer(HASH_INT *hash_array, HASHBASE_BYTE **kmer_hashmask_array, MAXKMERS_INT total_subseqs, int kmer_size);

void append_hash_to_array(STRUCT_HMER_PACK_ELEM *ref_hash_pack_array, MAXKMERS_INT  *ref_hash_count, HASH_INT *hash_array, unsigned long hmer_pos, MAXKMERS_INT hash_count);

void kmerize_hashmask_sequence_for_ksize(HASHBASE_BYTE **kmer_hashmask_array, HASH_INT *hash_array, STRUCT_HMER_PACK_ELEM *ref_hash_pack_array, MAXKMERS_INT *ref_hash_count, HASHMASK_WORD *sequence_hashmask, STRUCT_MAP_ELEM *ambiguous_map, int seq_len, int kmer_size);

MAXKMERS_INT calc_total_theoretical_kmers(int *kmer_sizes, int kmer_size_total);

PMAF_CEXT_ERROR parse_record_element(STRUCT_SEQ_HMER_ELEM **parsed_record, STRUCT_SEQ_RECORD_ELEM *record_element, int *kmer_sizes, int kmer_size_total);

PMAF_CEXT_ERROR parse_record_element_chunk(STRUCT_SEQ_HMER_ELEM ***parsed_record_chunk, STRUCT_SEQ_RECORD_ELEM **record_element_chunk, int *kmer_sizes, int kmer_size_total, int chunksize);

PMAF_CEXT_ERROR parse_theoretical_record_elements(HASH_INT **parsed_hash_array, char **kmer_array, int kmer_size, MAXKMERS_INT total_kmers);

PMAF_CEXT_ERROR make_primer_element_from_record_element(STRUCT_PRM_RECORD_ELEM **primer_element, STRUCT_SEQ_RECORD_ELEM *record_element);

PMAF_CEXT_ERROR run_primer_testing(STRUCT_SEQ_PRM_STATE_ELEM **record_primer_state, STRUCT_PRM_RECORD_ELEM **primer_element_array, STRUCT_SEQ_RECORD_ELEM *record_element, int total_primers);