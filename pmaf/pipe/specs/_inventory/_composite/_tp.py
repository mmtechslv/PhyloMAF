from ._base import  SpecificationCompositeBase
from pmaf.pipe.specs._inventory._primitive._ti import SpecTI
from pmaf.pipe.specs._inventory._primitive._ip import SpecIP

class SpecTP(SpecificationCompositeBase):
    ''' '''
    def __init__(self, *args, **kwargs):
        tmp_specs = [SpecTI(*args, **kwargs), SpecIP(*args, **kwargs)]
        tmp_steps = [step for spec in tmp_specs for step in spec.steps]
        super().__init__(_specs=tmp_specs,_steps=tmp_steps)