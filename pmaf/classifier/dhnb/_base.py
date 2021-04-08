from abc import abstractmethod
from ._metakit import DhnbClassifierBackboneMetabase
from ._shared import add_primer_prefix, adjust_chunksize, optimize_secondary_chunksize
from os import path, mkdir
import xarray as xr
import numpy as np
import pandas as pd
from math import exp
from statistics import mean

class DHNBClassifierBase(DhnbClassifierBackboneMetabase):
    MODEL_NAME = "Dynamic Hierarchical Naive Bayes Classifier"
    DATETIME_FORMAT = "%d/%m/%Y - %H:%M:%S"
    SUBROOT_DIR= 'mmaf_dhnb_cache'
    EMPC_COEFFICIENTS = ['tab', 'complexity', 'amb_mean', 'amb_rep_mean']
    EMPC_FACTORS = ['length', 'tab', 'complexity', 'amb_mean', 'amb_rep_mean']
    MEM_LIMIT = 5
    _cache_prefix = 'dhnb_'
    __valid_dimensions = ['rid','hmer','mhitem','mritem']
    __valid_variables = ['raw','rmeta','hmeta']
    def __init__(self, basefile_fp, cache_dir_fp, kmer_sizes_attr, compression_attr, max_seq_length, run_chunksize = 20000, io_chunksize=None, exec_chunksize=None, nworkers=8):
        if not isinstance(basefile_fp, str):
            raise ValueError('`basefile_fp` must be string.')
        if not path.exists(basefile_fp):
            raise FileNotFoundError('NetCDF file path not found')
        if not isinstance(nworkers,int):
            raise TypeError('`nworkers` must have `int` type.')
        tmp_cache_dir = None
        tmp_cache_root_dir = None
        if cache_dir_fp is not None:
            if not path.isdir(cache_dir_fp):
                raise NotADirectoryError('`cache_dir_fp` is invalid.')
            else:
                tmp_cache_root_dir = path.abspath(cache_dir_fp)
                tmp_cache_dir_path = path.join(tmp_cache_root_dir,self.SUBROOT_DIR)
                if not path.exists(tmp_cache_dir_path):
                    mkdir(tmp_cache_dir_path)
                tmp_cache_dir = tmp_cache_dir_path
        self._cache_root_dir = tmp_cache_root_dir
        self._cache_dir = tmp_cache_dir
        self._basefile_netcdf_fp = path.abspath(basefile_fp)
        self._basefile_xr = xr.open_dataset(self._basefile_netcdf_fp,engine='h5netcdf')
        self._kmer_sizes = tuple(map(int,self._basefile_xr.attrs[kmer_sizes_attr].split('|')))
        if (io_chunksize is None) or (exec_chunksize is None):
            io_chunksize, exec_chunksize = optimize_secondary_chunksize(run_chunksize, nworkers, max(self._kmer_sizes), max_seq_length, True, self.MEM_LIMIT, True)
        else:
            if not self._verify_chunksize(run_chunksize, io_chunksize, exec_chunksize):
                raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')

        self._run_chunksize = run_chunksize
        self._io_chunksize = io_chunksize
        self._exec_chunksize = exec_chunksize
        self._nworkers = nworkers

        self._compression = int(self._basefile_xr.attrs[compression_attr])

        self._raw = self._basefile_xr['raw']
        self._rmeta = self._basefile_xr['rmeta']
        self._hmeta = self._basefile_xr['hmeta']

        self._index_hmer = self._basefile_xr.coords['hmer'].to_index()
        self._index_rid = self._basefile_xr.coords['rid'].to_index()
        self._index_mritem = None
        self._index_mhitem = None
        self._valid_rids = None
        self._invalid_rids = None
        self._init_state = True
        self._at_hold = False
        self._chunked = False
        for attr,value in  self._basefile_xr.attrs.items():
            super().__setattr__(attr, value)

        self._reset_inits()

    def __repr__(self):
        class_name = self.__class__.__name__
        if self._init_state:
            read_state =  "Active" if not self._at_hold else "Hold"
            total_kmer = str(self._index_hmer.shape[0])
            kmer_sizes = ','.join(map(str,self._kmer_sizes))
            total_valid_rid =  str(self._valid_rids.shape[0])
            total_invalid_rid = str(self._invalid_rids.shape[0])
            total_rid_meta = str(self._index_mritem.shape[0])
            repr_str = "<{}:[{}], Sequence: [V/I/M:{}/{}/{}], Features: [{}], K-sizes: [{}]>".\
                format(class_name, read_state, total_valid_rid, total_invalid_rid, total_rid_meta, total_kmer,kmer_sizes)
        else:
            repr_str = "<{}:[Closed]>".format(class_name)
        return repr_str

    def __del__(self): 
        self._basefile_xr.close()
        return

    @classmethod
    def _verify_chunksize(self, run_chunksize, io_chunksize, exec_chunksize):
        if (run_chunksize < io_chunksize) or (io_chunksize < exec_chunksize) or (run_chunksize<exec_chunksize):
            return False
        else:
            return True

    def _reset_inits(self):
        if self._init_state and not self._at_hold:
            tmp_valid_rid_map = self._basefile_xr['rmeta'].loc[:,'valid'].to_pandas()
            self._valid_rids = tmp_valid_rid_map[tmp_valid_rid_map.astype(np.bool_)].index.values
            self._invalid_rids = tmp_valid_rid_map[~tmp_valid_rid_map.astype(np.bool_)].index.values
            self._index_mritem = self._basefile_xr.coords['mritem'].to_index()
            self._index_mhitem = self._basefile_xr.coords['mhitem'].to_index()
        else:
            raise RuntimeError('Basefile is closed or at hold.')
        
    def close(self):
        if not self._at_hold:
            self._basefile_xr.close()
            self._init_state = False
        else:
            raise RuntimeError('Basefile is currently at hold.')

    def __chunk_by_dim(self,dim,chunksize):
        if dim == 'rid':
            self._raw = self._raw.chunk({'rid': chunksize})
            self._rmeta = self._rmeta.chunk({'rid': chunksize})
            self._hmeta = self._hmeta.chunk({'rid': chunksize})
        elif dim == 'hmer':
            self._raw = self._raw.chunk({'hmer': chunksize})
            self._hmeta = self._hmeta.chunk({'hmer': chunksize})
        elif dim == 'mhitem':
            self._hmeta = self._hmeta.chunk({'mhitem': chunksize})
        elif dim == 'mritem':
            self._rmeta = self._rmeta.chunk({'mritem': chunksize})
        else:
            raise ValueError('Invalid dimension name.')

    def __chunk_by_var(self,var,chunks):
        if var == 'raw':
            self._raw = self._raw.chunk(chunks if chunks is not None else self._basefile_xr['raw'].encoding['chunksizes'])
        elif var == 'rmeta':
            self._rmeta = self._rmeta.chunk(chunks if chunks is not None else self._basefile_xr['rmeta'].encoding['chunksizes'])
        elif var == 'hmeta':
            self._hmeta = self._hmeta.chunk(chunks if chunks is not None else self._basefile_xr['hmeta'].encoding['chunksizes'])
        else:
            raise ValueError('Invalid variable name.')

    def __unchunk_by_var(self,var):
        if var == 'raw':
            self._raw = self._basefile_xr['raw']
        elif var == 'rmeta':
            self._rmeta = self._basefile_xr['rmeta']
        elif var == 'hmeta':
            self._hmeta = self._basefile_xr['hmeta']
        else:
            raise ValueError('Invalid variable name.')


    def __unchunk_by_dim(self,dim):
        if dim == 'rid':
            self._raw = self._raw.chunk({'rid': -1})
            self._rmeta = self._rmeta.chunk({'rid': -1})
            self._hmeta = self._hmeta.chunk({'rid': -1})
        elif dim == 'hmer':
            self._raw = self._raw.chunk({'hmer': -1})
            self._hmeta = self._hmeta.chunk({'hmer': -1})
        elif dim == 'mhitem':
            self._hmeta = self._hmeta.chunk({'mhitem': -1})
        elif dim == 'mritem':
            self._rmeta = self._rmeta.chunk({'mritem': -1})
        else:
            raise ValueError('Invalid dimension name.')

    def chunk(self,**kwargs):
        if self._init_state and not self._at_hold:
            if len(kwargs)>0:
                raw_bkp = self._raw
                hmeta_bkp = self._hmeta
                rmeta_bkp = self._rmeta
                target_dims = [dim for dim in self.__valid_dimensions if dim in kwargs.keys()]
                target_vars = [var for var in self.__valid_variables if var in kwargs.keys()]
                try:
                    if self._chunked:
                        for dim in target_dims:
                            self.__unchunk_by_dim(dim)
                        for var in target_vars:
                            self.__unchunk_by_var(var)
                    for dim in target_dims:
                        self.__chunk_by_dim(dim,kwargs[dim])
                    for var in target_vars:
                        self.__chunk_by_var(var,kwargs[var])
                    self._chunked = True
                except Exception as e:
                    self._raw = raw_bkp
                    self._hmeta = hmeta_bkp
                    self._rmeta = rmeta_bkp
                    raise e
            else:
                for var in self.__valid_variables:
                    self.__chunk_by_var(var,None)
                self._chunked = True
        else:
            raise RuntimeError('Basefile is closed or at hold')

    def unchunk(self,vars=None,dims=None):
        if self._init_state and not self._at_hold:
            if self._chunked:
                if dims is not None:
                    target_dims = [dim for dim in self.__valid_dimensions if dim in dims]
                    for dim in target_dims:
                        self.__unchunk_by_dim(dim)
                    if len(target_dims) == len(self.__valid_dimensions):
                        self._chunked = False
                if vars is not None:
                    target_vars = [var for var in self.__valid_variables if var in vars]
                    for var in target_vars:
                        self.__unchunk_by_var(var)
                    if len(target_vars) == len(self.__valid_variables):
                        self._chunked = False
                if dims is None and vars is None:
                    self._raw = self._basefile_xr['raw']
                    self._rmeta = self._basefile_xr['rmeta']
                    self._hmeta = self._basefile_xr['hmeta']
                    self._chunked = False
            else:
                raise RuntimeError('Data is already unchunked.')
        else:
            raise RuntimeError('Basefile is closed or at hold')

    def _hold_basefile(self):
        self._at_hold = True
        self._basefile_xr.close()

    def _release_basefile(self):
        self._at_hold = False
        self._basefile_xr = xr.open_dataset(self._basefile_netcdf_fp,engine='h5netcdf')

    @classmethod
    def _split_by_difficulty_chunks(cls, rep_stats, kmer_sizes, io_chunksize, exec_chunksize, empc_cutoff, nworkers,pre_excluded_rids=None):
        empc_mid_cut = empc_cutoff/2
        rep_stats_amb = rep_stats[rep_stats['tab'] > 1]
        empc_factor_coefficients = [0.23, 0.2, 0.23, 0.34]
        repa_empc_factors = rep_stats_amb[cls.EMPC_COEFFICIENTS]

        # formula is empc = (e^ksize)*(0.23*tab + 0.2*complexity + 0.23*amb_mean + 0.34*amb_rep_mean)
        repa_empc = (repa_empc_factors.mul(empc_factor_coefficients, axis=1).sum(axis=1) * exp(mean(kmer_sizes))).div(rep_stats_amb['length'])
        if pre_excluded_rids is None:
            excluded_reps = repa_empc[repa_empc > empc_cutoff].index
        else:
            tmp_excluded_reps = repa_empc[repa_empc > empc_cutoff].index
            excluded_reps =tmp_excluded_reps.append(pd.Index(pre_excluded_rids)).drop_duplicates()
        repa_empc_filtered = repa_empc[~repa_empc.index.isin(excluded_reps)]

        reps_stats_filtered = rep_stats.loc[~rep_stats.index.isin(excluded_reps),:]
        d_lvl_easy_rids = reps_stats_filtered[reps_stats_filtered['tab'] <= 1].index.values
        d_lvl_intermediate_rids = repa_empc_filtered[(repa_empc_filtered > 0) & (repa_empc_filtered < empc_mid_cut)].index.values
        d_lvl_hard_rids = repa_empc_filtered[(repa_empc_filtered > empc_mid_cut) & (repa_empc_filtered < empc_cutoff)].index.values

        reps_by_difficulty_tuples = ((*adjust_chunksize(io_chunksize, exec_chunksize, 1, len(d_lvl_easy_rids), nworkers), d_lvl_easy_rids, 1),
                                     (*adjust_chunksize(io_chunksize, exec_chunksize, 2, len(d_lvl_intermediate_rids), nworkers), d_lvl_intermediate_rids, 2),
                                     (*adjust_chunksize(io_chunksize, exec_chunksize, 3, len(d_lvl_hard_rids), nworkers), d_lvl_hard_rids, 3))

        return rep_stats.index[~rep_stats.index.isin(excluded_reps)].values, excluded_reps.values, reps_by_difficulty_tuples

    def get_hmers_by_ksize(self,kmer_sizes):
        if self._init_state and not self._at_hold:
            if isinstance(kmer_sizes,int):
                target_ksizes = np.asarray([kmer_sizes])
            else:
                target_ksizes = np.asarray(kmer_sizes)
            if np.isin(target_ksizes,self._kmer_sizes).all():
                ref_ksize_array = np.asarray(self._kmer_sizes)
                ref_ksize_array.sort()
                min_kmer = target_ksizes.min()
                max_kmer = target_ksizes.max()
                min_kmer_pos = np.where(ref_ksize_array == min_kmer)[0]
                kmer_prior_pos = min_kmer_pos - 1
                right_flank_max = 2 ** (2 * max_kmer + 1) - 1
                if kmer_prior_pos>=0:
                    kmer_prior = ref_ksize_array[kmer_prior_pos][0]
                    left_flank_max = 2 ** (2 * kmer_prior + 1) - 1
                else:
                    left_flank_max = 0
                return self._index_hmer[(self._index_hmer > left_flank_max) & (self._index_hmer <= right_flank_max)]
            else:
                raise ValueError('Invalid `kmer_sizes` is provided.')
        else:
            raise RuntimeError('Basefile is closed or at hold')

    def _extract_raw_fwd_prm(self,fwd_lbl):
        def mark_kmers(hmeta, rmeta):
            cmpr = lambda a, b: (a.T >= b).any(1)
            return xr.apply_ufunc(cmpr, hmeta.sel(mhitem='fp'), rmeta,
                                  dask='allowed',
                                  output_dtypes=['b'],
                                  exclude_dims=set(("rid",)),
                                  input_core_dims=[['rid', 'hmer'], ['rid']],
                                  output_core_dims=[['hmer']])

        prm_fwd_v_lbl = add_primer_prefix(fwd_lbl, 'valid')
        prm_fwd_s_lbl = add_primer_prefix(fwd_lbl, 'state')
        prm_fwd_fp_lbl = add_primer_prefix(fwd_lbl, 'first-pos')

        xrid_prm_fwd_vs_mask = (self.rmeta.loc[:, ['valid', prm_fwd_v_lbl, prm_fwd_s_lbl]] == 1).all(dim='mritem').compute()
        if xrid_prm_fwd_vs_mask.sum() > 0:
            rmeta_tsub = self.rmeta.loc[:, prm_fwd_fp_lbl].where(xrid_prm_fwd_vs_mask, 9999).drop('mritem').load()
            xhmer_prm_fwd_s_msk = mark_kmers(self.hmeta, rmeta_tsub).compute()
            return xr.where(xhmer_prm_fwd_s_msk, self.raw[xrid_prm_fwd_vs_mask], False)
        else:
            return xr.DataArray(name='raw',coords={'rid':np.array([],dtype=self.raw.coords['rid'].dtype),'hmer':np.array([],dtype='u8')}, dims=['rid', 'hmer']).astype('b')

    def _extract_raw_rev_prm(self,rev_lbl):

        prm_rev_v_lbl = add_primer_prefix(rev_lbl, 'valid')
        prm_rev_s_lbl = add_primer_prefix(rev_lbl, 'state')
        prm_rev_fp_lbl = add_primer_prefix(rev_lbl, 'first-pos')

        xrid_prm_rev_vs_mask = (self.rmeta.loc[:, ['valid', prm_rev_v_lbl, prm_rev_s_lbl]] == 1).all(dim='mritem')

        hmeta_prm_rev_s_2d_msk = (self.hmeta[xrid_prm_rev_vs_mask].sel(dict(mhitem='lp')) < self.rmeta.loc[xrid_prm_rev_vs_mask, prm_rev_fp_lbl])
        xhmer_prm_rev_s_msk = hmeta_prm_rev_s_2d_msk.any(dim='rid')
        xrid_prm_rev_s_msk = hmeta_prm_rev_s_2d_msk.any(dim='hmer')

        raw_prm_s_msk = (xrid_prm_rev_s_msk & xhmer_prm_rev_s_msk)

        raw_prm_s_msk = raw_prm_s_msk.drop([coord for coord in raw_prm_s_msk.coords.keys() if coord not in raw_prm_s_msk.dims])

        if raw_prm_s_msk.shape[0] > 0:
            return xr.where(raw_prm_s_msk, self.raw[xrid_prm_rev_vs_mask], 0)
        else:
            return xr.DataArray(name='raw',coords={'rid':np.array([],dtype=self.raw.coords['rid'].dtype),'hmer':np.array([],dtype='u8')}, dims=['rid', 'hmer']).astype('b')

    def _extract_raw_bid_prm(self,fwd_lbl, rev_lbl):
        prm_fwd_v_lbl = add_primer_prefix(fwd_lbl, 'valid')
        prm_rev_v_lbl = add_primer_prefix(rev_lbl, 'valid')
        prm_fwd_s_lbl = add_primer_prefix(fwd_lbl, 'state')
        prm_rev_s_lbl = add_primer_prefix(rev_lbl, 'state')
        prm_fwd_fp_lbl = add_primer_prefix(fwd_lbl, 'first-pos')
        prm_rev_fp_lbl = add_primer_prefix(rev_lbl, 'first-pos')

        xrid_prm_fwd_vs_mask = (self.rmeta.loc[:, ['valid', prm_fwd_v_lbl, prm_fwd_s_lbl]] == 1).all(dim='mritem')
        xrid_prm_rev_vs_mask = (self.rmeta.loc[:, ['valid', prm_rev_v_lbl, prm_rev_s_lbl]] == 1).all(dim='mritem')

        xrid_prm_bid_vs_mask = (xrid_prm_fwd_vs_mask & xrid_prm_rev_vs_mask)

        hmeta_prm_fwd_s_2d_msk = (self.hmeta[xrid_prm_bid_vs_mask].sel(dict(mhitem='fp')) > self.rmeta.loc[xrid_prm_fwd_vs_mask, prm_fwd_fp_lbl])
        hmeta_prm_rev_s_2d_msk = (self.hmeta[xrid_prm_bid_vs_mask].sel(dict(mhitem='lp')) < self.rmeta.loc[xrid_prm_rev_vs_mask, prm_rev_fp_lbl])

        xhmer_prm_fwd_s_msk = hmeta_prm_fwd_s_2d_msk.any(dim='rid')
        xrid_prm_fwd_s_msk = hmeta_prm_fwd_s_2d_msk.any(dim='hmer')
        xhmer_prm_rev_s_msk = hmeta_prm_rev_s_2d_msk.any(dim='rid')
        xrid_prm_rev_s_msk = hmeta_prm_rev_s_2d_msk.any(dim='hmer')

        raw_prm_s_msk = (xrid_prm_fwd_s_msk & xhmer_prm_fwd_s_msk) & (xrid_prm_rev_s_msk & xhmer_prm_rev_s_msk)
        raw_prm_s_msk = raw_prm_s_msk.drop([coord for coord in raw_prm_s_msk.coords.keys() if coord not in raw_prm_s_msk.dims])
        if raw_prm_s_msk.shape[0] > 0:
            return xr.where(raw_prm_s_msk, self.raw[xrid_prm_bid_vs_mask], 0)
        else:
            return xr.DataArray(name='raw',coords={'rid':np.array([],dtype=self.raw.coords['rid'].dtype),'hmer':np.array([],dtype='u8')}, dims=['rid', 'hmer']).astype('b')

    def __verify_primer_label(self,primer_label):
        if add_primer_prefix(primer_label, 'valid') in self.xmritem:
            return True
        else:
            return False

    def extract_raw_by_primer(self,forward_primer,reverse_primer=None):
        if (forward_primer is not None) and (reverse_primer is None):
            if self.__verify_primer_label(forward_primer):
                return self._extract_raw_fwd_prm(forward_primer)
            else:
                raise ValueError('`forward_primer` was not found.')
        elif (forward_primer is None) and (reverse_primer is not None):
            if self.__verify_primer_label(reverse_primer):
                return self._extract_raw_rev_prm(reverse_primer)
            else:
                raise ValueError('`reverse_primer` was not found.')
        elif (forward_primer is not None) and (reverse_primer is not None):
            if self.__verify_primer_label(forward_primer) and self.__verify_primer_label(reverse_primer):
                return self._extract_raw_bid_prm(forward_primer,reverse_primer)
            else:
                raise ValueError('`forward_primer` or/and `reverse_primer` was not found.')
        else:
            raise ValueError('Invalid operation. No primer was provided.')

    @abstractmethod
    def _refine_by_primer(self,*args, **kwargs):
        pass

    def refine(self, method, *args, **kwargs):
        if self._init_state and not self._at_hold:
            if method == 'primer':
                return self._refine_by_primer(*args, **kwargs)
            else:
                raise ValueError('Unrecognized method is requested.')
        else:
            raise RuntimeError('Basefile is closed or at hold')

    @property
    def basefile_fp(self):
        return self._basefile_netcdf_fp

    @property
    def xr(self):
        if not self._at_hold:
            return self._basefile_xr
        else:
            RuntimeError('Basefile is at hold.')

    @property
    def raw(self):
        if not self._at_hold:
            if self._chunked:
                return self._raw
            else:
                return self._basefile_xr['raw']
        else:
            RuntimeError('Basefile is at hold.')

    @property
    def rmeta(self):
        if self._init_state and not self._at_hold:
            if self._chunked:
                return self._rmeta
            else:
                return self._basefile_xr['rmeta']
        else:
            raise RuntimeError('Basefile is closed or at hold.')

    @property
    def hmeta(self):
        if self._init_state and not self._at_hold:
            if self._chunked:
                return self._hmeta
            else:
                return self._basefile_xr['hmeta']
        else:
            raise RuntimeError('Basefile is closed or at hold.')

    @property
    def xhmer(self):
        return self._index_hmer

    @property
    def xrid(self):
        return self._index_rid

    @property
    def xmritem(self):
        return self._index_mritem

    @property
    def xmhitem(self):
        return self._index_mhitem

    @property
    def passed_rids(self):
        return self._valid_rids

    @property
    def excluded_rids(self):
        return self._invalid_rids

    @property
    def state(self):
        return (self._init_state and (not self._at_hold))

    @property
    def chunked(self):
        return self._chunked

    @property
    def kmer_sizes(self):
        return self._kmer_sizes

    @property
    def compression(self):
        return self._compression

    @property
    def cache_root_dir(self):
        return self._cache_root_dir

    @property
    def cache_dir(self):
        return self._cache_dir

    @property
    def run_chunksize(self):
        return self._run_chunksize

    @run_chunksize.setter
    def run_chunksize(self, value):
        if self._verify_chunksize(value, self._io_chunksize, self._exec_chunksize):
            self._run_chunksize = value
        else:
            raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')

    @property
    def io_chunksize(self):
        return self._io_chunksize

    @io_chunksize.setter
    def io_chunksize(self, value):
        if self._verify_chunksize(self._run_chunksize, value, self._exec_chunksize):
            self._io_chunksize = value
        else:
            raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')

    @property
    def exec_chunksize(self):
        return self._exec_chunksize

    @exec_chunksize.setter
    def exec_chunksize(self, value):
        if self._verify_chunksize(self._run_chunksize, self._io_chunksize, value):
            self.chunksize_exec = value
        else:
            raise ValueError('Chunk parameters are invalid. Follow the rule `run_chunksize` > `io_chunksize` > `exec_chunksize`.')

    @property
    def nworkers(self):
        return self._nworkers

    @nworkers.setter
    def nworkers(self, value):
        self._nworkers = value
