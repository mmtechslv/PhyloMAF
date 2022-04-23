from pmaf.pipe.agents.mediators._base import MediatorBase
from pmaf.database._metakit import DatabaseBackboneMetabase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase


class MediatorLocalBase(MediatorBase):
    """"""

    def __init__(self, database, **kwargs):
        if not isinstance(database, DatabaseBackboneMetabase):
            TypeError("`database` has invalid type.")
        super().__init__(_client=database, _configs=kwargs)

    def __repr__(self):
        class_name = self.__class__.__name__
        client_class_name = self.client.name if self.state else "N/A"
        state = "Active" if self.client.state == 1 else "Inactive"
        repr_str = "<{}:[{}], Client:[{}]>".format(class_name, state, client_class_name)
        return repr_str

    def verify_factor(self, factor):
        """Verify/validate compatibility of the current :term:`mediator` and
        :term:`factor`

        Parameters
        ----------
        factor
            Factor to validate

        Returns
        -------
            Validation result
        """
        if isinstance(factor, FactorBackboneMetabase):
            gene_type = factor.factors.get("gene-type", None) == "marker"
            molecule_type = (
                factor.factors.get("molecule-type", None)
                == self.client.summary["molecule-type"]
            ) or self.client.summary["molecule-type"] == "N/A"
            gene_name = (
                factor.factors.get("gene-name", None) in self.client.summary["gene"]
            ) or self.client.summary["gene"] == "N/A"
            gene_target = (
                factor.factors.get("gene-target", None)
                in self.client.summary["gene-target-region"]
            ) or self.client.summary["gene-target-region"] == "N/A"
            return all([gene_type, molecule_type, gene_name, gene_target])
        else:
            raise TypeError("`factor` has invalid type.")

    @property
    def state(self):
        """State of the mediator(client)"""
        return self.client.state == 1
