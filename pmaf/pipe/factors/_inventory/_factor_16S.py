from pmaf.pipe.factors._base import FactorBase


class Factor16S(FactorBase):
    ''' '''
    def __init__(self,**kwargs):
        self.__externals = kwargs
        self.__factors = {'molecule-type': 'DNA', 'gene-type':'marker', 'gene-name':'rRNA', 'gene-target':'16S'}

    @property
    def externals(self):
        ''' '''
        return self.__externals

    @property
    def factors(self):
        ''' '''
        return self.__factors