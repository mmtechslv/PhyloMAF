from ._base import DHNBClassifierBase
from ._metakit import DhnbClassifierDatasetMetabase,DhnbClassifierBaseMetabase
from pmaf.classifier.dhnb._shared import add_primer_prefix
from pmaf.classifier.dhnb._constructors import parse_refine_primer_chunk, generate_theoretical_hmers, parse_process_chunk, verify_kmer_sizes
from pmaf.internal._extensions._cpython._pmafc_extension import make_sequence_record_tuple
from pmaf.internal._shared import chunk_generator
from os import path
import xarray as xr
import numpy as np
import pandas as pd
from math import ceil
from tqdm import tqdm
from netCDF4 import Dataset
from datetime import datetime
from joblib import Memory,Parallel,delayed
from tempfile import mkdtemp
from collections import defaultdict
import warnings
warnings.simplefilter('ignore', category=UserWarning)

class DHNBClassifierDataset(DHNBClassifierBase,DhnbClassifierDatasetMetabase):
    __cache_prefix = 'cdrp_'
    __cache_build_prefix = 'build_cdrp_'
    def __init__(self, dataset_fp, seq_record_df, cache_dir_fp=None, **kwargs):
        max_seq_length = seq_record_df['length'].max()
        super().__init__(dataset_fp, cache_dir_fp, 'dts_kmer_sizes', 'dts_compression', max_seq_length, **kwargs)
        if self.xr.dts_classifier_type != self.MODEL_NAME:
            raise TypeError('Dataset is not compatible with classifier.')
        if not (seq_record_df.index.isin(self.xrid).sum() == seq_record_df.shape[0]):
            raise ValueError('Dataset IDs do not mach Feature IDs. ')
        self._seq_records = seq_record_df
        tmp_indexed_seq_record_df = seq_record_df.loc[self.passed_rids].reset_index()
        self._index_label_map = tmp_indexed_seq_record_df[seq_record_df.index.name]
        self._mapped_seq_record_df = tmp_indexed_seq_record_df.reset_index().set_index(seq_record_df.index.name)


    @classmethod
    def verify_classifier(cls, classifier_instance):
        ret = False
        if isinstance(classifier_instance, DhnbClassifierBaseMetabase) and isinstance(classifier_instance,DHNBClassifierBase):
            if classifier_instance.state:
                ret = True
        return ret

    @classmethod
    def verify_basefile(cls, basefile_fp):
        ret = False
        if isinstance(basefile_fp, str):
            if path.exists(basefile_fp):
                dataset_xr = xr.open_dataset(basefile_fp)
                if (dataset_xr.dts_type == cls.__name__) and (dataset_xr.dts_classifier_type == cls.MODEL_NAME):
                    ret = True
                dataset_xr.close()
        return ret


    def __init_primer_metadata(self, primers_dict):

        self._hold_basefile()
        dataset_storer = Dataset(self.basefile_fp, 'a')

        rmeta = dataset_storer.variables['rmeta']
        mritem_var = dataset_storer.variables['mritem']

        mritem_index_counter = self.xmritem.shape[0]

        for primer_label, primer_seq_str in primers_dict.items():
            if add_primer_prefix(primer_label,'valid') not in self.xmritem:
                mritem_meta_prm_state_index = mritem_index_counter
                mritem_meta_prm_valid_index =  mritem_index_counter + 1
                mritem_meta_prm_first_pos_index = mritem_index_counter + 2

                mritem_var[mritem_meta_prm_state_index] = add_primer_prefix(primer_label,'state')
                mritem_var[mritem_meta_prm_valid_index] = add_primer_prefix(primer_label,'valid')
                mritem_var[mritem_meta_prm_first_pos_index] = add_primer_prefix(primer_label,'first-pos')

                mritem_index_counter = mritem_index_counter + 3
            else:
                mritem_meta_prm_state_index = self.xmritem.get_loc(add_primer_prefix(primer_label, 'state'))
                mritem_meta_prm_valid_index =  self.xmritem.get_loc(add_primer_prefix(primer_label, 'valid'))
                mritem_meta_prm_first_pos_index = self.xmritem.get_loc(add_primer_prefix(primer_label, 'first-pos'))

            rmeta[:, mritem_meta_prm_state_index] = 0
            rmeta[:, mritem_meta_prm_valid_index] = 1
            rmeta[:, mritem_meta_prm_first_pos_index] = 0

        dataset_storer.close()

        self._release_basefile()
        self._reset_inits()
        return

    def _refine_by_primer(self, primers_dict):
        if not isinstance(primers_dict, dict):
            raise TypeError('`primer_dict` must be a dictionary.')
        if self.cache_dir is not None:
            cache_dir_fp = mkdtemp(prefix=self.__cache_prefix, dir=self.cache_dir)
        else:
            cache_dir_fp = None

        tqdm.write("Parsing primers and assigning metadata.")


        self.__init_primer_metadata(primers_dict)

        primer_records_list = []
        mritem_primer_labels = []
        tmp_primer_index_counter = 1
        tmp_primer_index_map = defaultdict(str)

        for primer_label, primer_seq_str in primers_dict.items():
            primer_records_list.append(make_sequence_record_tuple(tmp_primer_index_counter, primer_seq_str))
            mritem_primer_labels.append(add_primer_prefix(primer_label, 'state'))
            mritem_primer_labels.append(add_primer_prefix(primer_label, 'first-pos'))
            tmp_primer_index_map[tmp_primer_index_counter] = primer_label
            tmp_primer_index_counter = tmp_primer_index_counter + 1

        primer_records_tuple = tuple(primer_records_list)

        self._hold_basefile()

        dataset_storer = Dataset(self.basefile_fp, 'a')

        rmeta = dataset_storer.variables['rmeta']

        ft_refine_pbar = tqdm(desc='Parsing/digesting/caching _feature sequences for primers', total=self.passed_rids.shape[0], position=0)
        refiner_memory_cache = Memory(location=cache_dir_fp, verbose=0, compress=ceil(self.compression / 2) if self.compression > 0 else False)

        parse_refine_primer_chunk_cached = refiner_memory_cache.cache(parse_refine_primer_chunk)

        parsed_chunk_result_shelves = []

        for run_chunk_record_tuples in chunk_generator(self.__make_target_sequence_records(self._mapped_seq_record_df,self.passed_rids), self.run_chunksize):
            parsed_chunk_result_shelves.extend(
                Parallel(n_jobs=self.nworkers, prefer='threads', verbose=0)(delayed(parse_refine_primer_chunk_cached.call_and_shelve)
                                                                            (chunk_records_length, chunk_record_tuples, self.exec_chunksize, primer_records_tuple)
                                                                            for chunk_records_length, chunk_record_tuples in
                                                                            chunk_record_generator(run_chunk_record_tuples, self.io_chunksize, ft_refine_pbar)))

        ft_refine_pbar.n = ft_refine_pbar.total
        ft_refine_pbar.refresh()

        db_write_pbar = tqdm(desc='Adding digest into dataset file', total=self.passed_rids.shape[0], position=1)
        rmeta_labels_order = [label for label in self.xmritem.values if label in mritem_primer_labels]
        write_chunk_counter = 0
        rids_chunk = []
        rmeta_chunk = []
        for parsed_chunk_result_shelve in parsed_chunk_result_shelves:
            for rid, primer_state_dict in parsed_chunk_result_shelve.get():
                if write_chunk_counter < self.io_chunksize:
                    rids_chunk.append(rid)
                    rmeta_primer_dict = defaultdict(int)
                    for primer_id, primer_state in primer_state_dict.items():
                        rmeta_primer_dict[add_primer_prefix(tmp_primer_index_map[primer_id], 'state')] = primer_state[0]
                        rmeta_primer_dict[add_primer_prefix(tmp_primer_index_map[primer_id], 'first-pos')] = primer_state[1]
                    rmeta_chunk.append([rmeta_primer_dict[label] for label in rmeta_labels_order])
                    write_chunk_counter = write_chunk_counter + 1
                else:
                    rmeta[self.xrid.isin(self._index_label_map[rids_chunk].values), self.xmritem.isin(rmeta_labels_order)] = np.asarray(rmeta_chunk).astype('u4')
                    rids_chunk = []
                    rmeta_chunk = []
                    db_write_pbar.update(write_chunk_counter)
                    write_chunk_counter = 0

        if write_chunk_counter > 0:
            rmeta[self.xrid.isin(self._index_label_map[rids_chunk].values), self.xmritem.isin(rmeta_labels_order)] = np.asarray(rmeta_chunk).astype('u4')
            db_write_pbar.update(write_chunk_counter)

        refiner_memory_cache.clear(warn=False)
        dataset_storer.close()
        self._release_basefile()
        return

    @classmethod
    def __make_target_sequence_records(cls,mapped_seq_record_df,target_ids):
        target_seq_records = mapped_seq_record_df.loc[target_ids, ['index', 'sequence', 'length', 'tab']].astype({'length': int, 'tab': int})
        return tuple(zip(*zip(*target_seq_records.values)))

    @classmethod
    def build(cls, dataset_fp, seq_record_df, kmer_sizes=(5, 6), cache_dir_fp=None, run_chunksize=10000, io_chunksize=400, exec_chunksize=80, empc_cutoff=40, force_new=False, compress=4, nworkers=8, author='', name='', extra_metadata_dict = {}):

        if not isinstance(seq_record_df,pd.DataFrame):
            raise TypeError('`database_instance` has invalid type.')

        if (path.exists(dataset_fp)) and (not force_new):
            raise FileExistsError('File must not exist. Use `force_new` = True to rewrite.')

        if isinstance(extra_metadata_dict, dict):
            for key,value in extra_metadata_dict.items():
                if not (isinstance(key,str) and isinstance(value,str)):
                    raise TypeError('Dataset attributes must have `str` type.')

        if not isinstance(nworkers, int):
            raise TypeError('`nworkers` must have `int` type.')
        if not isinstance(author, str):
            raise TypeError('`author` must have `str` type.')
        if not isinstance(name, str):
            raise TypeError('`name` must have `str` type.')
        if not isinstance(compress, int):
            raise TypeError('`compress` must be integer.')
        else:
            if (compress > 9) and (compress < 0):
                raise ValueError('`compress` can be greater or equal to 0 and less than 9.')
        if cache_dir_fp is not None:
            if not path.isdir(cache_dir_fp):
                raise NotADirectoryError('`cache_dir_fp` is invalid.')
        if empc_cutoff <= 30:
            raise ValueError('`empc_cutoff must be greater than 30.`')
        if not cls._verify_chunksize(run_chunksize, io_chunksize, exec_chunksize):
            raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')
        if not isinstance(kmer_sizes, tuple):
            raise TypeError('`kmer_sizes` must be tuple.')
        else:
            if not verify_kmer_sizes(kmer_sizes):
                raise ValueError('`kmer_sizes` have invalid combination.')
        if len(kmer_sizes) == 0:
            raise ValueError('`kmer_sizes` cannot be empty.')
        if cache_dir_fp is not None:
            cache_dir_fp = mkdtemp(prefix=cls.__cache_build_prefix, dir=cache_dir_fp)
        else:
            cache_dir_fp = None
        zlib_state = True if compress > 0 else False
        zlib_level = compress if compress > 0 else 4

        tqdm.write("Preparing optimized chunks for best performance.")

        repseq_stats = seq_record_df.loc[:,cls.EMPC_FACTORS]
        included_rids_array, excluded_rids_array, difficulty_chunks = cls._split_by_difficulty_chunks(repseq_stats, kmer_sizes, io_chunksize, exec_chunksize, empc_cutoff, nworkers)

        parser_memory_cache = Memory(location=cache_dir_fp, verbose=0, compress=ceil(zlib_level / 2) if zlib_state else False)

        all_hmer_array = np.sort(np.array(list(generate_theoretical_hmers(kmer_sizes, io_chunksize)), dtype=np.uint64))

        tqdm.write("Creating template NetCDF file.")
        # dataset
        dataset_storer = Dataset(dataset_fp, 'w', format='NETCDF4')
        dataset_storer.setncatts(extra_metadata_dict)
        dataset_storer.dts_classifier_type = cls.MODEL_NAME
        dataset_storer.dts_type = cls.__name__
        dataset_storer.dts_compression = str(compress)
        current_timestamp = datetime.now()
        dataset_storer.dts_created = current_timestamp.strftime(cls.DATETIME_FORMAT)
        dataset_storer.dts_kmer_sizes = "|".join([str(ksize) for ksize in kmer_sizes])
        dataset_storer.dts_name = name
        dataset_storer.dts_author = author
        dataset_storer.dts_description = "Classifier Type: {}. Kmer Sizes: {}".format(cls.MODEL_NAME, ",".join([str(ksize) for ksize in kmer_sizes]))


        # dimensions
        dataset_storer.createDimension('mritem', None)
        dataset_storer.createDimension('mhitem', 2)
        dataset_storer.createDimension('rid', None)
        dataset_storer.createDimension('hmer', all_hmer_array.shape[0])

        # coordinates
        hmer_var = dataset_storer.createVariable('hmer', 'u8', ('hmer',))
        hmer_var[:] = all_hmer_array.astype('u8')
        mritem_var = dataset_storer.createVariable('mritem', str, ('mritem',))
        mritem_var[:2] = np.array(['valid', 'empc'], dtype=str)
        mhitem_var = dataset_storer.createVariable('mhitem', "S2", ('mhitem',))
        mhitem_var[:] = np.array(['fp', 'lp'], dtype="S2")

        rid_dtype = seq_record_df.index.values.astype('U').dtype
        rid_var = dataset_storer.createVariable('rid', rid_dtype, ('rid',))

        # data arrays
        raw = dataset_storer.createVariable('raw', 'b', ('rid', 'hmer'), zlib=zlib_state, complevel=zlib_level)
        rmeta = dataset_storer.createVariable('rmeta', 'u4', ('rid', 'mritem'), zlib=zlib_state, complevel=zlib_level)
        hmeta = dataset_storer.createVariable('hmeta', 'u4', ('rid', 'hmer', 'mhitem'), zlib=zlib_state, complevel=zlib_level)

        indexed_seq_record_df = seq_record_df.reset_index()

        index_label_map = indexed_seq_record_df[seq_record_df.index.name]

        mapped_seq_record_df = indexed_seq_record_df.reset_index().set_index(seq_record_df.index.name)

        parse_process_chunk_cached = parser_memory_cache.cache(parse_process_chunk)
        parsed_chunk_result_shelves = []

        ft_parse_pbar = tqdm(desc='Parsing and caching _feature sequences', total=included_rids_array.shape[0], position=0)
        d_level_pbar_dict = {d_empc_level: tqdm(total=len(d_rid_list), desc='Digesting difficulty level-{}/3'.format(str(d_empc_level)), bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}]', position=d_empc_level) for
                             d_io_chunksize, d_exec_chunksize, d_rid_list, d_empc_level in difficulty_chunks}

        for d_io_chunksize, d_exec_chunksize, d_rid_list, d_empc_level in difficulty_chunks:
            for d_r_rid_list in chunk_generator(d_rid_list, run_chunksize):
                parsed_chunk_result_shelves.extend(
                    Parallel(n_jobs=nworkers, prefer='processes', verbose=0)(delayed(parse_process_chunk_cached.call_and_shelve)
                                                                             (chunk_records_length, chunk_record_tuples, d_empc_level, d_exec_chunksize, kmer_sizes)
                                                                             for chunk_records_length, chunk_record_tuples in
                                                                             chunk_record_generator(cls.__make_target_sequence_records(mapped_seq_record_df,d_r_rid_list), io_chunksize, ft_parse_pbar)))
            d_level_pbar_dict[d_empc_level].n = d_level_pbar_dict[d_empc_level].total
            d_level_pbar_dict[d_empc_level].refresh()

        ft_parse_pbar.n = ft_parse_pbar.total
        ft_parse_pbar.refresh()

        all_rids_array = []
        rid_counter = 0
        hmer_pos_matrix_buffer = np.zeros((all_hmer_array.shape[0], 2), dtype='u2')

        ft_write_pbar = tqdm(desc='Adding digest into dataset file', total=seq_record_df.shape[0], position=4)
        for parsed_chunk_result_shelve in parsed_chunk_result_shelves:
            for d_empc_level, rid, hmer_array, hmer_pos_matrix in parsed_chunk_result_shelve.get():
                hmer_array_mask = np.isin(all_hmer_array, hmer_array, assume_unique=True).astype(np.bool_)
                hmer_pos_matrix_buffer[hmer_array_mask] = hmer_pos_matrix
                raw[rid_counter, :] = hmer_array_mask
                hmeta[rid_counter, :, :] = hmer_pos_matrix_buffer
                rmeta[rid_counter, 0] = True
                rmeta[rid_counter, 1] = d_empc_level
                all_rids_array.append(rid)
                rid_counter = rid_counter + 1
                hmer_pos_matrix_buffer.fill(0)
                ft_write_pbar.update(1)

        parser_memory_cache.clear(warn=False)

        hmer_pos_matrix_buffer.fill(0)
        hmer_array_mask_zeros = np.zeros((all_hmer_array.shape[0],), dtype=np.bool_)
        dts_excluded_pbar = tqdm(desc='Marking excluded representative sequences', total=excluded_rids_array.shape[0], position=5)
        for rid in excluded_rids_array.tolist():
            raw[rid_counter, :] = hmer_array_mask_zeros
            hmeta[rid_counter, :, :] = hmer_pos_matrix_buffer
            rmeta[rid_counter, 0] = False  # valid = False
            rmeta[rid_counter, 1] = 99999  # empc = 6
            all_rids_array.append(mapped_seq_record_df.loc[rid, 'index'])
            rid_counter = rid_counter + 1
            dts_excluded_pbar.update(1)
        dts_excluded_pbar.refresh()

        # setting last coordinate in parsed order
        all_rids_array = np.array(all_rids_array)
        rid_var[:] = index_label_map[all_rids_array].values.astype(rid_dtype)
        # refining
        # closing active files
        dataset_storer.close()
        return

    @property
    def records(self):
        return self._seq_records