from ._metakit import MediatorBackboneMetabase
from typing import Any


class MediatorBase(MediatorBackboneMetabase):
    def __init__(self, _client: Any, _configs: dict):
        self.__client = _client
        self.__configs = dict(_configs)

    def reconfig(self, name: str, value: Any):
        """Set config `name` to `value`

        Parameters
        ----------
        name
            Configuration name
        value
            Configuration value
        """
        if name in self.__configs.keys():
            self.__configs[name] = value
        else:
            raise KeyError("Configuration does not exist.")

    @property
    def configs(self) -> dict:
        """All current configs."""
        return self.__configs

    @property
    def client(self) -> Any:
        """Current active client that :term:`mediator` mediates."""
        return self.__client
