Glossary
========

.. glossary::
    
    tids
        New reference identifiers or unique Taxon identifiers

    rids
        Old reference identifiers or Redundant taxon identifiers
    
    subs
        Refer to any number of inherited subordinate taxa that make a single :term:`tid <tids>`

    hdf5
        Hierarchical Data Format 5. For details refer to `HDF5 <https://www.hdfgroup.org/solutions/hdf5/>`_
        
    MSA
        Multiple Sequence Alignment

    MRCA
        Most Recent Common Ancestor

    16S
        16S ribosomal RNA

    IUPAC
        International Union of Pure and Applied Chemistry

    rRNA
        ribosomal RNA

    NCBI
        National Center for Biotechnology Information

    API
        Application Programming Interface

    taxid
        Taxon identifier in :term:`NCBI` database

    spec
        In PhyloMAF "spec" refers to set of stepwise instructions(or specifications) that define a pipeline(or pipe)

    docker
        In PhyloMAF "docker" refer to any intermediate data instance that moves in or out pipe :term:`specs<spec>`

    mediator
        In PhyloMAF "mediator" refer to any class from :mod:`~pmaf.pipe.agents.mediators` module that is responsible for providing mediator interface for the client database.

    factor
        In PhyloMAF "factor" refer to any class from :mod:`~pmaf.pipe.factors` module that describe the type of data to be mined.
