from ._base import MinerBase
from pmaf.pipe.agents.mediators._metakit import (
    MediatorAccessionMetabase,
    MediatorTaxonomyMetabase,
    MediatorSequenceMetabase,
    MediatorPhylogenyMetabase,
)
from pmaf.pipe.agents.dockers._metakit import (
    DockerAccessionMetabase,
    DockerIdentifierMetabase,
    DockerPhylogenyMetabase,
    DockerTaxonomyMetabase,
    DockerSequenceMetabase,
)
from pmaf.pipe.agents.dockers._mediums._id_medium import DockerIdentifierMedium
from pmaf.pipe.agents.dockers._mediums._acs_medium import DockerAccessionMedium
from pmaf.pipe.agents.dockers._mediums._phy_medium import DockerPhylogenyMedium
from pmaf.pipe.agents.dockers._mediums._seq_medium import DockerSequenceMedium
from pmaf.pipe.agents.dockers._mediums._tax_medium import DockerTaxonomyMedium
from collections import defaultdict
from pmaf.internal._shared import chunk_generator
from typing import Any, Generator


class Miner(MinerBase):
    """Main class that perform data mining operations in :mod:`~pmaf.pipe`
    module."""

    def yield_taxonomy_by_identifier(
        self, docker: DockerIdentifierMedium, **kwargs: Any
    ) -> Generator[DockerTaxonomyMedium, None, None]:
        """Yields the next taxonomy :term:`docker` from the given identifier
        parameter `docker`

        Parameters
        ----------
        docker
            The input identifier :term:`docker`
        kwargs
            Compatibility

        Yields
        ------
            Taxonomy :term:`docker`
        """
        if isinstance(docker, DockerIdentifierMetabase):
            if isinstance(self.mediator, MediatorTaxonomyMetabase):
                yield from self.__yield_taxonomy_by_identifier(docker, **kwargs)
            else:
                raise RuntimeError("`mediator` does not support such request.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def yield_phylogeny_by_identifier(
        self, docker: DockerIdentifierMedium, **kwargs: Any
    ) -> DockerPhylogenyMedium:
        """Yield the next phylogeny :term:`docker` from given identifier
        parameter `docker`

        Parameters
        ----------
        docker
            The input identifier :term:`docker`
        kwargs
            Compatibility


        Yields
        ------
            Phylogeny :term:`docker`
        """
        if isinstance(docker, DockerIdentifierMetabase):
            if isinstance(self.mediator, MediatorPhylogenyMetabase):
                yield from self.__yield_phylogeny_by_identifier(docker, **kwargs)
            else:
                raise RuntimeError("`mediator` does not support such request.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def yield_sequence_by_identifier(
        self, docker: DockerIdentifierMedium, **kwargs: Any
    ) -> DockerSequenceMedium:
        """Yield the next sequence :term:`docker` from given identifier
        parameter `docker`

        Parameters
        ----------
        docker
            The input identifier :term:`docker`
        kwargs
            Compatibility


        Yields
        ------
            Sequence :term:`docker`
        """
        if isinstance(docker, DockerIdentifierMetabase):
            if isinstance(self.mediator, MediatorSequenceMetabase):
                yield from self.__yield_sequence_by_identifier(docker, **kwargs)
            else:
                raise RuntimeError("`mediator` does not support such request.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def yield_identifier_by_accession(
        self, docker: DockerAccessionMedium, **kwargs: Any
    ) -> DockerIdentifierMedium:
        """Yield the next identifier :term:`docker` from given accessions
        parameter `docker`

        Parameters
        ----------
        docker
            The input accession :term:`docker`
        kwargs
            Compatibility


        Yields
        ------
            Identifier :term:`docker`
        """
        if isinstance(docker, DockerAccessionMetabase):
            if isinstance(self.mediator, MediatorAccessionMetabase):
                yield from self.__yield_identifier_by_accession(docker, **kwargs)
            else:
                raise RuntimeError("`mediator` does not support such request.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def yield_accession_by_identifier(
        self, docker: DockerIdentifierMedium, **kwargs: Any
    ) -> DockerAccessionMedium:
        """Yield the next accession :term:`docker` from given identifier
        parameter `docker`

        Parameters
        ----------
        docker
            The input identifier :term:`docker`
        kwargs
            Compatibility


        Yields
        ------
            Accession :term:`docker`
        """
        if isinstance(docker, DockerIdentifierMetabase):
            if isinstance(self.mediator, MediatorAccessionMetabase):
                yield from self.__yield_accession_by_identifier(docker, **kwargs)
            else:
                raise RuntimeError("`mediator` does not support such request.")
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def yield_identifier_by_docker(self, docker, **kwargs):
        """Yield the next identifier :term:`docker` from any given parameter
        `docker`. This method will automatically decide which result to produce
        depending on assigned :term:`mediator` instance.

        Parameters
        ----------
        docker
            The input :term:`docker`
        kwargs
            Compatibility


        Yields
        ------
            Any type of :term:`docker` depending on assigned :term:`mediator`
        """
        if self.verify_docker(docker):
            if isinstance(docker, DockerAccessionMetabase):
                yield from self.__yield_identifier_by_accession(docker, **kwargs)
            elif isinstance(docker, DockerPhylogenyMetabase):
                yield from self.__yield_identifier_by_phylogeny(docker, **kwargs)
            elif isinstance(docker, DockerTaxonomyMetabase):
                yield from self.__yield_identifier_by_taxonomy(docker, **kwargs)
            elif isinstance(docker, DockerSequenceMetabase):
                yield from self.__yield_identifier_by_sequence(docker, **kwargs)
            elif isinstance(docker, DockerIdentifierMetabase):
                yield from iter([docker])
            else:
                raise RuntimeError
        else:
            raise TypeError("`docker` must be instance of DockerIdentifierMetabase.")

    def __yield_accession_by_identifier(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_accession_by_identifier,
            docker,
            DockerAccessionMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_taxonomy_by_identifier(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_taxonomy_by_identifier,
            docker,
            DockerTaxonomyMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_sequence_by_identifier(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_sequence_by_identifier,
            docker,
            DockerSequenceMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_phylogeny_by_identifier(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_phylogeny_by_identifier,
            docker,
            DockerPhylogenyMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_identifier_by_accession(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_identifier_by_accession,
            docker,
            DockerIdentifierMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_identifier_by_taxonomy(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_identifier_by_taxonomy,
            docker,
            DockerIdentifierMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_identifier_by_sequence(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_identifier_by_sequence,
            docker,
            DockerIdentifierMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __yield_identifier_by_phylogeny(self, docker, chunksize=None, **kwargs):
        return self.__process_chunks_by_docker_for_method(
            self.mediator.get_identifier_by_phylogeny,
            docker,
            DockerIdentifierMedium,
            chunksize=chunksize,
            factor=self.factor,
            **kwargs
        )

    def __process_chunks_by_docker_for_method(
        self, method, docker, outlet, chunksize=None, **kwargs
    ):
        """Method to mine dockers in chunks."""
        if docker.singleton:
            return iter([method(docker, **kwargs)])
        else:
            if chunksize is not None:
                tmp_chunks_gen = chunk_generator(docker.get_iterator(), chunksize)
                tmp_docker_name = docker.name
                tmp_docker_metadata = docker.metadata
                tmp_docker_type = type(docker)
                tmp_outlet = outlet

                def chunk_products(**kwargs):
                    chunk_i = 0
                    for tmp_chunk in tmp_chunks_gen:
                        chunk_name = (
                            str(chunk_i)
                            if tmp_docker_name is None
                            else "{}-{}".format(tmp_docker_name, str(chunk_i))
                        )
                        tmp_chunk_dockers = {name: docker for name, docker in tmp_chunk}
                        tmp_docker_container = tmp_docker_type(
                            tmp_chunk_dockers,
                            name=chunk_name,
                            metadata=tmp_docker_metadata,
                        )
                        yield self.__process_recursive_by_docker_for_method(
                            method, tmp_docker_container, tmp_outlet, **kwargs
                        )
                        chunk_i += 1

                return chunk_products(**kwargs)
            else:
                return iter(
                    [
                        self.__process_recursive_by_docker_for_method(
                            method, docker, outlet, **kwargs
                        )
                    ]
                )

    def __process_recursive_by_docker_for_method(
        self, method, docker_container, outlet, **kwargs
    ):
        """Method to mine non-singleton dockers recursively."""

        def nested_parser(docker):
            if docker.singleton:
                return method(docker, **kwargs)
            else:
                product_dict = defaultdict(None)
                product_metadata = defaultdict(dict)
                for ix, sub_docker in docker.get_iterator():
                    tmp_parsed_docker = nested_parser(sub_docker)
                    product_dict[ix] = tmp_parsed_docker
                    product_metadata[ix] = tmp_parsed_docker.metadata
                new_metadata = {
                    "verbose": dict(product_metadata),
                    "master": docker.wrap_meta(),
                }
                return outlet(
                    product_dict,
                    name=docker.name,
                    metadata=new_metadata,
                    _transit=docker_container,
                )

        return nested_parser(docker_container)
