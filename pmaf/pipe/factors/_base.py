from pmaf.pipe.factors._metakit import FactorBackboneMetabase


class FactorBase(FactorBackboneMetabase):
    """ """

    def __repr__(self):
        class_name = self.__class__.__name__
        repr_str = "<{}:, Factors:[{}], Externals:[{}]>".format(
            class_name, len(self.factors), len(self.externals)
        )
        return repr_str
