"""
Database Manager
----------------
Database Storage Manager

.. currentmodule:: pmaf.database

"""
import warnings

import pandas as pd
import tables
from os import path
import pickle
from collections import defaultdict
from pmaf.database._shared._common import *
from typing import Optional, Tuple, Union, Dict, Generator, Any
from pmaf.internal._typing import AnyGenericIdentifier


class DatabaseStorageManager:
    """Database :term:`hdf5` storage manager."""

    def __init__(self, hdf5_filepath: str, storage_name: str, force_new: bool = False):
        """Constructor for storage manager.

        Parameters
        ----------
        hdf5_filepath
            Path to :term:`hdf5` file
        storage_name
            Storage database name. Must match the one in storage file.
        force_new
            If file exists the override it for new construction
        """
        self._storer = None  # Current storer(pandas/pytables) handle
        self._storer_state = False  # Current storer state
        self._storer_mode = None  # Value can be either 1 for `tables` or 2 for `pandas`
        self._hdf5_filepath = None  # HDF5 filepath
        self._storage_name = None  # Storage database name
        self._init_state = 0  # Initiation state. 0 or False: Inactive; -1: Under construction; 1: Active for data retrieval.
        self._db_info_cache = (
            None  # Database cache for storage element "metadata-db-info"
        )
        self._db_summary = (
            None  # Database cache for storage element states. Stored as pd.Series
        )
        self._interxmap_cache = {
            "map-interx-taxon": None,
            "map-interx-repseq": None,
        }  # Cache for interxmap elements
        self._supplement_cache = defaultdict(None)  # Additional optional cache elements
        if isinstance(storage_name, str) and isinstance(hdf5_filepath, str):
            if len(storage_name) > 0 and len(hdf5_filepath) > 0:
                if not path.exists(hdf5_filepath) or force_new:
                    self._hdf5_filepath = hdf5_filepath
                    self._storage_name = storage_name
                    self.__build_storage()
                else:
                    if self.validate_storage(hdf5_filepath, storage_name):
                        self._hdf5_filepath = hdf5_filepath
                        self._storage_name = storage_name
                        self.__init_manager()
                    else:
                        raise ValueError("Storage file or storage name is invalid.")
            else:
                raise ValueError("Storage file or storage name is invalid.")
        else:
            raise ValueError("Storage file or storage name is invalid.")

    def __exit__(self, exc_type, exc_value, traceback):
        """Close storer when :class:`.DatabaseStorageManager` is deleted."""
        self._storer.close()

    def __init_manager(self):
        """This function initiates storage manager by making it active for
        working. It also loads metadata-db-info into memory which is required
        to let know other package _components about what kind of data is
        available in the storage file.

        Returns:
            Nothing but raises error if initiation was not success.
        """
        try:
            self._db_info_cache = pd.read_hdf(
                self._hdf5_filepath, DATABASE_HDF5_STRUCT["metadata-db-info"]
            )
            self._init_state = 1
            if not self.initiate_memory_cache():
                raise RuntimeError("Cannot initiate cache.")
        except TypeError:
            raise TypeError("Invalid _local file.")
        except:
            raise RuntimeError(
                "Failed to initiate manager. Reading HDF5 was not successful."
            )

        return

    def initiate_memory_cache(self, level: int = 1) -> bool:
        """Load various elements based on `level` from storage to the memory
        for rapid data access.

        Parameters
        ----------
        level
            Level of data caching.
            Levels:
            - Level 1: Only loads inter index map to the memory. # Run by default
            - Level 2: Additionally load taxonomy-sheet to the memory
            - Level 3: Additionally load all map-elements to the memory
            - Level 4: Additionally load all tree-instance to the memory

        Returns
        -------

            True level until which data was cached.
        """
        ret = False
        if self._init_state == 1:
            tmp_storer = pd.HDFStore(self._hdf5_filepath, mode="r")
            if level >= 1:
                if (
                    self._db_info_cache["map-interx-taxon"]
                    and self._db_info_cache["map-interx-repseq"]
                ):
                    self._interxmap_cache["map-interx-repseq"] = tmp_storer.select(
                        DATABASE_HDF5_STRUCT["map-interx-repseq"]
                    )
                    self._interxmap_cache["map-interx-taxon"] = tmp_storer.select(
                        DATABASE_HDF5_STRUCT["map-interx-taxon"]
                    )
                    self._db_summary = tmp_storer.select(
                        DATABASE_HDF5_STRUCT["metadata-db-summary"]
                    )
                    ret = 1
            if level >= 2:
                if self._db_info_cache["taxonomy-sheet"]:
                    self._supplement_cache["taxonomy-sheet"] = tmp_storer.select(
                        DATABASE_HDF5_STRUCT["taxonomy-sheet"]
                    )
                    ret = 2
            if level >= 3:
                for element_key in filter_elements_by(
                    "map-", ["map-interx-repseq", "map-interx-taxon"]
                ):
                    if self._db_info_cache[element_key]:
                        self._supplement_cache[element_key] = tmp_storer.select(
                            DATABASE_HDF5_STRUCT[element_key]
                        )
                        ret = 3
            tmp_storer.close()
            if level >= 4:
                if self._db_info_cache["tree-object"]:
                    tmp_storer = tmp_storer.get_handle_by_element("tree-object")
                    tree_object_bytes = tmp_storer.get_node(
                        DATABASE_HDF5_STRUCT["tree-object"]
                    ).read()[0]
                    self._supplement_cache["tree-object"] = tree_object_bytes
                    tmp_storer.close()
                    ret = 4
        return ret

    @staticmethod
    def validate_storage(hdf5_filepath: str, storage_name: str) -> bool:
        """Validates storage :term:`hdf5` file.

        Parameters
        ----------
        hdf5_filepath
            Path to :term:`hdf5` file
        storage_name
            Storage database name

        Returns
        -------

            Validation result
        """
        ret = False
        try:
            tmp_storer = tables.open_file(hdf5_filepath, mode="r")
            if tmp_storer.title == storage_name:
                title_list = []
                path_list = []
                for node in tmp_storer.walk_nodes():
                    if node._v_title != "":
                        title_list.append(node._v_title)
                        path_list.append(node._v_pathname)
                tmp_storer.close()
                title_verify = all(
                    [title in title_list[1:] for title in DATABASE_HDF5_STRUCT.keys()]
                )
                path_verify = all(
                    [path in path_list[1:] for path in DATABASE_HDF5_STRUCT.values()]
                )
                if title_verify and path_verify:
                    ret = True
            else:
                tmp_storer.close()
        except:
            raise RuntimeError("Error during validating storage file.")
        return ret

    def shutdown(self):
        """Shutdown the database and mark cache clean for garbage collector."""
        try:
            self.__close_storer()
            self._db_info_cache = None
            self._interxmap_cache = {
                "map-interx-taxon": None,
                "map-interx-repseq": None,
            }
            self._supplement_cache = defaultdict(None)
            self._db_summary = None
            self._storer_state = False
            self._storer = None
            self._init_state = 0
        except:
            raise RuntimeError("Error during closing _local.")
        return

    def __close_storer(self):
        """This method closes :meth:`.storer` and releases the storage file for
        reopening."""
        if self._storer_state:
            try:
                self._storer.close()  # Same function for both pandas and tables. Might change in the future.
            except:
                raise RuntimeError("Storer cannot be closed.")
            self._storer_state = False
        return

    def __open_as_tables(self, mode: str = "r"):
        """Open the storage :term:`hdf5` file using :mod:`tables`

        Parameters
        ----------
        mode
            Open file using mode
        """
        if self._init_state:
            self.__close_storer()
            try:
                self._storer = tables.open_file(self._hdf5_filepath, mode=mode)
            except:
                raise RuntimeError("Storage file cannot be opened properly.")
            self._storer_mode = 1
            self._storer_state = True
        else:
            raise RuntimeError("Storage manager must is not initiated.")
        return self._storer_state

    def __open_as_pandas(self, mode="r"):
        """Open the storage :term:`hdf5` file using :mod:`pandas`

        Parameters
        ----------
        mode
            Open file using mode
        """
        if self._init_state:
            self.__close_storer()
            try:
                self._storer = pd.HDFStore(self._hdf5_filepath, mode=mode)
            except:
                raise RuntimeError("Storage file cannot be opened properly.")
            self._storer_mode = 2
            self._storer_state = True
        else:
            raise RuntimeError("Storage manager must is not initiated.")
        return self._storer_state

    def __build_storage(self):
        """This method builds new storage element and generates its internal
        structure. It also fill necessary defaults to make working storage
        file.

        Returns:
            Nothing but will raise error if something goes wrong.
        """
        try:
            tmp_storer = tables.open_file(
                self._hdf5_filepath, mode="w", title=self._storage_name
            )

            tmp_storer.create_group("/", "tre", title="root-tree")
            tmp_storer.create_group("/tre", "master", title="tree-prior")
            tmp_storer.create_group("/tre", "parsed", title="tree-parsed")
            tmp_storer.create_group("/tre", "pickled", title="tree-object")
            tmp_storer.create_vlarray(
                "/tre/master", "value", title="bytes", atom=tables.VLUnicodeAtom()
            )
            tmp_storer.create_vlarray(
                "/tre/parsed", "value", title="bytes", atom=tables.VLUnicodeAtom()
            )
            tmp_storer.create_vlarray(
                "/tre/pickled", "value", title="bytes", atom=tables.ObjectAtom()
            )

            tmp_storer.create_group("/", "tax", title="root-taxonomy")
            tmp_storer.create_group("/tax", "master", title="taxonomy-prior")
            tmp_storer.create_group("/tax", "parsed", title="taxonomy-sheet")

            tmp_storer.create_group("/", "seq", title="root-sequence")
            tmp_storer.create_group("/seq", "reps", title="sequence-representative")
            tmp_storer.create_group("/seq", "algn", title="sequence-aligned")
            tmp_storer.create_group("/seq", "accs", title="sequence-accession")

            tmp_storer.create_group("/", "map", title="root-map")
            tmp_storer.create_group("/map", "interxtax", title="map-interx-taxon")
            tmp_storer.create_group("/map", "interxreps", title="map-interx-repseq")
            tmp_storer.create_group("/map", "reptid", title="map-rep2tid")
            tmp_storer.create_group("/map", "repseq", title="map-repseq")
            tmp_storer.create_group("/map", "tree", title="map-tree")

            tmp_storer.create_group("/", "stat", title="root-stats")
            tmp_storer.create_group("/stat", "reps", title="stat-reps")
            tmp_storer.create_group("/stat", "taxs", title="stat-taxs")

            tmp_storer.create_group("/", "meta", title="root-metadata")
            tmp_storer.create_group("/meta", "summary", title="metadata-db-summary")
            tmp_storer.create_group("/meta", "info", title="metadata-db-info")
            tmp_storer.create_group("/meta", "stamp", title="metadata-db-stamp")
            tmp_storer.create_group("/meta", "history", title="metadata-db-history")

            tmp_element_key_defaults = [
                "tree-parsed",
                "tree-prior",
                "tree-object",
                "taxonomy-prior",
                "taxonomy-sheet",
                "sequence-representative",
                "sequence-aligned",
                "sequence-accession",
                "metadata-db-summary",
                "metadata-db-stamp",
                "map-interx-taxon",
                "map-interx-repseq",
                "map-rep2tid",
                "map-repseq",
                "map-tree",
                "stat-reps",
                "stat-taxs",
            ]

            tmp_storer.close()

            tmp_storer = pd.HDFStore(self._hdf5_filepath, mode="a")

            tmp_element_defaults_series = pd.Series(False, tmp_element_key_defaults)
            tmp_storer.put(
                DATABASE_HDF5_STRUCT["metadata-db-info"],
                tmp_element_defaults_series,
                format="fixed",
            )
            tmp_storer.get_node(
                DATABASE_HDF5_STRUCT["metadata-db-info"]
            )._v_title = "metadata-db-info"

            tmp_storer.close()

            self._db_info_cache = pd.Series(False, tmp_element_key_defaults)
            self._init_state = -1
        except:
            raise RuntimeError("Error creating new HDF5 storage file.")
        return

    def commit_to_storage(self, element_key, product_generator):
        """This is a primary function that commit changes to the storage.

        Parameters
        ----------
        element_key
            element key to which product product must be put.
        product_generator
            Primary generator that yields output that can be put into storage element.
            All product generators and must follow following output rules.
            For `sequence-master` and `sequence-aligned` generator must first yield (`product_inits`, `product_generator_first_chunk`).
            Where `product_inits` contain data such as `expectedrows` or `min_itemsize`,
            which are required if product processes in chunks. Following yield must be `product_product_chunk`.
            For all others, generator must first yield `product_inits`, `None`. Following yield must be `product_product`
            Note: Not all product generators are processed same way. For more details, view product documentation.

        Returns
        -------

            Last result from generator if success. Otherwise RuntimeError is raised.
        """
        if self._init_state == -1:
            print("Starting to process [{}]".format(element_key))
            last_product = self.__put_to_storage(element_key, product_generator)
            if last_product is not None:
                self._db_info_cache.loc[element_key] = True
                print("Successfully committed [{}]".format(element_key))
            return last_product
        else:
            raise RuntimeError(
                "Data base was already stamped so it is not possible to commit again."
            )

    def __put_to_storage(self, element_key: str, product_generator: Generator) -> Any:
        """This is main function that performs actual commit to the storage.

        Parameters
        ----------
        element_key
            Storage element key to put data into
        product_generator
            Data generator that will be put into storage element

        Returns
        -------
            Return last product chunk that was put to storage.
        """
        ret = None
        try:
            if element_key in ["sequence-representative", "sequence-aligned"]:
                if self.__open_as_pandas("a"):
                    product_inits, product_generator_first_chunk = next(
                        product_generator
                    )
                    max_rows = product_inits.pop("max_rows")
                    self._storer.put(
                        DATABASE_HDF5_STRUCT[element_key],
                        product_generator_first_chunk,
                        format="table",
                        data_columns=True,
                        min_itemsize=product_inits,
                        index=False,
                    )
                    last_chunk = product_generator_first_chunk
                    for next_chunk in product_generator:
                        self._storer.append(
                            DATABASE_HDF5_STRUCT[element_key],
                            next_chunk,
                            format="table",
                            data_columns=True,
                            min_itemsize=product_inits,
                            expectedrows=max_rows,
                            index=False,
                        )
                        last_chunk = next_chunk
                    self._storer.get_node(
                        DATABASE_HDF5_STRUCT[element_key]
                    )._v_title = element_key
                    self._storer.create_table_index(
                        DATABASE_HDF5_STRUCT[element_key],
                        columns=["index"],
                        optlevel=9,
                        kind="full",
                    )
                    ret = last_chunk
            elif element_key in [
                "sequence-accession",
                "taxonomy-prior",
                "taxonomy-sheet",
                "metadata-db-summary",
                "map-rep2tid",
                "map-repseq",
                "metadata-db-history",
                "stat-reps",
                "stat-taxs",
            ]:
                if self.__open_as_pandas("a"):
                    product_inits, product_generator_first_chunk = next(
                        product_generator
                    )
                    if (product_inits is not None) and (
                        product_generator_first_chunk is not None
                    ):
                        max_rows = product_inits.pop("max_rows")
                        x_columns = product_inits.pop("index_columns")
                        min_itemsize = product_inits if len(product_inits) > 0 else None
                        self._storer.put(
                            DATABASE_HDF5_STRUCT[element_key],
                            product_generator_first_chunk,
                            format="table",
                            data_columns=True,
                            min_itemsize=min_itemsize,
                            index=False,
                        )
                        last_chunk = product_generator_first_chunk
                        for next_chunk in product_generator:
                            self._storer.append(
                                DATABASE_HDF5_STRUCT[element_key],
                                next_chunk,
                                format="table",
                                data_columns=True,
                                min_itemsize=min_itemsize,
                                expectedrows=max_rows,
                                index=False,
                            )
                            last_chunk = next_chunk
                        self._storer.get_node(
                            DATABASE_HDF5_STRUCT[element_key]
                        )._v_title = element_key
                        self._storer.create_table_index(
                            DATABASE_HDF5_STRUCT[element_key],
                            columns=x_columns,
                            optlevel=9,
                            kind="full",
                        )
                        ret = last_chunk
                    else:
                        product_product_whole = next(product_generator)
                        self._storer.put(
                            DATABASE_HDF5_STRUCT[element_key],
                            product_product_whole,
                            format="table",
                            data_columns=True,
                        )
                        self._storer.get_node(
                            DATABASE_HDF5_STRUCT[element_key]
                        )._v_title = element_key
                        ret = product_product_whole
            elif element_key in ["tree-prior", "tree-parsed"]:
                if self.__open_as_tables("a"):
                    _, _ = next(product_generator)
                    product_product_whole = next(product_generator)
                    product_product_whole_utf8 = product_product_whole.encode("utf-8")
                    self._storer.get_node(DATABASE_HDF5_STRUCT[element_key]).append(
                        product_product_whole_utf8
                    )
                    ret = product_product_whole
            elif element_key == "tree-object":
                if self.__open_as_tables("a"):
                    _, _ = next(product_generator)
                    product_product_whole = next(product_generator)
                    product_product_whole_bytes = pickle.dumps(product_product_whole)
                    self._storer.get_node(DATABASE_HDF5_STRUCT[element_key]).append(
                        product_product_whole_bytes
                    )
                    ret = product_product_whole
            elif element_key in ["map-interx-taxon", "map-interx-repseq", "map-tree"]:
                if self.__open_as_pandas("a"):
                    _, _ = next(product_generator)
                    product_product_whole = next(product_generator)
                    self._storer.put(
                        DATABASE_HDF5_STRUCT[element_key],
                        product_product_whole,
                        format="fixed",
                        data_columns=True,
                    )
                    self._storer.get_node(
                        DATABASE_HDF5_STRUCT[element_key]
                    )._v_title = element_key
                    ret = product_product_whole
        except:
            raise RuntimeError("Error while processing [{}]".format(element_key))
        return ret

    def imprint_database(self, stamp_dict: dict):
        """This is the final function that _local constructor must call. This
        function will add signature to the storage file and will lock it so
        that no changes can be performed. Locking is performed only stamp
        presence check via storage manager.

        Parameters
        ----------
        stamp_dict
            Stamp data to imprint into storage file.
        """
        if self._init_state == -1:
            if not (
                self._db_info_cache["map-interx-taxon"]
                and self._db_info_cache["map-interx-repseq"]
            ):
                raise ValueError(
                    "Cannot imprint _local without `map-interx-taxon` and `map-interx-repseq` elements."
                )

            if self.__open_as_tables("r"):
                title_list = []
                for node in self._storer.walk_nodes():
                    if (
                        node._v_title in DATABASE_HDF5_STRUCT.keys()
                        and not node._v_title.startswith("root-")
                    ):
                        if node._v_nchildren > 0:
                            if node._v_children.values()[0]._v_title == "bytes":
                                if node._v_children.values()[0].nrows > 0:
                                    title_list.append(node._v_title)
                            else:
                                title_list.append(node._v_title)
                if (
                    self._db_info_cache.index.isin(title_list).sum()
                    != self._db_info_cache.sum()
                ):
                    raise RuntimeError(
                        "Cannot imprint. Possible storage file corruption."
                    )
                self.__open_as_pandas("a")
                self._db_info_cache["metadata-db-stamp"] = True
                self._storer.put(
                    DATABASE_HDF5_STRUCT["metadata-db-info"],
                    self._db_info_cache,
                    format="fixed",
                )
                self._storer.get_node(
                    DATABASE_HDF5_STRUCT["metadata-db-info"]
                )._v_title = "metadata-db-info"

                self._storer.put(
                    DATABASE_HDF5_STRUCT["metadata-db-stamp"],
                    pd.Series(stamp_dict),
                    format="fixed",
                )
                self._storer.get_node(
                    DATABASE_HDF5_STRUCT["metadata-db-stamp"]
                )._v_title = "metadata-db-stamp"
        return

    def __set_handle_by_element(self, element_key: str):
        """Re-assign :attr:`.storer` handle based on `element_key`"""
        storer_mode = get_element_mode(element_key)
        if not ((storer_mode == self._storer_mode) and self._storer_state):
            if storer_mode == 2:
                self.__open_as_pandas()
            elif storer_mode == 1:
                self.__open_as_tables()
        return self._storer_state

    def __get_coordinates_for_element_by_ids(
        self, element_key: str, ids: AnyGenericIdentifier
    ) -> pd.Index:
        """Retrieve cached index coordianates for target `ids` and
        `element_key`

        Parameters
        ----------
        element_key
            Target storage element
        ids
            Target ids of storage element

        Returns
        -------
            :class:`~pandas.Index` with coordinates of target `ids` for target storage elementof target `ids` for target storage element
        """
        tmp_interxmap_type = get_element_index_type(element_key)
        if self._init_state == 1:
            valid_ids = self._interxmap_cache[tmp_interxmap_type].index.isin(ids)
            if valid_ids.sum() == len(ids):
                tmp_target_index_map = self._interxmap_cache[tmp_interxmap_type][
                    element_key
                ][valid_ids]
                ret = pd.Index(tmp_target_index_map.values)
            else:
                raise ValueError("Invalid identifiers are provided.")
        else:
            index_coord = self._storer.select_column(
                DATABASE_HDF5_STRUCT[element_key], "index"
            )
            ret = index_coord[index_coord.isin(ids)].index
        return ret

    def get_index_by_element(
        self, element_key: str, condition: Optional[str] = None
    ) -> pd.Index:
        """Get index of target storage element.

        Parameters
        ----------
        element_key
            Storage element's key
        condition
            Custom :mod:`tables` conditions.

        Returns
        -------
            Index of target storage element at given conditions.
        """
        if self._init_state:
            if self._db_info_cache[element_key] or self._init_state == -1:
                if get_element_mode(element_key) == 2:
                    self.__set_handle_by_element(element_key)
                    if condition is None:
                        return self._storer.select_column(
                            DATABASE_HDF5_STRUCT[element_key], "index"
                        )
                    else:
                        if isinstance(condition, str):
                            return self._storer.select(
                                DATABASE_HDF5_STRUCT[element_key],
                                "columns == index & {}".format(condition),
                            )
                        else:
                            raise ValueError(
                                "Invalid condition parameter is provided. `condition` must have string type."
                            )
                else:
                    raise ValueError("Requested element requested does not have index.")
            else:
                raise ValueError("Invalid element requested.")
        else:
            raise RuntimeError("Storage manager must be initiated.")

    def retrieve_data_by_element(
        self, element_key, columns=None, chunksize=None
    ) -> Any:
        """Retrieves data from storage element as whole or in chunks.

        Parameters
        ----------
        element_key
            Target storage element
        columns
            Target columns of table to retrieve
        chunksize
            Size of chunks to split retrieval or None to retrieve as whole.

        Returns
        -------
            Depends on input parameters. If chunked the return generator, if not then depends on type of storage element.
        """

        def fixed_product_generator(chunk_iter):
            for product_chunk in chunk_iter:
                yield self.__fix_table(element_key, product_chunk)

        if self._init_state:
            if self._db_info_cache[element_key]:
                if get_element_mode(element_key) == 2:
                    if (chunksize is not None) and get_element_type(
                        element_key
                    ) != "table":
                        raise ValueError(
                            "Error! Attempt to use `chunksize` on fixed tables."
                        )
                    if self._supplement_cache.get(element_key, None) is None:
                        self.__set_handle_by_element(element_key)
                        if columns is None:
                            product = self._storer.select(
                                DATABASE_HDF5_STRUCT[element_key], chunksize=chunksize
                            )
                        else:
                            product = self._storer.select(
                                DATABASE_HDF5_STRUCT[element_key],
                                "columns in ['index', {}]".format(
                                    ", ".join(
                                        ["'{}'".format(column) for column in columns]
                                    )
                                ),
                                chunksize=chunksize,
                            )
                        return (
                            self.__fix_table(element_key, product)
                            if chunksize is None
                            else fixed_product_generator(product)
                        )
                    else:
                        if columns is None:
                            return self.__fix_table(
                                element_key, self._supplement_cache[element_key]
                            )
                        else:
                            return self.__fix_table(
                                element_key,
                                self._supplement_cache[element_key][columns],
                            )

                else:
                    if self._supplement_cache.get(element_key, None) is None:
                        self.__set_handle_by_element(element_key)
                        return self._storer.get_node(
                            DATABASE_HDF5_STRUCT[element_key]
                        ).read()[0]
                    else:
                        return self._supplement_cache[element_key]
            else:
                raise ValueError("Invalid element requested.")
        else:
            raise RuntimeError("Storage manager must be initiated.")

    def get_element_data_by_ids(self, element_key, ids):
        """Get partial data from storage element by `ids`.

        Parameters
        ----------
        element_key
            Target storage element
        ids
            Target identifiers to retrieve data for

        Returns
        -------
            Depends on storage element type.
        """
        if self._init_state:
            if self._db_info_cache[element_key]:
                target_ids = np.asarray(ids)
                if (get_element_mode(element_key) == 2) and (
                    get_element_index_type(element_key) != None
                ):
                    if self._supplement_cache.get(element_key, None) is None:
                        self.__set_handle_by_element(element_key)
                        coord = self.__get_coordinates_for_element_by_ids(
                            element_key, target_ids
                        )
                        product = self._storer.select(
                            DATABASE_HDF5_STRUCT[element_key], coord
                        )
                        return self.__fix_table(element_key, product)
                    else:
                        valid_ids = self._supplement_cache[element_key].index.isin(
                            target_ids
                        )
                        if valid_ids.sum() == len(target_ids):
                            return self.__fix_table(
                                element_key,
                                self._supplement_cache[element_key].loc[target_ids],
                            )
                        else:
                            raise ValueError("Invalid identifiers provided.")
                else:
                    raise ValueError(
                        "Required element was not intended to be used via indexing. Use `retrieve_data_by_element` instead."
                    )
            else:
                raise ValueError("Invalid element requested.")
        else:
            raise RuntimeError("Storage manager must be initiated.")

    def compress_storage(
        self, complevel: int = 9, complib: str = "blosc", overwrite: bool = False
    ) -> bool:
        """Compresses the storage file using the required parameters.

        Parameters
        ----------
        complevel
            Compression level. Higher value will produce better
            compressions but will be processed for longer time.
        complib
            Compression method. For details look into :mod:`tables` documentation
        overwrite
            Whether to overwrite the file if it exists.

        Returns
        -------
            True if successful compressions, False otherwise.
        """
        ret = False
        if self._init_state:
            if path.exists(self._hdf5_filepath) and isinstance(complevel, int):
                if complevel < 10 and complevel > 0:
                    import subprocess
                    import os

                    self.__open_as_tables()
                    original_title = self._storer.title
                    self.shutdown()
                    hdf5_abs_path = path.abspath(self._hdf5_filepath)
                    hdf5_dir_path = path.dirname(hdf5_abs_path)
                    hdf5_basename = path.basename(hdf5_abs_path)
                    hdf5_filename = path.splitext(hdf5_basename)[0]
                    hdf5_extension = path.splitext(hdf5_basename)[1]
                    compressed_hdf5_basename = "{}.compressed{}".format(
                        hdf5_filename, hdf5_extension
                    )
                    compressed_hdf5_abs_path = "{}/{}".format(
                        hdf5_dir_path, compressed_hdf5_basename
                    )
                    ptrepack_cmd = "ptrepack --dest-title={} --chunkshape=auto --propindexes --complevel={} --complib={}".format(
                        original_title, str(complevel), complib
                    ).split()
                    ptrepack_cmd.extend([hdf5_abs_path, compressed_hdf5_abs_path])
                    process = subprocess.Popen(
                        ptrepack_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                    )
                    output, error = process.communicate()
                    output = output.decode() if isinstance(output, bytes) else output
                    error = error.decode() if isinstance(error, bytes) else error
                    process.kill()
                    if output == "":
                        if overwrite:
                            os.remove(hdf5_abs_path)
                            os.rename(compressed_hdf5_abs_path, hdf5_abs_path)
                            ret = True
                        else:
                            ret = True
                    if error.find("."):
                        if error.strip(".") != "":
                            print(error)
        return ret

    @classmethod
    def __fix_table(cls, element_key, target_df):
        """Fix the table with missing values."""
        if element_key == "map-rep2tid":
            return target_df
        else:
            return missing_to_none(target_df)

    @property
    def state(self):
        """State of the storage manager.

        True of :attr:`.storer` is assigned.
        """
        return self._init_state

    @property
    def active_elements(self):
        """Active storage elements that can be used."""
        return self._db_info_cache[self._db_info_cache == True].index.tolist()

    @property
    def element_state(self):
        """Cached states per storage element."""
        return self._db_info_cache

    @property
    def summary(self):
        """Cached storage database summary table."""
        return self._db_summary

    @property
    def taxon_ids(self) -> pd.Index:
        """The :term:`tids` present in the storage."""
        if self._interxmap_cache["map-interx-taxon"] is not None:
            return self._interxmap_cache["map-interx-taxon"].index
        else:
            RuntimeError("Storage is closed/broken.")

    @property
    def repseq_ids(self) -> pd.Index:
        """The :term:`rids` present in the storage."""
        if self._interxmap_cache["map-interx-repseq"] is not None:
            return self._interxmap_cache["map-interx-repseq"].index
        else:
            RuntimeError("Storage is closed/broken.")

    @property
    def storage_name(self):
        """Storage database name/label."""
        return self._storage_name

    @property
    def hdf5_filepath(self):
        """Path to :term:`hdf5` file."""
        return path.abspath(self._hdf5_filepath)

    @property
    def has_repseq(self):
        """True if database storage contains reference sequences, False
        otherwise."""
        return self._db_info_cache["sequence-representative"]

    @property
    def has_align(self):
        """True if database storage contains alignments, False otherwise."""
        return self._db_info_cache["sequence-aligned"]

    @property
    def has_accs(self):
        """True if database storage contains sequence accessions, False
        otherwise."""
        return self._db_info_cache["sequence-accession"]

    @property
    def has_tree(self):
        """True if database storage contains reference phylogeny, False
        otherwise."""
        return self._db_info_cache["tree-parsed"]

    @property
    def has_tax(self):
        """True if database storage contains reference taxonomy, False
        otherwise."""
        return self._db_info_cache["taxonomy-sheet"]
