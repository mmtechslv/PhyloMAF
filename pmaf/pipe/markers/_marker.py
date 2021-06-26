from ._metakit import MarkerBackboneMetabase
from pmaf.pipe.specs._metakit import SpecificationBackboneMetabase
from pmaf.pipe.agents.dockers._metakit import DockerBackboneMetabase
from datetime import datetime
from typing import Any, Optional


class Marker(MarkerBackboneMetabase):
    """This class assists user in using pipe module."""

    def __init__(
        self, input: Any, name: Optional[str] = None, metadata: Optional[dict] = None
    ):
        """Constructor for :class:`.Marker`

        Parameters
        ----------
        input
            Instance of any type that has `.data` attribute.
            For example, :mod:`~pmaf.biome` or :mod:`pmaf.pipe.agents.dockers`.
        name
            Name of the marker instance.
        metadata
            Metadata of the marker instance.
        """
        if input is not None:
            if not isinstance(input, DockerBackboneMetabase):
                if hasattr(input, "data"):
                    self.__input = input.data
                else:
                    self.__input = input
            else:
                self.__input = input
            self.__inlet = type(input)
        else:
            raise ValueError("`data` cannot be None.")
        if isinstance(name, (str, int, type(None))):
            tmp_name = name
        else:
            raise TypeError("`name` can be str,int or None")
        if isinstance(metadata, dict):
            tmp_metadata = metadata
        elif metadata is None:
            tmp_metadata = {}
        else:
            raise TypeError("`metadata` can be dict or None")

        if hasattr(input, "name") and name is None:
            self.__name = input.name
        else:
            self.__name = tmp_name

        if hasattr(input, "metadata") and metadata is None:
            self.__metadata = input.metadata
        else:
            self.__metadata = tmp_metadata

        self.__outlet = None
        self.__output = None
        self.__tasks = []
        self.__task_pointer = None

    def __repr__(self):
        class_name = self.__class__.__name__
        state = "Active" if len(self.__tasks) > 0 else "Inactive"
        step = (
            "{}/{}".format(str(self.__task_pointer), str(len(self.__tasks)))
            if len(self.__tasks) > 0
            else "N/A"
        )
        inlet = self.inlet.__name__
        outlet = self.outlet.__name__ if self.outlet is not None else "N/A"
        repr_str = "<{}:[{}], Step/Total:[{}], Inlet:[{}], Outlet:[{}]>".format(
            class_name, state, step, inlet, outlet
        )
        return repr_str

    def embed_specs(self, *args):
        """Embed :term:`specs<spec>` to the :class:`.Marker`.

        Parameters
        ----------
        *args
            Instances of :term:`spec` that must be embedded.


        Returns
        -------
            Returns the outlet type of the last :term:`spec`
        """
        for spec in args:
            if isinstance(spec, SpecificationBackboneMetabase):
                if self.__task_pointer is None:
                    self.__task_pointer = 0
                    last_tix = None
                else:
                    last_tix = len(self.__tasks) - 1
                for name, method, outlet, description in spec.steps:
                    self.__tasks.append(
                        {
                            "status": False,
                            "results": None,
                            "time": datetime.now(),
                            "request": {
                                "method": method,
                                "input": last_tix,
                                "outlet": outlet,
                                "name": name,
                                "description": description,
                            },
                        }
                    )
                    last_tix = len(self.__tasks) - 1
                    self.__outlet = outlet
            else:
                raise TypeError("`marker` has invalid type.")

    def __get_pending(self):
        """Get the pending :term:`specs<spec>` to be evaluated."""
        return sorted(
            [ix for ix, task in enumerate(self.__tasks) if not task["status"]]
        )

    def __get_finished(self):
        """Get the last finished :term:`spec`"""
        return sorted([ix for ix, task in enumerate(self.__tasks) if task["status"]])

    def __move_to_next_task(self, current_task_results):
        """Move cursor to the next :term:`spec` and mark last completed."""
        self.__tasks[self.__task_pointer]["results"] = current_task_results
        self.__tasks[self.__task_pointer]["status"] = True
        self.__task_pointer = self.__task_pointer + 1
        self.__output = current_task_results[0]
        return

    def __get_next_task(self):
        """get the next :term:`spec` to be evaluated."""
        if self.__task_pointer is not None:
            if self.__task_pointer < len(self.__tasks):
                return self.__tasks[self.__task_pointer]
            else:
                return None
        else:
            raise RuntimeError("Marker is not initiated.")

    def __iter__(self):
        """Iterate over pending :term:`specs<spec>`"""
        if len(self.__tasks) > 0:
            while len(self.__get_pending()) > 0:
                yield self.__next()
        else:
            raise RuntimeError("Marker is not initiated.")

    def __next__(self):
        """Run next :term:`spec`"""
        if len(self.__tasks) > 0:
            if len(self.__get_pending()) > 0:
                return self.__next()
            else:
                raise StopIteration
        else:
            raise RuntimeError("Marker is not initiated.")

    def __next(self):
        """Helper for __next__"""
        next_task = self.__get_next_task()
        if next_task is not None:
            current_input = next_task["request"]["input"]
            spec_method = next_task["request"]["method"]
            if isinstance(current_input, int):
                last_results = self.__tasks[current_input]["results"]
                next_args = (last_results[0], *last_results[1])
                next_kwargs = last_results[2]
            else:
                next_args = (self.__input,)
                next_kwargs = {"metadata": self.__metadata, "name": self.__name}
            tmp_results = spec_method(*next_args, **next_kwargs)
            self.__move_to_next_task(tmp_results)
            return tmp_results[0]
        else:
            return None

    def next(self):
        """Same as builtin next() command."""
        if len(self.__tasks) > 0:
            if len(self.__get_pending()) > 0:
                return self.__next()
            else:
                raise StopIteration
        else:
            raise RuntimeError("Marker is not initiated.")

    def compute(self):
        """Evaluate :term:`specs<spec>`"""
        if len(self.__tasks) > 0:
            tmp_product = None
            while len(self.__get_pending()) > 0:
                tmp_product = self.__next()
            return tmp_product
        else:
            raise RuntimeError("Marker is not initiated.")

    def get_outputs(self):
        """Get the outputs."""
        return [self.__tasks[ix]["results"][0] for ix in self.__get_finished()]

    @property
    def tasks(self):
        """List all the tasks."""
        return self.__tasks

    @property
    def name(self):
        """Name of the instance."""
        return self.__name

    @property
    def metadata(self):
        """Metadata of the instance."""
        return self.__metadata

    @property
    def inlet(self):
        """Inlet type of the marker."""
        return self.__inlet

    @property
    def outlet(self):
        """Outlet type marker."""
        return self.__outlet

    @property
    def input(self):
        """Input of the marker."""
        return self.__input

    @property
    def output(self):
        """Output of the marker."""
        return self.__output

    @property
    def upcoming(self):
        """Upcoming task."""
        if len(self.__tasks) > 0:
            return self.__tasks[self.__task_pointer]["request"]["name"]
        else:
            return None
