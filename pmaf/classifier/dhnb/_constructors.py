from pmaf.internal._constants import IUPAC_NON_AMBIGUOUS_BASES
from pmaf.internal._shared import chunk_generator
from pmaf.internal._extensions._cpython import cext
from itertools import product as itrt_product
import numpy as np

def generate_theoretical_hmers(kmer_sizes,chunksize):
    # this function generate theoretical hmers but from the simple kmer list
    # this function is very rapid but the hmers always are same so this can be changed to simple python function that generates hmer numbers later
    hash_set = set()
    for kmer_size in kmer_sizes:
        ksize_kmers_records = [(''.join(p),) for p in itrt_product(IUPAC_NON_AMBIGUOUS_BASES, repeat=kmer_size)]
        for kmer_record_chunk in chunk_generator(ksize_kmers_records, chunksize):
            tmp_hash_set = cext.PMAFCEXT.parse_theoretical_kmers_chunk(iter(kmer_record_chunk), kmer_size, len(kmer_record_chunk))
            for tmp_hash in tmp_hash_set:
                hash_set.add(tmp_hash)
    return hash_set

def db_chunk_record_generator(rid_list, exec_chunksize, database_instance, digest_pbar):
    # this function retrieves sequence records from local HDF5 in chunks with size `exec_chunksize`
    # max len of `rid_list` is run_chunksize but it yields in batchs bases on `io_chunksize` this is controlled by joblib
    io_chunk_record_generator = database_instance.get_sequence_by_rid(rid_list, iterator=True, like='tuples', chunksize = exec_chunksize)
    for exec_chunk_rids, chunk_record_tuples in io_chunk_record_generator:
        chunk_records_length = len(exec_chunk_rids) # total rids in chunk ideally `exec_chunksize` but can be less since records exhaust
        digest_pbar.next(chunk_records_length) # This function is thread based (it should be but does not really matter) so progress bar can be updated
        yield exec_chunk_rids, chunk_record_tuples #yield (rid_list_in_chunk, chunk_records)

def chunk_record_generator(chunk_records_tuples, io_chunksize, digest_pbar):
    # this does the same as `db_chunk_record_generator` but used only for datasets with pre-made list of records.
    io_chunk_record_generator = chunk_generator(chunk_records_tuples, io_chunksize)
    for chunk_record_tuples in io_chunk_record_generator:
        chunk_records_length = len(chunk_record_tuples)
        digest_pbar.next(chunk_records_length)
        yield chunk_records_length, chunk_record_tuples

def parse_refine_primer_chunk(ordered_chunk_rids, ordered_primer_ids, exec_chunk_records,  primer_records_tuple):
    # this is similar to `parse_process_chunk` but much faster since it only deambiguates sequences and identifies primers with their positions
    # this function yield simple results and parsed in simpler manner. Although C side looks much more mess!
    chunk_result_tuples_list = []
    if len(ordered_chunk_rids)>0:
        chunk_parsed = cext.PMAFCEXT.parse_match_primers_for_record_chunk(iter(exec_chunk_records),primer_records_tuple,len(exec_chunk_records))
        for rid in ordered_chunk_rids:
            chunk_result_tuples_list.append([value for primer_id in ordered_primer_ids for value in chunk_parsed[rid][primer_id]])
    return np.asarray(chunk_result_tuples_list,dtype='u4')

def parse_process_chunk(ordered_chunk_rids, chunk_records_tuples, kmer_sizes):
    result_fixed_list = [] # reference array to store results
    if len(ordered_chunk_rids)>0: # if no records are passed skip parsing. This should not happen ideally but just in case
        chunk_parsed = cext.PMAFCEXT.parse_record_chunk(iter(chunk_records_tuples), kmer_sizes, len(ordered_chunk_rids)) # pass record tuples to C extension parser (kmerizer/hmerizer/pos-identification)
        max_hmer_pack_len = max([len(rid_pack) for rid_pack in chunk_parsed.values()])+1 # get max number of hmers and add 1 to ensure that 0 present later during transforms
        for rid in ordered_chunk_rids: # keep the order of the chunk_rids
            rid_pack = chunk_parsed[rid]  # `parse_record_chunk` returns dict as product so just get the corresponding element from that dict
            hmer_diff = (max_hmer_pack_len-len(rid_pack)) # find difference in hmers
            tmp_result = [(hmer_row[0],(hmer_row[1:])) for hmer_row in rid_pack] + hmer_diff*[(0,(0,0))] #make list of tuples (hmer,fp,lp) and add (0,0,0) times difference
            tmp_result.sort(key=lambda hmer_row:hmer_row[0]) # sort by hmers, this is important to ensure correct and rapid transformation later
            result_fixed_list.append(tmp_result)
    return np.array(result_fixed_list,dtype=[('hmer','u8'),('pos','u2',2)]) # make valid adjusted for missing hmers and sorted structural numpy array that can be saved as numpy memmap

def verify_kmer_sizes(kmer_sizes):
    # This supposed to be kmer verifier but actual verification is done via `cext.verify_kmer_sizes`.
    # However if ksize is greater than 15 or say 16. Then mim size of hmer require 32 bits and
    # I have yet no idea why but at C side memalloc cannot allocate memory more than that eventhough CPU is 64 bits and C extension was compiled accordingly.
    # Simply f*** it for now, so lets say limit for now is max 15
    ret = False
    hmerize_size_limits = cext.PMAFCEXT.get_size_info()
    if cext.verify_kmer_sizes(kmer_sizes,*hmerize_size_limits) == 0:
        ret = True
        for ksize in kmer_sizes:
            if ksize>15:
                ret = False
                break
    return ret

def transform_hmer_matrix(block_hmer_vector, block_hmer_matrix):
    # this transforms makes `raw` sub-blocks from single shelve
    # block_hmer_vector - shape = (ref_hmer_count, 1)
    # block_hmer_matrix - shape = (block_rid_N, max_hmers from `parse_process_chunk`)
    hmer_idx = np.searchsorted(block_hmer_vector, block_hmer_matrix) # make hmer index matrix with shape of block_hmer_matrix and respective indices in block_hmer_matrix
    hmer_idx[hmer_idx==len(block_hmer_vector)] = 0 # get rid of all hmers that are greater than possible hmers in block_hmer_vector
    block_hmer_vector_ix = block_hmer_vector.argsort() # make index vector for block_hmer_vector. same as range(ref_hmer_count) because block_hmer_vector is sorted
    block_hmer_mask = np.zeros((block_hmer_matrix.shape[0],len(block_hmer_vector)),dtype='b') # make buffer zeros for mask matrix of shape = (block_rid_N, ref_hmer_count)
    hmer_idx_adj = block_hmer_vector_ix[hmer_idx] # transform 1d array block_hmer_vector_ix to 2d array of shape same as hmer_idx
    np.put_along_axis(block_hmer_mask, hmer_idx_adj, block_hmer_vector[hmer_idx_adj] == block_hmer_matrix, axis=1) # along rid axis put all True/False values from `values` to buffer matrix at positions given with hmer_idx_adj
    return block_hmer_mask[:,1:] # remove first hmer element since it is always zero and is used to preserve order and get rid of missing values adjusted in `parse_process_chunk`

def transform_pos_matrix(block_hmer_vector, parsed_result_matrix):
    # this transforms makes `hmeta` sub-blocks from single shelve
    # block_hmer_vector - shape = (ref_hmer_count, 1)
    #parsed_result_matrix - shape = (block_rid_N, max_hmers from `parse_process_chunk`, (+2)). this is the original structured array from `parsed_result_matrix`
    hmer_idx = np.searchsorted(block_hmer_vector, parsed_result_matrix['hmer']) # make hmer index matrix with shape of block_hmer_matrix and respective indices in block_hmer_matrix
    hmer_idx[hmer_idx==len(block_hmer_vector)] = 0 # get rid of all hmers that are greater than possible hmers in block_hmer_vector
    block_hmer_vector_ix = block_hmer_vector.argsort() # make index vector for block_hmer_vector. same as range(ref_hmer_count) because block_hmer_vector is sorted
    hmer_idx_adj = np.where(block_hmer_vector[hmer_idx]==parsed_result_matrix['hmer'],block_hmer_vector_ix[hmer_idx],0) # make an array 2d index array of same size as hmer_idx and containing corresponding index positions of block_hmer_vector_ix of only hmers that present in parsed_result_matrix['hmer']
    hmer_idx_pos_adj = np.repeat(hmer_idx_adj[:, :, np.newaxis], 2, axis=2) # transform 2d array hmer_idx_adj into 3d array with third dimension ['fp','lp'] of same values (because order in original matrix are same for both)
    block_pos_matrix = np.zeros((parsed_result_matrix.shape[0],len(block_hmer_vector),2),dtype='u2') # create buffer 3d array of size (block_rid_N, ref_hmer_count, 2)
    np.put_along_axis(block_pos_matrix, hmer_idx_pos_adj, parsed_result_matrix['pos'], axis=1) # along rid axis put all ('fp','lp') values from `values` to buffer 3d array at positions given with 3d index array hmer_idx_adj
    return block_pos_matrix[:,1:,:] # remove first hmer element since it is always zero and is used to preserve order and get rid of missing values adjusted in `parse_process_chunk`

def raw_transform_shelve_to_block(block_cache_map,block_info=None):
    # this transform is makes `raw` blocks from list of shelves
    # `block_info` contain all the information about where currently map_blocks is working
    raw_matrix = np.empty(block_info[None]['chunk-shape'],dtype=block_info[None]['dtype']) # create buffer array to store all sub-transforms
    block_hmer_vector = np.insert(block_cache_map[block_info[None]['chunk-location']][0],0,0) # insert 0 at reference hmer array to ensure that all missing values from shelves are mapped there
    parsed_chunk_shelves = block_cache_map[block_info[None]['chunk-location']][1] # get all the parsed shelves in form of numpy memmaps
    rid_i = 0 # rid counter
    for parsed_chunk_shelve in parsed_chunk_shelves: # iter over shelves
        block_hmer_matrix = parsed_chunk_shelve.get()['hmer'] # load the parsed shelve to RAM/lazy by numpy and only select 'hmer' array from original structural ndarray
        parsed_chunk_len = block_hmer_matrix.shape[0] # total number of rids in shelve
        raw_matrix[rid_i:rid_i + parsed_chunk_len, :] = transform_hmer_matrix(block_hmer_vector,block_hmer_matrix) # transform shelve into valid mask matrix and set to the corresponding position in the buffer
        rid_i = rid_i + parsed_chunk_len # add total parsed rid to rid counter
    return raw_matrix # return the completed block so that dask can pass it to xarray so that it can store it as single I/O chunk in the storage

def hmeta_transform_shelve_to_block(block_cache_map,block_info=None):
    # this transform is makes `hmeta` blocks from list of shelves
    # `block_info` contain all the information about where currently map_blocks is working
    hmeta_matrix = np.empty(block_info[None]['chunk-shape'], dtype=block_info[None]['dtype']) # create buffer array to store all sub-transforms
    block_hmer_vector = np.insert(block_cache_map[block_info[None]['chunk-location']][0],0,0)# insert 0 at reference hmer array to ensure that all missing values from shelves are mapped there
    parsed_chunk_shelves = block_cache_map[block_info[None]['chunk-location']][1]# get all the parsed shelves in form of numpy memmaps
    rid_i = 0 # rid counter
    for parsed_chunk_shelve in parsed_chunk_shelves: # iter over shelves
        parsed_result_matrix = parsed_chunk_shelve.get()# load the parsed shelve to RAM/lazy by numpy
        parsed_chunk_len = parsed_result_matrix.shape[0]# total number of rids in shelve
        hmeta_matrix[rid_i:rid_i + parsed_chunk_len, :, :] = transform_pos_matrix(block_hmer_vector,parsed_result_matrix) # transform shelve into valid 3d pos array and set to the corresponding position in the buffer
        rid_i = rid_i + parsed_chunk_len # add total parsed rid to rid counter
    return hmeta_matrix# return the completed block so that dask can pass it to xarray so that it can store it as single I/O chunk in the storage