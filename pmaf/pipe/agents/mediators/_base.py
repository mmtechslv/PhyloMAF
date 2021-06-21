from ._metakit import MediatorBackboneMetabase

class MediatorBase(MediatorBackboneMetabase):
    """ """
    def __init__(self,_client,_configs):
        self.__client = _client
        self.__configs = dict(_configs)


    def reconfig(self,name,value):
        """

        Parameters
        ----------
        name :
            
        value :
            

        Returns
        -------

        """
        if name in self.__configs.keys():
            self.__configs[name] = value
        else:
            raise KeyError("Configuration does not exist.")

    @property
    def configs(self):
        """ """
        return self.__configs

    @property
    def client(self):
        """ """
        return self.__client
