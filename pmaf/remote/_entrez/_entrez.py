from ._base import EntrezBase
from typing import Optional, Union

# TODO: This class was coded during early PhyloMAF development days, therefore it should be completely revised.


class Entrez(EntrezBase):
    """Remote class responsible for batch data fetching from :term:`NCBI`'s
    Entrez :term:`API` :cite:t:`schuler10EntrezMolecular1996`"""

    def __init__(
        self, email: str, api_key: Optional[str] = None, tool: str = "PhyloMAF"
    ):
        """Create Entrez instance to connect to :term:`NCBI` database.

        Parameters
        ----------
        email
            User's email that will be passed to :term:`NCBI` server
        api_key
            User's :term:`API` key obtained from :term:`NCBI` account page.
            Default is None(without key). However, it is recommended to obtain
            an :term:`API` key for faster access.
        tool
            Label of the tool that will be passed to :term:`NCBI` server. Default is "PhyloMAF"`
        """
        super().__init__(email, api_key, tool)

    def get_taxid_by_query(self, query: str) -> Union[bool, str]:
        """Fetch :term:`NCBI` taxonomy database using `query` and get a
        :term:`NCBI`'s internal :term:`taxid`.

        Parameters
        ----------
        query
            Query string to search for


        Returns
        -------
            False if fail or :term:`taxid`
        """
        ret = False
        raw_data = self._request_taxid_by_query(query)
        if raw_data:
            taxid = self._get_top_taxid(raw_data)
            ret = taxid
        return ret

    def get_genome_id_by_taxid(self, taxid: str) -> Union[bool, str]:
        """Get :term:`NCBI`'s genome ID by target :term:`taxid`

        Parameters
        ----------
        taxid
            Target :term:`taxid` to look for

        Returns
        -------
            False if fails or genome ID.
        """
        ret = False
        raw_data = self._request_genomes_by_taxid(taxid)
        if raw_data:
            genome_id = self._get_top_genome_id(raw_data)
            ret = genome_id
        return ret

    def get_chromosome_id_by_genome_id(self, genome_id: str) -> Union[bool, str]:
        """Get :term:`NCBI`'s chromosome ID by target `genome_id`

        Parameters
        ----------
        genome_id
            Target genome ID to look for


        Returns
        -------
            False if fails or chromosome ID
        """
        ret = False
        raw_data = self._request_chromosomes_by_genome_id(genome_id)
        if raw_data:
            chromosome_id = self._get_top_chromosome_id(raw_data)
            ret = chromosome_id
        return ret

    def get_gene_features_by_chromosome_id(
        self, chromosome_id: str, gene: str = "rRNA"
    ) -> Union[bool, list]:
        """Get gene features by chromosome ID.

        Parameters
        ----------
        chromosome_id
            Target :term:`NCBI` chromosome ID
        gene
            Target gene type. Default is "rRNA".
            Disclaimer: method was not tested for other gene types.

        Returns
        -------
            False if failed or string with extracted gene features from :term:`NCBI`'s feature table.
        """
        ret = False
        raw_io = self._request_sequence_feature_table_by_acc_id(chromosome_id, True)
        if raw_io:
            gene_features = self.filter_genes_from_future_table(raw_io, gene)
            raw_io.close()
            ret = gene_features
        return ret

    def get_fasta_sequence_by_param(
        self,
        accession_id: str,
        start_pos: Union[str, int],
        stop_pos: Union[str, int],
        strand: Union[str, int],
    ) -> str:
        """Get FASTA string from :term:`NCBI` database by `accesion_id`

        Parameters
        ----------
        accession_id
            Accession number of the "Nucleotide" database of :term:`NCBI`.
        start_pos
            Start position of sequence to crop
        stop_pos
            Stop position of the sequence to crop
        strand
            Strand of the sequence. Can be either "1" or "2".
            For more details check :term:`NCBI` documentation.

        Returns
        -------
            String with sequnce in FASTA format.
        """
        ret = False
        if strand in ["1", "2"]:
            ret = self._request_sequence_fasta(
                accession_id, start_pos, stop_pos, strand
            )
        return ret
