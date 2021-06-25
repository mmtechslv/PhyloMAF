from ._metakit import SpecificationBackboneMetabase
from typing import Any, Union


class SpecificationBase(SpecificationBackboneMetabase):
    """"""

    def __repr__(self):
        class_name = self.__class__.__name__
        state = "Active" if self.state == 1 else "Inactive"
        total_steps = str(len(self.steps))
        inlet = self.inlet.__name__
        outlet = self.outlet.__name__
        repr_str = "<{}:[{}], Steps:[{}], Inlet:[{}], Outlet:[{}]>".format(
            class_name, state, total_steps, inlet, outlet
        )
        return repr_str

    def fetch(self, data: Any, *args: Any, **kwargs: Any):
        """Fetch the data through the pipe specification.

        Parameters
        ----------
        data
            Data that will be passed through the pipe.
            Type of `data` depends on the :term:`spec` indicated in :meth:`.inlet`.

        *args
            Compatibility
        **kwargs
            Compatibility

        Returns
        -------
            Results of the pipe with type matching :meth:`.outlet`
        """
        product = None
        next_args = (data, *args)
        next_kwargs = kwargs
        for name, method, outlet, description in self.steps:
            product, new_args, next_kwargs = method(*next_args, **next_kwargs)
            next_args = (product, *new_args)
        if isinstance(product, self.outlet):
            return product
        else:
            raise RuntimeError("Process was not completed according to specification.")
