import warnings
warnings.simplefilter('ignore', category=FutureWarning)
from skbio.sequence import DNA,RNA,Protein,Sequence

def sniff_mode(sequence_str):
    '''

    Args:
      sequence_str: 

    Returns:

    '''
    if isinstance(sequence_str,str):
        if len(sequence_str)>0:
            try:
                skbio_seq = DNA(sequence_str)
            except ValueError:
                skbio_seq = None
            except:
                raise
            if skbio_seq is None:
                try:
                    skbio_seq = RNA(sequence_str)
                except ValueError:
                    skbio_seq = None
                except:
                    raise
            return None if skbio_seq is None else type(skbio_seq)
        else:
            raise ValueError('`sequence_str` must have length greater than one.')
    else:
        raise TypeError('`sequence_str` must be string.')

def mode_as_skbio(mode):
    '''

    Args:
      mode: 

    Returns:

    '''
    ret = False
    if isinstance(mode,str):
        mode_str = mode.lower()
    else:
        mode_str = mode
    if mode_str == 'dna':
        ret = DNA
    elif mode_str == 'rna':
        ret = RNA
    elif mode_str == 'protein':
        ret = Protein
    elif mode_str == None:
        ret = Sequence
    else:
        ret = False
    return ret

def mode_as_str(mode_skbio):
    '''

    Args:
      mode_skbio: 

    Returns:

    '''
    ret = False
    if mode_skbio == DNA:
        ret = 'dna'
    elif mode_skbio == RNA:
        ret = 'rna'
    elif mode_skbio == Protein:
        ret = 'protein'
    elif mode_skbio == Sequence:
        ret = None
    else:
        ret = False
    return ret

def mode_is_nucleotide(mode):
    '''

    Args:
      mode: 

    Returns:

    '''
    ret = False
    if isinstance(mode,str):
        mode_str = mode.lower()
        if mode_str == 'dna' or mode_str == 'rna':
            ret = True
    elif mode == DNA or mode == RNA:
        ret = True
    return ret

def validate_seq_mode(mode_str):
    '''

    Args:
      mode_str: 

    Returns:

    '''
    ret = False
    mode_str = mode_str.lower()
    if mode_str == 'dna':
        ret = True
    elif mode_str == 'rna':
        ret = True
    elif mode_str == 'protein':
        ret = True
    return ret

def validate_seq_grammar(seq_str,mode_str):
    '''

    Args:
      seq_str: 
      mode_str: 

    Returns:

    '''
    return True