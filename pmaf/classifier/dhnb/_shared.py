from math import ceil
from os import sysconf

    

def adjust_chunksize(io_chunksize,exec_chunksize,empc_level,rid_size,nworkers):
    if rid_size < io_chunksize:
        if rid_size <= nworkers:
            adj_io_csz = rid_size
        else:
            adj_io_csz = ceil(rid_size/nworkers)
    else:
        adj_io_csz = io_chunksize
    if empc_level == 2:
        adj_exec_csz = ceil(exec_chunksize*0.8)
    elif empc_level == 3:
        adj_exec_csz = ceil(exec_chunksize * 0.4)
    else:
        adj_exec_csz = exec_chunksize
    return ceil(adj_io_csz/adj_exec_csz), adj_exec_csz

def add_primer_prefix(label,meta):
    if meta=='state':
        return "prm_state_{}".format(label)
    elif meta=='first-pos':
        return "prm_pos_first_{}".format(label)
    elif meta=='valid':
        return "prm_valid_{}".format(label)
    else:
        raise ValueError('Invalid `meta` value.')

def optimize_secondary_chunksize(run_chunksize, nworkers, max_ksize, max_seq_length, builder, limit_perc, process):
    max_record_nbytes = 8 + max_seq_length * 2 + 8 + 8
    total_hmers = 4 ** max_ksize
    base_mem_bytes = sysconf('SC_PAGE_SIZE') * sysconf('SC_PHYS_PAGES')
    mem_bytes = base_mem_bytes * 0.9  # 90% of total memory
    calc_mem_pf = lambda nbytes, mnbytes: ((nbytes / mnbytes) * 100)
    process_factor = nworkers if process else 1
    if builder:
        exp_factor = total_hmers
        builder_factor = 1
    else:
        if max_ksize >= 16:
            exp_factor = 4 ** (16)
        else:
            exp_factor = 4 ** (max_ksize)
        builder_factor = 0

    calc_io_nbytes = lambda chsz: chsz * process_factor * (max_record_nbytes + 8 * (exp_factor * (8 + 2 * 4)) / (max_seq_length - max_ksize + 1) * 3 * builder_factor)
    calc_exec_nbytes = lambda chsz: chsz * ((exp_factor * (8 + 2 * 4)) / (max_seq_length - max_ksize + 1)) + exp_factor * (8 + 2 * 4) * builder_factor / chsz

    io_chunksize = run_chunksize
    while calc_mem_pf(calc_io_nbytes(io_chunksize), mem_bytes) >= limit_perc:
        io_chunksize = io_chunksize / 1.2
        if io_chunksize < 1:
            io_chunksize = 5
            break

    if (io_chunksize / run_chunksize) >= 0.25:
        io_chunksize = 1 + run_chunksize / nworkers

    adj_io_chunksize = round(io_chunksize)

    rem_mem_bytes = mem_bytes - calc_io_nbytes(adj_io_chunksize)
    exec_chunksize = adj_io_chunksize

    while calc_mem_pf(calc_exec_nbytes(exec_chunksize), rem_mem_bytes) >= limit_perc:
        exec_chunksize = exec_chunksize / 1.2
        if exec_chunksize < 1:
            exec_chunksize = 5
            break

    if (exec_chunksize / adj_io_chunksize) >= 0.25:
        exec_chunksize = 1 + adj_io_chunksize / 4

    adj_exec_chunksize = round(exec_chunksize)
    return adj_io_chunksize, adj_exec_chunksize

def calc_optimal_chunksize(dtype_size, exec_chunksize, id_dim, data_dim, var_dim, limit_perc):
    if (limit_perc > 1) and (limit_perc < 70):
        var_dim_fx = 1 if var_dim is None else var_dim
        mem_bytes = sysconf('SC_PAGE_SIZE') * sysconf('SC_PHYS_PAGES')
        calc_mem_pf = lambda nbytes: ((nbytes / mem_bytes) * 100)
        calc_io_nbytes = lambda id_chsz, data_chsz: id_chsz * data_chsz * var_dim_fx * dtype_size
        if (calc_mem_pf(calc_io_nbytes(id_dim, data_dim)) <= limit_perc):
            id_chunk = exec_chunksize*round((id_dim/2)/exec_chunksize)
            data_chunk = data_dim
        else:
            trial = 1
            total_trial = 0
            id_step = 10
            data_step = 2
            id_dim_chsz = exec_chunksize * id_step
            data_dim_chsz = data_dim / data_step
            while calc_mem_pf(calc_io_nbytes(id_dim_chsz, data_dim_chsz)) >= limit_perc:
                if (exec_chunksize * (trial * id_step)) <= id_dim:
                    id_dim_chsz = exec_chunksize * (trial * id_step)
                data_dim_chsz = data_dim / (trial * data_step)
                if trial == 10:
                    id_step = (id_step + 1) / 1.5
                    data_step = data_step * 1.5
                    trial = 1
                else:
                    trial = trial + 1
                if total_trial >= 100:
                    id_dim_chsz = exec_chunksize * 2
                    data_dim_chsz = data_dim / 2
                    break
                else:
                    total_trial = total_trial + 1
            id_chunk = round(id_dim_chsz)
            data_chunk = round(data_dim_chsz)
        if var_dim is None:
            return (id_chunk, data_chunk)
        else:
            return (id_chunk, data_chunk, var_dim_fx)
    else:
        raise ValueError('Invalid `limit_perc`. Value must be between 1% - 70%.')