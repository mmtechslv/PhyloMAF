from ._base import SpecificationCompositeBase
from pmaf.pipe.specs._metakit import SpecificationBackboneMetabase

def ForgeSpec(name,*inters):
    """

    Parameters
    ----------
    name :
        
    *inters :
        

    Returns
    -------

    """
    if isinstance(name,str):
        if not len(name)>0:
            raise ValueError('`name` is invalid.')
    else:
        raise TypeError('`name` has invalid type.')
    if not (issubclass(inters[0],SpecificationBackboneMetabase) and issubclass(inters[-1],SpecificationBackboneMetabase)):
        raise TypeError('`args` first and last objects must be specification.')
    if not all([callable(inter) for inter in inters]):
        raise TypeError('`args` contain object with invalid type.')

    # CHECK CORRECTES HERE NOT DOWN THERE
    # USE WRAPPER TO FIX INTER CALLABLES. Input args and kwargs and same outputs are can be imporoived from custom user functions

    def __init__(self,*args,**kwargs):
        tmp_specs = []
        tmp_steps = []
        last_outlet = None
        for inter in inters:
            if isinstance(inter,type):
                if issubclass(inter,SpecificationBackboneMetabase):
                    tmp_spec = inter(*args,**kwargs)
                    tmp_specs.append(tmp_spec)
                    tmp_steps.extend(tmp_spec.steps)
                    last_outlet = tmp_spec.steps[-1][2]
                else:
                    raise RuntimeError('Forged specification is incorrect.')
            else:
                tmp_steps.append((inter.__name__,inter,last_outlet,str(inter)))
        SpecificationCompositeBase.__init__(self,_specs=tmp_specs, _steps=tmp_steps)

    return type(name, (SpecificationCompositeBase,), {'__init__':__init__})