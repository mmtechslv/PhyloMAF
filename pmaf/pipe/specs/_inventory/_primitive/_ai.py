from ._base import SpecificationPrimitiveBase
from pmaf.pipe.agents.mediators._metakit import MediatorAccessionMetabase
from pmaf.pipe.factors._metakit import FactorBackboneMetabase
from pmaf.pipe.agents.miners._miner import Miner
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._acs_medium import DockerAccessionMedium
from pmaf.pipe.agents.dockers._metakit import DockerBackboneMetabase


class SpecAI(SpecificationPrimitiveBase):
    """Accessions -> Identifiers ."""

    def __init__(self, mediator, factor, **kwargs):
        if not isinstance(mediator, MediatorAccessionMetabase):
            raise TypeError("`mediator` must be instance of MediatorAccessionMetabase.")
        if isinstance(factor, FactorBackboneMetabase):
            if not mediator.verify_factor(factor):
                raise ValueError("`factor` is not supported by database.")
        else:
            raise TypeError("`factor` has invalid type.")
        tmp_miner = Miner(mediator=mediator, factor=factor, **kwargs)
        tmp_steps = self.__define_lazy_steps()
        super().__init__(_steps=tmp_steps, _miner=tmp_miner)

    def __define_lazy_steps(self):
        steps_dict = [
            (
                "verify-input",
                self.__checkpoint_verify_input,
                DockerAccessionMedium,
                "Verify Input.",
            ),
            (
                "accession-to-identifier",
                self.__checkpoint_accession_to_identifier,
                DockerIdentifierMedium,
                "Retrieve identifiers by accessions .",
            ),
        ]
        return steps_dict

    def __checkpoint_verify_input(self, input, *args, **kwargs):
        if not isinstance(input, DockerBackboneMetabase):
            tmp_docker = DockerAccessionMedium(input, **kwargs)
        else:
            tmp_docker = input
        if self.miner.verify_docker(tmp_docker):
            return tmp_docker, args, kwargs
        else:
            raise ValueError("`docker` is not supported by current specification.")

    def __checkpoint_accession_to_identifier(self, docker, *args, **kwargs):
        identifiers = next(self.miner.yield_identifier_by_accession(docker, **kwargs))
        return identifiers, args, kwargs

    @property
    def inlet(self):
        """:class:`.DockerIdentifierMedium`"""
        return DockerAccessionMedium

    @property
    def outlet(self):
        """:class:`.DockerAccessionMedium`"""
        return DockerIdentifierMedium
