from ._base import DHNBClassifierBase
from ._metakit import DhnbClassifierBaseMetabase,DhnbClassifierDatasetMetabase
from pmaf.database._metakit import DatabaseBackboneMetabase
from collections import defaultdict
from h5netcdf import File as H5NCDF_File
from pmaf.internal._extensions._cpython._pmafc_extension import make_sequence_record_tuple
from pmaf.internal._shared import chunk_generator
from pmaf.classifier.dhnb._shared import adjust_chunksize,add_primer_prefix, optimize_secondary_chunksize, calc_optimal_chunksize
import pmaf.classifier.dhnb._constructors as constr
import joblib as jbl
import xarray as xr
import warnings
warnings.simplefilter('ignore', category=UserWarning)
import numpy as np
from os import path
from datetime import datetime
from tempfile import mkdtemp
from dask import delayed
import dask.array as da
from dask.diagnostics import ProgressBar
from progress.bar import Bar
from tabulate import tabulate
from tempfile import TemporaryDirectory
from sys import stdout
Bar.check_tty = False
Bar.file = stdout


class DHNBClassifier(DHNBClassifierBase,DhnbClassifierBaseMetabase):
    def __init__(self, classifier_netcdf_fp, database_instance, cache_dir_fp=None, **kwargs):
        if not isinstance(database_instance, DatabaseBackboneMetabase):
            raise TypeError('`database_instance` has invalid type.')
        max_seq_length = database_instance.get_stats_by_rid(include='length').max()
        super().__init__(classifier_netcdf_fp, cache_dir_fp, 'cls_kmer_sizes', 'cls_compression',max_seq_length, **kwargs)
        if self.xr.cls_database_type != type(database_instance).__name__:
            raise TypeError('Database is not compatible with classifier.')
        self._db_instance = database_instance
        self._db_database_type = type(database_instance)
        self._index_tid = self.xr.coords['tid'].to_index()
        self._tmeta =  self.xr['tmeta']
        self._index_mtitem = None
        self._valid_tids = None
        self._invalid_tids = None
        self._reset_inits()

    def chunk(self, **kwargs):
        if self.state:
            if len(kwargs) > 0:
                tmeta_bkp = self._tmeta
                try:
                    if self._chunked:
                        if 'tid' in kwargs.keys():
                            self._tmeta = self._tmeta.chunk({'tid': -1})
                        if 'mtitem' in kwargs.keys():
                            self._tmeta = self._tmeta.chunk({'mtitem': -1})
                        if 'tmeta' in kwargs.keys():
                            self._tmeta = self.xr['tmeta']
                    if 'tid' in kwargs.keys():
                        self._tmeta = self._tmeta.chunk({'tid': kwargs['tid']})
                    if 'mtitem' in kwargs.keys():
                        self._tmeta = self._tmeta.chunk({'mtitem': kwargs['mtitem']})
                    if 'tmeta' in kwargs.keys():
                        self._tmeta = self.xr['tmeta'].chunk(kwargs['tmeta'] if kwargs['tmeta'] is not None else self.xr['tmeta'].encoding['chunksizes'])
                    self._chunked = True
                    super().chunk(**kwargs)
                except Exception as e:
                    self._tmeta = tmeta_bkp
                    raise e
            else:
                self._tmeta = self.xr['tmeta'].chunk(self.xr['tmeta'].encoding['chunksizes'])
                super().chunk(**kwargs)
        else:
            raise RuntimeError('Basefile is closed or at hold')

    def unchunk(self,vars=None,dims=None):
        if self.state:
            if self.chunked:
                last_chunk_state = self._tmeta.chunks
                if dims is not None:
                    if 'tid' in dims:
                        self._tmeta = self._tmeta.chunk({'tid': -1})
                    if 'mtitem' in dims:
                        self._tmeta = self._tmeta.chunk({'mtitem': -1})
                if vars is not None:
                    if 'tmeta' in vars:
                        self._tmeta = self.xr['tmeta']
                if dims is None and vars is None:
                    self._tmeta = self.xr['tmeta']
                super().unchunk(vars, dims)
                if (not self.chunked) and (last_chunk_state is not None):
                    self._chunked = True
        else:
            raise RuntimeError('Basefile is closed or at hold')

    def _reset_inits(self):
        super()._reset_inits()
        tmp_valid_tid_map = self.xr['tmeta'].to_pandas()['valid']
        self._valid_tids = tmp_valid_tid_map[tmp_valid_tid_map.astype(np.bool_)].index.values
        self._invalid_tids = tmp_valid_tid_map[~tmp_valid_tid_map.astype(np.bool_)].index.values
        self._index_mtitem = self.xr.coords['mtitem'].to_index()

    @classmethod
    def verify_dataset(self, dataset_instance):
        ret = False
        if (isinstance(dataset_instance, DhnbClassifierDatasetMetabase) and isinstance(dataset_instance, DHNBClassifierBase)):
            ret = True
        return ret

    @classmethod
    def verify_database(self, database_instance):
        ret = False
        if isinstance(database_instance, DatabaseBackboneMetabase):
            if database_instance.storage_manager.state == 1:
                if database_instance.storage_manager.has_repseq:
                    ret = True
        return ret

    @classmethod
    def verify_basefile(cls, basefile_fp):
        ret = False
        if isinstance(basefile_fp, str):
            if path.exists(basefile_fp):
                dataset_xr = xr.open_dataset(basefile_fp,engine='h5netcdf')
                if dataset_xr.cls_type == cls.__name__:
                    ret = True
                dataset_xr.close()
        return ret
    
    @classmethod
    def _filter_by_ksize(cls,database_instance,kmer_size):
        rstat_N_repmin = database_instance.get_stats_by_rid(include='N_repmax')
        tmp_tid_stats = database_instance.get_stats_by_tid(include=['singleton', 'subseqs'])
        non_singleton_tid_subs = tmp_tid_stats[~tmp_tid_stats['singleton']]['subseqs']
        higly_N_rep_rids = rstat_N_repmin[rstat_N_repmin >= kmer_size].index
        pre_potential_exc_tids = database_instance.find_tid_by_rid(higly_N_rep_rids,flatten=True,mode='array')
        potential_exc_tids = non_singleton_tid_subs.index[non_singleton_tid_subs.index.isin(pre_potential_exc_tids)]
        if len(potential_exc_tids)>0:
            potential_exc_tids_rids_sum = database_instance.find_rid_by_tid(potential_exc_tids,subs=True,mode='frame').map(lambda rids:np.isin(rids,higly_N_rep_rids).sum())
            possible_singleton_tids = non_singleton_tid_subs.loc[potential_exc_tids].sub(potential_exc_tids_rids_sum)
            new_singleton_tids = possible_singleton_tids[possible_singleton_tids<2].unique()
            return higly_N_rep_rids.values, new_singleton_tids
        else:
            return np.asarray([]),np.asarray([])

    def __filter_by_primer(self, primers_dict):
        verified_primers_dict = defaultdict(dict)
        rstat_N_repmin = self.database.get_stats_by_rid(include='N_repmax')
        tmp_tid_stats = self.database.get_stats_by_tid(include=['singleton', 'subseqs'])
        non_singleton_subs = tmp_tid_stats[~tmp_tid_stats['singleton']]['subseqs']
        for label, primer_sequence in primers_dict.items():
            primer_exc_rids = rstat_N_repmin[rstat_N_repmin >= len(primer_sequence)].index
            primer_exc_tids = self.database.find_tid_by_rid(primer_exc_rids,flatten=True,mode='array')
            if len(primer_exc_tids)>0:
                primer_exc_tid_exc_rid_totals = self.database.find_rid_by_tid(primer_exc_tids,subs=True,mode='frame').map(lambda rids:np.isin(rids,primer_exc_rids).sum())
                possible_singleton_tids = non_singleton_subs.loc[primer_exc_tids].sub(primer_exc_tid_exc_rid_totals)
                new_singleton_tids = possible_singleton_tids[possible_singleton_tids<2].unique()
                verified_primers_dict[label] = {'rids':primer_exc_rids.values,'tids':new_singleton_tids}
            else:
                verified_primers_dict[label] = {'rids':np.asarray([]),'tids':np.asarray([])}
        return dict(verified_primers_dict)

    def __init_primer_metadata(self, primers_dict):

        prior_rmeta_var = self.xr['rmeta']
        prior_tmeta_var = self.xr['tmeta']

        new_mritem_list = []
        new_mtitem_list = []
        for primer_label, primer_seq_str in primers_dict.items():
            if add_primer_prefix(primer_label, 'valid') not in self.xmritem:
                new_mritem_list.append(add_primer_prefix(primer_label, 'state'))
                new_mritem_list.append(add_primer_prefix(primer_label, 'valid'))
                new_mritem_list.append(add_primer_prefix(primer_label, 'first-pos'))
                new_mtitem_list.append(add_primer_prefix(primer_label, 'valid'))

        if len(new_mritem_list) > 0:
            new_mritem_coords = np.asarray(new_mritem_list, dtype=object)
            new_rmeta_var = xr.DataArray(data=np.zeros((len(self.xrid), len(new_mritem_coords)), dtype='u4'), dims=('rid', 'mritem'), coords={'rid': self.xrid, 'mritem': new_mritem_coords})
            post_rmeta_var = xr.concat((prior_rmeta_var, new_rmeta_var), dim='mritem', join='exact')
        else:
            post_rmeta_var = prior_rmeta_var.load()

        if len(new_mtitem_list) > 0:
            new_mtitem_coords = np.asarray(new_mtitem_list, dtype=object)
            new_tmeta_var = xr.DataArray(data=np.zeros((len(self.xtid), len(new_mtitem_coords)), dtype='u4'), dims=('tid', 'mtitem'), coords={'tid': self.xtid, 'mtitem': new_mtitem_coords})
            post_tmeta_var = xr.concat((prior_tmeta_var, new_tmeta_var), dim='mtitem', join='exact')
        else:
            post_tmeta_var = prior_tmeta_var.load()

        primer_verified_dict = self.__filter_by_primer(primers_dict)

        for primer_label, verification_result in primer_verified_dict.items():
            primer_passed_rid_mask = (~self.xrid.isin(verification_result['rids']))
            primer_passed_tid_mask = (~self.xtid.isin(verification_result['tids']))
            post_rmeta_var.loc[primer_passed_rid_mask, add_primer_prefix(primer_label, 'valid')] = 1
            post_tmeta_var.loc[primer_passed_tid_mask, add_primer_prefix(primer_label, 'valid')] = 1

        return post_rmeta_var, post_tmeta_var

    def _refine_by_primer(self, primers_dict):

        if not isinstance(primers_dict, dict):
            raise TypeError('`primer_dict` must be a dictionary.')
        if self.cache_dir is not None:
            cache_dir = mkdtemp(prefix=self._cache_prefix, dir=self.cache_dir)
            tmp_dir = None
        else:
            tmp_dir = TemporaryDirectory(prefix=self._cache_prefix)
            cache_dir = tmp_dir.name

        print("> Parsing primers and assigning metadata.")

        rmeta_var, tmeta_var = self.__init_primer_metadata(primers_dict)

        all_valid_label = ['valid'] + [add_primer_prefix(primer_label, 'valid') for primer_label in primers_dict.keys()]

        valid_rid_vector = rmeta_var.indexes['rid'][rmeta_var.loc[:, all_valid_label].all(dim='mritem')]
        valid_tid_vector = tmeta_var.indexes['tid'][tmeta_var.loc[:, all_valid_label].all(dim='mtitem')]

        primer_records_list = []
        ordered_primer_ids = []
        ordered_mritem_labels = []

        for primer_i, (primer_label, primer_seq_str) in enumerate(primers_dict.items()):
            primer_id = primer_i + 1
            ordered_primer_ids.append(primer_id)
            primer_records_list.append(make_sequence_record_tuple(primer_id, primer_seq_str))
            state_label = add_primer_prefix(primer_label, 'state')
            first_post_label = add_primer_prefix(primer_label, 'first-pos')
            ordered_mritem_labels.extend([state_label, first_post_label])

        primer_records_tuple = tuple(primer_records_list)

        rid_empc_levels = rmeta_var.loc[valid_rid_vector, 'empc'].to_pandas()

        print("> Making preparations to get best performance.")

        refiner_memory_cache = jbl.Memory(location=cache_dir, mmap_mode='r', verbose=0)

        parse_refine_primer_chunk_cached = refiner_memory_cache.cache(constr.parse_refine_primer_chunk)

        parsed_chunk_result_shelves = []

        print('> Parsing and caching reference local sequences.')
        db_digest_pbar = Bar('Digesting Sequences', max=len(valid_rid_vector))

        for d_empc_level, d_rid_group in rid_empc_levels.groupby(rid_empc_levels, sort=True):
            d_io_batch_size, d_exec_chunksize = adjust_chunksize(self.io_chunksize, self.exec_chunksize, d_empc_level, d_rid_group.index.shape[0], self.nworkers)
            d_rid_list = d_rid_group.index.tolist()
            if len(d_rid_list):
                db_digest_pbar.message = 'Digesting Sequence Difficulty Level - {}:'.format(d_empc_level)
            for d_r_rid_list in chunk_generator(d_rid_list, self.run_chunksize):
                parsed_chunk_result_shelves.extend(
                    jbl.Parallel(n_jobs=self.nworkers, prefer='threads', batch_size=d_io_batch_size, pre_dispatch=2 * d_io_batch_size, verbose=0)
                    (jbl.delayed(lambda *args: (args[0], parse_refine_primer_chunk_cached.call_and_shelve(*args)))
                     (d_exec_chunk_rids, ordered_primer_ids, d_exec_chunk_record_tuples, primer_records_tuple)
                     for d_exec_chunk_rids, d_exec_chunk_record_tuples in constr.db_chunk_record_generator(d_r_rid_list, d_exec_chunksize, self.database, db_digest_pbar)))
        db_digest_pbar.finish()

        print("> Finalizing Refining.")
        db_write_pbar = Bar('Building dataset from digest.', max=len(valid_rid_vector))
        for rid_chunk, parsed_chunk_result_shelve in parsed_chunk_result_shelves:
            parsed_result = parsed_chunk_result_shelve.get()
            rmeta_var.loc[list(rid_chunk), ordered_mritem_labels] = parsed_result
            db_write_pbar.next(len(rid_chunk))

        print("> Adding digest into storage file.")
        self._hold_basefile()
        tmp_store = H5NCDF_File(self.basefile_fp, mode='a')
        tmp_store.resize_dimension('mritem', len(rmeta_var.coords['mritem']))
        tmp_store.resize_dimension('mtitem', len(tmeta_var.coords['mtitem']))
        tmp_store['mritem'][:] = rmeta_var.coords['mritem']
        tmp_store['mtitem'][:] = tmeta_var.coords['mtitem']
        tmp_store['rmeta'][:] = rmeta_var.values
        tmp_store['tmeta'][:] = tmeta_var.values
        tmp_store.flush()
        tmp_store.close()
        self._release_basefile()
        self._reset_inits()
        refiner_memory_cache.clear(warn=False)
        if self.cache_dir is None:
            tmp_dir.cleanup()
        return

    @classmethod
    def build(cls, database_instance, classifier_fp, # reference local to use and classifier file path
              kmer_sizes=(6, 7), # Target kmer sizes
              cache_dir_fp=None, # If None then use system /tmp
              run_chunksize=30000, io_chunksize=None, exec_chunksize=None,
              empc_cutoff=35, # Rough cutoff for very complicated and non-informative sequences
              nworkers=(8,16), # (nproccesses, nthreads)
              force_new=False, # If True writes over existing storage
              compress=4, # Compression level for hmeta and joblib memory cache (only if memmap = False)
              memmap=True, # If true do not compress intermediate cache and directly store as numpy memmap. This is much much faster than using compression
              author='', name=''): # Self explanatory

        if not isinstance(database_instance, DatabaseBackboneMetabase):
            raise TypeError('`database_instance` has invalid type.')
        else:
            if database_instance.storage_manager.state != 1:
                raise ValueError('`database_instance` has invalid state.')
            else:
                if not database_instance.storage_manager.has_repseq:
                    raise ValueError('`database_instance` does not have any representative sequences.')
        if not isinstance(nworkers, tuple):
            raise TypeError('`nworkers` must be `tuple`.')
        if not all([isinstance(n, int) for n in nworkers]):
            raise TypeError('`nworkers` must be (`int`, `int`).')
        if not isinstance(author, str):
            raise TypeError('`author` must have `str` type.')
        if not isinstance(name, str):
            raise TypeError('`name` must have `str` type.')
        if not isinstance(compress, int):
            raise TypeError('`compress` must be integer.')
        else:
            if (compress > 9) and (compress < 0):
                raise ValueError('`compress` can be greater or equal to 0 and less than 9.')
        if (path.exists(classifier_fp)) and (not force_new):
            raise FileExistsError('File must not exist. Use `force_new` = True to rewrite.')
        if cache_dir_fp is not None:
            if not path.isdir(cache_dir_fp):
                raise NotADirectoryError('`cache_dir_fp` is invalid.')
        if empc_cutoff <= 1:
            raise ValueError('`empc_cutoff must be greater than 1.`')
        if not ((cls.MEM_LIMIT > 1) and (cls.MEM_LIMIT < 40)):
            raise ValueError('`mem_limit` must be greater than 1% and less than 40%.`')
        if not isinstance(kmer_sizes, tuple):
            raise TypeError('`kmer_sizes` must be tuple.')
        else:
            if not constr.verify_kmer_sizes(kmer_sizes):
                raise ValueError('`kmer_sizes` have invalid combination.')
        if len(kmer_sizes) == 0:
            raise ValueError('`kmer_sizes` cannot be empty.')
        if (io_chunksize is None) or (exec_chunksize is None):
            # Following is recommended because it calculates optimal execution chunksize and io_chunksize.
            rid_length_stats = database_instance.get_stats_by_rid(include='length')
            io_chunksize, exec_chunksize = optimize_secondary_chunksize(run_chunksize, nworkers[0], max(kmer_sizes), int(rid_length_stats.max()), True, cls.MEM_LIMIT, True)
        else:
            if not cls._verify_chunksize(run_chunksize, io_chunksize, exec_chunksize):
                raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')
        if cache_dir_fp is not None:
            cache_dir = mkdtemp(prefix=cls._cache_prefix, dir=cache_dir_fp)
            tmp_dir = None
        else:
            tmp_dir = TemporaryDirectory(prefix=cls._cache_prefix)
            cache_dir = tmp_dir.name
        zlib_state = True if compress > 0 else False
        cmp_level = compress if compress > 0 else 4

        print("> Making preparations to get best performance.\n")
        # prepeare memory cache by joblib
        if memmap:
            parser_memory_cache = jbl.Memory(location=cache_dir, mmap_mode='r', verbose=0)
        else:
            parser_memory_cache = jbl.Memory(location=cache_dir, verbose=0, compress=cmp_level if zlib_state else False)

        # Prepare and identify singletons that already present, that will be present if we remove sequnces with N_repmax>=min(kmer_sizes)
        # singletons are identified both for tids and rids
        repseq_stats = database_instance.get_stats_by_rid(include=cls.EMPC_FACTORS)
        tid_stats_singeltons = database_instance.get_stats_by_tid(include='singleton')
        prior_tid_singeltons = tid_stats_singeltons[tid_stats_singeltons].index.values
        prior_rid_tid_singeltons = database_instance.find_rid_by_tid(prior_tid_singeltons, flatten=True, mode='array')
        new_rid_singelton, new_tid_singeltons = cls._filter_by_ksize(database_instance, min(kmer_sizes))
        pre_excluded_rids = np.union1d(prior_rid_tid_singeltons, new_rid_singelton)
        tid_singeltons = np.union1d(prior_tid_singeltons, new_tid_singeltons)
        # perform final filtering in addition to above and split rids by difficulty levels
        included_rids_array, excluded_rids_array, difficulty_chunks = cls._split_by_difficulty_chunks(repseq_stats, kmer_sizes, io_chunksize, exec_chunksize, empc_cutoff, nworkers[0], pre_excluded_rids)

        all_tids_vector = np.sort(database_instance.xtid.values) # retrieve and sort tids
        all_hmer_vector = np.sort(np.array(list(constr.generate_theoretical_hmers(kmer_sizes, io_chunksize)), dtype='u8')) # generate and sort tids
        total_rids = len(included_rids_array) + len(excluded_rids_array) # total rids
        total_hmers = len(all_hmer_vector) # total hmers
        total_tids = len(all_tids_vector) # total tids

        hmer_coord = all_hmer_vector.astype('u8') #cast hmer array/coords to respective dtype
        tid_coord = all_tids_vector.astype('u4') # cast tid array/coords to respective dtype
        mritem_coord = np.asarray(['valid', 'empc'], dtype=str) #make rid meta data coordinates. With Unlimited Dimensions!
        mtitem_coord = np.asarray(['valid'], dtype=str) #make tid meta data coordinates. With Unlimited Dimensions!
        mhitem_coord = np.asarray(['fp', 'lp'], dtype=str) #make hmer meta data coordinates. Only 'fp', 'lp', first position of kmer/hmer in sequence and last position, respectively

        # IMPORTANT! `calc_optimal_chunksize` functions NEVER should and do generate rid chunksize less than exec_chunksize
        # `calc_optimal_chunksize` is far not perfect but attempts to make a square-like block of data block that will consume only fraction of RAM defined by cls.MEM_LIMIT, default 5%
        raw_chunksize = calc_optimal_chunksize(1, exec_chunksize, total_rids, total_hmers, None, cls.MEM_LIMIT) # Re-evaluate chunksize for sinlge dask block for `raw` variable.  Typically relatively square like blocks
        rmeta_chunksize = calc_optimal_chunksize(4, exec_chunksize, total_rids, 2, None, cls.MEM_LIMIT)# Re-evaluate chunksize for sinlge dask block for `rmeta` variable. Typically very large blocks
        tmeta_chunksize = calc_optimal_chunksize(4, exec_chunksize, total_tids, 1, None, cls.MEM_LIMIT)# Re-evaluate chunksize for sinlge dask block for `tmeta` variable. Typically very large blocks
        hmeta_chunksize = calc_optimal_chunksize(2, exec_chunksize, total_rids, total_hmers, 2, cls.MEM_LIMIT)# Re-evaluate chunksize for sinlge dask block for `hmeta` variable.  Much smaller blocks than `raw` but more wide than long.

        # Generate summary information about upcoming data processing.
        optimization_summary = [['Samples/Features', total_rids, total_tids, total_hmers],
                                ['Singletons', len(pre_excluded_rids), len(tid_singeltons), None],
                                ['Passed', len(included_rids_array), total_tids - len(tid_singeltons), None],
                                ['Excluded', len(excluded_rids_array), len(tid_singeltons), None],
                                ['Difficulty Level 1', len(difficulty_chunks[0][2]), None, None],
                                ['Difficulty Level 2', len(difficulty_chunks[1][2]), None, None],
                                ['Difficulty Level 3', len(difficulty_chunks[2][2]), None, None],
                                ['`raw` chunksize', raw_chunksize[0], None, raw_chunksize[1]],
                                ['`rmeta` chunksize', rmeta_chunksize[0], None, None],
                                ['`tmeta` chunksize', None, tmeta_chunksize[0], None],
                                ['`hmeta` chunksize', hmeta_chunksize[0], None, hmeta_chunksize[1]]]

        print(tabulate(optimization_summary, headers=['Total', 'Refs (Seq)', 'Reps (Tax)', 'K-mers'], tablefmt='github', numalign="center", missingval='-'))

        estimated_filesize = (total_rids * (1 * total_hmers + 4 * 2 + 2 * total_hmers * 2) + 1 * total_tids * 4) / (1024 ** 3) # Should be correct esimate

        print("\nEstimated Uncompressed File Size: {:,.5g} Gigabytes".format(estimated_filesize))
        print("Approximate Compressed File Size: {:,.3g} Gigabytes".format(estimated_filesize * 0.05)) # Very rough and invalid estimate!
        print("\nRuntime Chunksize: {:,} per chunk.".format(run_chunksize)) # This determines how confident you are in your RAM. Each time total rid number will be equal to run_chunksize. Processes will restart without relying on joblib batch adjusting.
        print("I/O Chunksize: {:,} per chunk/batch.".format(io_chunksize)) # This is rough number and it actually transformed to batch sizes. Like ceil(io_chunksize/exe_chunksize)
        print("Execution Chunksize: {:,} per chunk.".format(exec_chunksize)) # This is the most important chunksize. It determines how much data will go to C-parser and minimum data that will be written as single block along rid axis

        parse_process_chunk_cached = parser_memory_cache.cache(constr.parse_process_chunk) # transform parser function into joblib cache function
        parsed_chunk_result_shelves = [] # This is where all shelves will be stored
        rid_ordered_list = [] # This is where all rids are appended in order that shelves appear. This is very important and should follow shelves. Otherwise, invalid coordinates will be present in final data

        print('\n> Parsing and caching reference local sequences.')
        db_digest_pbar = Bar('Digesting Sequences', max=len(included_rids_array))

        for d_io_batch_size, d_exec_chunksize, d_rid_list, d_empc_level in difficulty_chunks: # Run parsing proccess separately for each difficulty level
            if len(d_rid_list): # if difficulty level has at least 1 rid then update progress bar
                db_digest_pbar.message = 'Digesting Sequence Difficulty Level - {}:'.format(d_empc_level)
            for d_r_rid_list in chunk_generator(d_rid_list, run_chunksize): # Run parsing process in chunks based on run_chunksize. Each loop will restart workers and free memory.
                tmp_parsed_chunk_result_shelves = jbl.Parallel(n_jobs=nworkers[0], prefer='processes', batch_size=d_io_batch_size, pre_dispatch=2 * d_io_batch_size, verbose=0) \
                    (jbl.delayed(lambda *args: (args[0], parse_process_chunk_cached.call_and_shelve(*args))) # Produce result in form (exec_chunk_rid_list, shelves)
                     (d_exec_chunk_rids, d_exec_chunk_record_tuples, kmer_sizes) # parameters that will be passed to `parse_process_chunk`
                     for d_exec_chunk_rids, d_exec_chunk_record_tuples in constr.db_chunk_record_generator(d_r_rid_list, d_exec_chunksize, database_instance, db_digest_pbar)) # split into further exec chunks
                parsed_chunk_result_shelves.extend(tmp_parsed_chunk_result_shelves) # append parsed results in flat manner to the ref shelve collection
                rid_ordered_list.extend([rid for exec_chunk in tmp_parsed_chunk_result_shelves for rid in exec_chunk[0]]) # in the same order extend the rids in reference rid_list

        db_digest_pbar.finish() # Finalize progress bar

        rid_ordered_list.extend(excluded_rids_array.tolist()) #Add exluded rids to the ordered reference rid_list

        print("\n> Preparing Dask task graph.")

        # This two lines generate number of dask blocks required to make
        # Because each shelve contains minimum exec_chunksize rids and total number of chunksize we desire and confident that will fit to memory is raw_chunksize or hmeta_chunksize
        # This number regulates two for - loops bellow using `chunk_generator` which actually generates chunks of already chunked shelves by nblocks
        raw_rid_nblocks = round(raw_chunksize[0] / exec_chunksize)
        hmeta_rid_nblocks = round(hmeta_chunksize[0] / exec_chunksize)

        # This two lines split complete ref hmer array into chunks along hmer axis typically is not that large blocks should be generated. It depends on kmer size and exec_chunksize
        # So each line actually breaks total(all_hmer_vector) = N_hmer_blocks* [block_hmer_array of size xxx_chunksize[1]]
        raw_hmer_blocks = tuple(chunk_generator(all_hmer_vector, raw_chunksize[1]))
        hmeta_hmer_blocks = tuple(chunk_generator(all_hmer_vector, hmeta_chunksize[1]))

        # Total number of chunksize in each block
        raw_hmer_chunks_list = [len(chunk) for chunk in raw_hmer_blocks]
        hmeta_hmer_chunks_list = [len(chunk) for chunk in hmeta_hmer_blocks]

        # This two dicts will contain all required information about blocks such as
        # xxx_block_cache_map[(location of the block in final dask array)] = (block_hmer_array, corresponding list of shelves each with length of ~ exec_chunksize)
        raw_block_cache_map = defaultdict(tuple)
        hmeta_block_cache_map = defaultdict(tuple)

        # This two lists will contain actual number of chunks in each generated block, which obviously will vary during exhaustion and different difficulty levels
        raw_rid_chunks_list = []
        hmeta_rid_chunks_list = []

        # This loop generates blocks required to construct `raw` dask array of shape = (total_rids,total_hmers) and dtype = int8 or bool
        for rid_block_i, raw_block_chunks_parsed_shelves_tuple in enumerate(chunk_generator(parsed_chunk_result_shelves, raw_rid_nblocks)):
            rid_block, raw_block_chunks_parsed_shelves = zip(*raw_block_chunks_parsed_shelves_tuple)
            rid_block_flat = [rid for rid_chunk in rid_block for rid in rid_chunk]
            raw_rid_chunks_list.append(len(rid_block_flat))
            for hmer_block_i, block_hmer_array in enumerate(raw_hmer_blocks):
                raw_block_cache_map[(rid_block_i, hmer_block_i)] = (block_hmer_array, raw_block_chunks_parsed_shelves)

        # This loop generates blocks required to construct `hmeta` dask array of shape = (total_rids,total_hmers,2) and dtype = int16
        for rid_block_i, hmeta_block_chunks_parsed_shelves_tuple in enumerate(chunk_generator(parsed_chunk_result_shelves, hmeta_rid_nblocks)):
            rid_block, hmeta_block_chunks_parsed_shelves = zip(*hmeta_block_chunks_parsed_shelves_tuple)
            rid_block_flat = [rid for rid_chunk in rid_block for rid in rid_chunk]
            hmeta_rid_chunks_list.append(len(rid_block_flat))
            for hmer_block_i, block_hmer_array in enumerate(hmeta_hmer_blocks):
                hmeta_block_cache_map[(rid_block_i, hmer_block_i, 0)] = (block_hmer_array, hmeta_block_chunks_parsed_shelves) # final coordinate is not chunked and always 0

        # Make final chunksize tuples required by dask da.map_blocks
        raw_chunks = (tuple(raw_rid_chunks_list), tuple(raw_hmer_chunks_list))
        hmeta_chunks = (tuple(hmeta_rid_chunks_list), tuple(hmeta_hmer_chunks_list), (2,))

        # Transform xxx_block_cache_map to dask delayed objects in order to avoid unnecessary data transfer during construction
        # This also advised by dask Best Practices to let dask optimize its graph to best
        raw_block_cache_map_delayed = delayed(dict(raw_block_cache_map))
        hmeta_block_cache_map_delayed = delayed(dict(hmeta_block_cache_map))

        # Lazy construct actual dask arrays `raw` and `hmeta` in blocks generated above
        raw_passed_da = da.map_blocks(constr.raw_transform_shelve_to_block, raw_block_cache_map_delayed, chunks=raw_chunks, dtype='b')
        hmeta_passed_da = da.map_blocks(constr.hmeta_transform_shelve_to_block, hmeta_block_cache_map_delayed, chunks=hmeta_chunks, dtype='u2')

        # Lazy create dask zeros arrays `raw` and `hmeta` for exluded rids. Arrays use exactly same chunksize as above but opimized by dask itself
        raw_excluded_da = da.zeros((len(excluded_rids_array), total_hmers), dtype='b', chunks=raw_chunksize)
        hmeta_excluded_da = da.zeros((len(excluded_rids_array), total_hmers, 2), dtype='u2', chunks=hmeta_chunksize)

        # Concatenate passed dask array with exluded dask arrays
        raw_da = da.concatenate([raw_passed_da, raw_excluded_da], axis=0)
        hmeta_da = da.concatenate([hmeta_passed_da, hmeta_excluded_da], axis=0)

        # Finally transform complete and ordered rid list to numpy array with correct dtype
        rid_coord = np.asarray(rid_ordered_list, dtype='u4')

        # Lazy construct dask array for `tmeta` with marked exluded tids
        tid_excluded_mask = np.isin(all_tids_vector, tid_singeltons, assume_unique=True)
        tmeta_array = np.where(tid_excluded_mask, 0, 1).astype('u4').reshape((total_tids, 1))

        # Lazy construct dask array for `rmeta` with marked exluded tids and difficulty levels
        rmeta_array = np.zeros(shape=(total_rids, 2), dtype='u4')
        rid_excluded_mask = np.isin(rid_coord, excluded_rids_array, assume_unique=True)
        rmeta_array[~rid_excluded_mask, 0] = 1
        rmeta_array[np.isin(rid_coord, difficulty_chunks[0][2]), 1] = difficulty_chunks[0][-1]
        rmeta_array[np.isin(rid_coord, difficulty_chunks[1][2]), 1] = difficulty_chunks[1][-1]
        rmeta_array[np.isin(rid_coord, difficulty_chunks[2][2]), 1] = difficulty_chunks[2][-1]

        # Convert dask arrays to xarray DataArrays
        raw_var = xr.DataArray(data=raw_da, dims=('rid', 'hmer'), coords={'rid': rid_coord, 'hmer': hmer_coord})
        hmeta_var = xr.DataArray(data=hmeta_da, dims=('rid', 'hmer', 'mhitem'), coords={'rid': rid_coord, 'hmer': hmer_coord, 'mhitem': mhitem_coord})
        rmeta_var = xr.DataArray(data=rmeta_array, dims=('rid', 'mritem'), coords={'rid': rid_coord, 'mritem': mritem_coord})
        tmeta_var = xr.DataArray(data=tmeta_array, dims=('tid', 'mtitem'), coords={'tid': tid_coord, 'mtitem': mtitem_coord})


        # Create xarray DataSet
        classifier_dts = xr.Dataset(
            data_vars=dict(
                raw=raw_var,
                rmeta=rmeta_var,
                hmeta=hmeta_var,
                tmeta=tmeta_var),
            coords=dict(
                hmer=('hmer', hmer_coord),
                rid=('rid', rid_coord),
                tid=('tid', tid_coord),
                mritem=('mritem', mritem_coord),
                mtitem=('mtitem', mtitem_coord),
                mhitem=('mhitem', mhitem_coord)),
            attrs=dict(
                cls_name=name,
                cls_type=cls.MODEL_NAME,
                cls_created=datetime.now().strftime(cls.DATETIME_FORMAT),# time of creation
                cls_author=author,
                cls_database_name=database_instance.name, # Name of the local
                cls_database_type=type(database_instance).__name__, # Class name of the local
                cls_kmer_sizes=kmer_sizes,
                cls_description="Classifier Type: {}. Database {}. Kmer Sizes: {}".format(cls.MODEL_NAME, database_instance.name, ",".join([str(ksize) for ksize in kmer_sizes])),
                cls_compression=compress,
                cls_exec_chunksize=exec_chunksize,
                cls_io_chunksize=io_chunksize,
                cls_run_chunksize=run_chunksize))

        print("> Creating final storage file.")

        # Lazy generate NetCDF 4 file via h5netcdf backend
        delayed_save = classifier_dts.to_netcdf(
            path=classifier_fp,
            format='NETCDF4',
            engine='h5netcdf',
            unlimited_dims={'mritem', 'mtitem'},
            compute=False,
            encoding=dict(
                raw=dict(dtype='b', chunksizes=raw_chunksize, compression='lzf', shuffle=True),
                rmeta=dict(dtype='u4', chunksizes=rmeta_chunksize, compression='lzf', shuffle=True),
                tmeta=dict(dtype='u4', chunksizes=tmeta_chunksize, compression='lzf', shuffle=True),
                hmeta=dict(dtype='u2', chunksizes=hmeta_chunksize, zlib=True, complevel=cmp_level, shuffle=True))) # Use gzip to compress hmeta since it used rarely and has large size

        with ProgressBar(): # Register dask ProgressBar for computation
            delayed_save.compute(scheduler='threads', num_workers=nworkers[1], optimize_graph=True) #Optimize graph and run all computation process using thread based scheduler.

        # Close all active instances and empty the cache
        database_instance.close()
        classifier_dts.close()
        parser_memory_cache.clear()
        if cache_dir_fp is None:
            tmp_dir.cleanup()
        return

    def classify(self, dataset, **kwargs):
        if not self.verify_dataset(dataset):
            raise TypeError('`dataset_instance` has invalid type.')
        if set(self.kmer_sizes) != set(dataset.kmer_sizes):
            raise TypeError('Dataset and classifier have different kmers.')
    
    @property
    def xtid(self):
        return self._index_tid

    @property
    def xmtitem(self):
        return self._index_mtitem

    @property
    def tmeta(self):
        if self.state:
            if self.chunked:
                return self._tmeta
            else:
                return self.xr['tmeta']
        else:
            raise RuntimeError('Basefile is closed or at hold.')

    @property
    def database(self):
        return self._db_instance