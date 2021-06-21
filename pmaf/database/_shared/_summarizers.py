import pandas as pd
from pmaf.internal._constants import MAIN_RANKS, ITS
from pmaf.internal._shared import get_rank_upto, generate_lineages_from_taxa

def recap_taxonomy_sheet(master_taxonomy_sheet):
    """

    Parameters
    ----------
    master_taxonomy_sheet :
        

    Returns
    -------

    """
    database_summary = {}

    master_taxonomy_sheet.loc[:, MAIN_RANKS] = master_taxonomy_sheet.loc[:, MAIN_RANKS].applymap(lambda x: None if (x == '') else x)
    avail_ranks = [rank for rank in MAIN_RANKS if master_taxonomy_sheet.loc[:, rank].notna().any()]
    master_taxonomy_sheet.loc[:, 'lineage'] = generate_lineages_from_taxa(master_taxonomy_sheet, True, avail_ranks, False)

    total_taxa = master_taxonomy_sheet.shape[0]
    database_summary.update({'total-taxa': str(total_taxa)})

    total_duplicated_taxa = master_taxonomy_sheet[master_taxonomy_sheet.duplicated(subset=['lineage'], keep=False)].drop_duplicates(subset=['lineage']).reset_index(drop=True).shape[0]
    database_summary.update({'total-duplicated-taxa': str(total_duplicated_taxa)})

    total_unduplicated_taxa = master_taxonomy_sheet.drop_duplicates(subset=['lineage']).reset_index(drop=True).shape[0]
    database_summary.update({'total-unduplicated-taxa': str(total_unduplicated_taxa)})

    total_unique_taxa = master_taxonomy_sheet[~master_taxonomy_sheet.duplicated(subset=['lineage'], keep=False)].shape[0]
    database_summary.update({'total-unique-taxa': str(total_unique_taxa)})

    def summarize_for_rank(rank):
        """

        Parameters
        ----------
        rank :
            

        Returns
        -------

        """
        if rank in avail_ranks:
            total = master_taxonomy_sheet[master_taxonomy_sheet[rank].notna()][rank]
            duplicated = total.duplicated(keep=False)
            unique = total[~duplicated].dropna()
            count_shared = 0
            if rank in avail_ranks:
                prior_ranks = get_rank_upto(avail_ranks, rank)
                if prior_ranks:
                    filter_dup = master_taxonomy_sheet[master_taxonomy_sheet.duplicated(subset=[rank], keep=False)].dropna(subset=[rank])[avail_ranks].drop_duplicates(subset=prior_ranks)
                    count_shared = filter_dup[filter_dup.duplicated(subset=rank, keep=False)].reset_index(drop=True).shape[0]
            count_total = total.shape[0]
            count_duplicated = sum(duplicated)
            count_unique = unique.shape[0]

            return {'total': str(count_total), 'duplicated': str(count_duplicated), 'unique': str(count_unique), 'internal-with-other-taxa': str(count_shared)}
        else:
            return {'total': str(0), 'duplicated': str(0), 'unique': str(0), 'internal-with-other-taxa': str(0)}

    for rank in MAIN_RANKS:
        rank_name_full = ITS['r2rank'][rank]
        summary = summarize_for_rank(rank)
        database_summary.update({'{}-total'.format(rank_name_full): summary['total']})
        database_summary.update({'{}-duplicated'.format(rank_name_full): summary['duplicated']})
        database_summary.update({'{}-unique'.format(rank_name_full): summary['unique']})
        database_summary.update({'{}-internal'.format(rank_name_full): summary['internal-with-other-taxa']})

    summary_series = pd.Series(database_summary).map(str)
    return summary_series

def recap_transformation(transformation_details):
    """

    Parameters
    ----------
    transformation_details :
        

    Returns
    -------

    """
    tmp_summary = pd.Series()
    tmp_summary['avail-ranks'] =  '|'.join(transformation_details['avail-ranks'])
    tmp_summary['discarded-taxa'] = '|'.join([str(rid) for rid in transformation_details['removed-rids'].values.tolist()])
    return tmp_summary

def recap_sequence_info(sequence_details={}, alignment_details={}):
    """

    Parameters
    ----------
    sequence_details :
        (Default value = {})
    alignment_details :
        (Default value = {})

    Returns
    -------

    """
    tmp_sequence_summary = pd.Series()
    tmp_sequence_summary['max-sequence-length'] = str(sequence_details['sequence']) if len(sequence_details)>0 else 'N/A'
    tmp_sequence_summary['min-sequence-length'] = str(sequence_details['min_sequence']) if len(sequence_details) > 0 else 'N/A'
    tmp_sequence_summary['max-alignment-length'] = str(alignment_details['sequence']) if len(alignment_details)>0 else 'N/A'
    tmp_sequence_summary['min-alignment-length'] = str(alignment_details['min_sequence']) if len(alignment_details) > 0 else 'N/A'
    return tmp_sequence_summary

def append_recaps(ref_recaps,new_recap_dict):
    """

    Parameters
    ----------
    ref_recaps :
        
    new_recap_dict :
        

    Returns
    -------

    """
    new_recaps = pd.Series(new_recap_dict)
    return ref_recaps.append(new_recaps)

def merge_recaps(*args):
    """

    Parameters
    ----------
    *args :
        

    Returns
    -------

    """
    tmp_summary = args[0]
    for summary_element in args[1:]:
        tmp_summary = tmp_summary.append(summary_element)
    return tmp_summary
