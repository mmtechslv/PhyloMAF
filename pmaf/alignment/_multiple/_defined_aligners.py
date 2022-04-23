from os import environ, path

from Bio.Align.Applications import ClustalwCommandline


def clustalw2_wrapper(in_tmp_file, out_tmp_file, param_dict={}, cmd_bin="clustalw2"):
    """

    Parameters
    ----------
    in_tmp_file :

    out_tmp_file :

    param_dict :
        (Default value = {})
    cmd_bin :
        (Default value = 'clustalw2')

    Returns
    -------

    """
    default_cmd = "clustalw2"
    output_format = "clustal"
    cmb_bin_adj = default_cmd if cmd_bin is None else cmd_bin
    in_tmp_file.file.seek(0)
    if len(param_dict) > 0:
        clustal_exec = ClustalwCommandline(
            cmb_bin_adj,
            infile=in_tmp_file.name,
            outfile=out_tmp_file.name,
            **param_dict
        )
    else:
        clustal_exec = ClustalwCommandline(
            cmb_bin_adj, infile=in_tmp_file.name, outfile=out_tmp_file.name
        )
    stdout, stderr = clustal_exec()
    out_tmp_file.file.seek(0)
    return stdout, stderr, output_format
