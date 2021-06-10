from ._metakit import EssentialControllerBackboneMetabse
from pmaf.biome.essentials._metakit import EssentialFeatureMetabase,EssentialSampleMetabase,EssentialBackboneMetabase
import numpy as np

class EssentialsController(EssentialControllerBackboneMetabse):
    '''Controller for any `biome.essentials` working together within `biome.assembly`.'''

    def __init__(self, remount=False, **kwargs):
        """

        :param remount: Force remount.
        :type remount: bool
        :param kwargs:
        :type kwargs:
        """
        self.__essentials = []
        self.__feature_ids = None
        self.__sample_ids = None
        self.__remount = bool(remount)

    def insert_essential(self, essential):
        '''Add instance of `Essentials` to the controller.

        Args:
          essential(EssentialBackboneMetabase): Instance of `pmaf.biome.essentials._metakit.EssentialBackboneMetabase`

        Returns:

        '''
        if isinstance(essential,EssentialBackboneMetabase):
            if not essential.is_mounted or self.__remount:
                self.__append_essential(essential)
            else:
                raise ValueError('`essential` is already mounted.')
        else:
            raise TypeError('`essential` has invalid type.')

    def verify_essential(self, essential, check_axis=True, check_mount=True):
        '''Validates the essentials instance.

        Args:
          essential(EssentialBackboneMetabase): Instance of `Essentials` to validate.
          check_axis(bool, optional): Whether to check if axes are compatible with active essential instances. (Default value = True)
          check_mount(bool, optional): Whether to check if the instance is already mounted. (Default value = True)

        Returns:
          bool: Result of validation.

        '''
        ret = False
        if isinstance(essential,EssentialBackboneMetabase):
            if not essential.is_mounted or self.__remount or not check_mount :
                tmp_essential_types = {type(tmp_essential) for tmp_essential in self.__essentials}
                if check_axis:
                    if type(essential) not in tmp_essential_types:
                        if isinstance(essential, EssentialFeatureMetabase):
                            if self.__feature_ids is None:
                                feature_ret = True
                            else:
                                tmp_feature_ids = np.sort(essential.xrid)
                                if np.array_equal(self.__feature_ids, tmp_feature_ids):
                                    feature_ret = True
                                else:
                                    feature_ret = False
                        else:
                            feature_ret = True
                        if isinstance(essential, EssentialSampleMetabase):
                            if self.__sample_ids is None:
                                sample_ret = True
                            else:
                                tmp_sample_ids = np.sort(essential.xsid)
                                if np.array_equal(self.__sample_ids, tmp_sample_ids):
                                    sample_ret = True
                                else:
                                    sample_ret = False
                        else:
                            sample_ret = True
                        ret = feature_ret and sample_ret
                else:
                    ret = True
        return ret

    def __append_essential(self, essential):
        """Logic behind adding the instance of `Essentials`.

        :param essential: Instance to append.
        :type essential: EssentialBackboneMetabase
        """
        tmp_essential_types = {type(tmp_essential) for tmp_essential in self.__essentials}
        if type(essential) not in tmp_essential_types:
            if isinstance(essential,EssentialBackboneMetabase):
                essential_pass= False
                if isinstance(essential, EssentialFeatureMetabase):
                    if self.__feature_ids is None:
                        self.__feature_ids = np.sort(essential.xrid)
                        essential_pass = True
                    else:
                        tmp_feature_ids  = np.sort(essential.get_feature_ids(self.__feature_ids.dtype))
                        if np.array_equal(self.__feature_ids, tmp_feature_ids):
                            essential_pass = True
                        else:
                            raise ValueError('Essentials must have same ids at both axes.')
                if isinstance(essential, EssentialSampleMetabase):
                    if self.__sample_ids is None:
                        self.__sample_ids = np.sort(essential.xsid)
                        essential_pass = True
                    else:
                        tmp_sample_ids = np.sort(essential.get_sample_ids(self.__sample_ids.dtype))
                        if np.array_equal(self.__sample_ids, tmp_sample_ids):
                            essential_pass = True
                        else:
                            raise ValueError('Essentials must have same ids at both axes.')
                if essential_pass:
                    essential._mount_controller(self)
                    essential._buckle()
                    self.__essentials.append(essential)
                else:
                    raise RuntimeError('`essential` did not pass controls.')
            else:
                raise ValueError('`essential` has invalid type.')
        else:
            raise RuntimeError('`essential` of same type is already present.')

    def __reinitialize(self):
        """(Re)initialize the current controller instance.

        :rtype: object
        """
        tmp_feature_ids = None
        tmp_sample_ids = None
        for essential in self.__essentials:
            if isinstance(essential, EssentialFeatureMetabase):
                if tmp_feature_ids is None:
                    tmp_feature_ids = np.sort(essential.xrid)
                else:
                    if not np.array_equal(tmp_feature_ids, np.sort(essential.xrid)):
                        raise RuntimeError('Essentials have invalid axes.')
            if isinstance(essential, EssentialSampleMetabase):
                if tmp_sample_ids  is None:
                    tmp_sample_ids  = np.sort(essential.xsid)
                else:
                    if not np.array_equal(tmp_sample_ids, np.sort(essential.xsid)):
                        raise RuntimeError('Essentials have invalid axes.')
        self.__feature_ids = tmp_feature_ids
        self.__sample_ids = tmp_sample_ids

    def reflect_action(self, source, method, value, **kwargs):
        '''Reflect or mirror the action to controlled instances of `essentials`.

        Args:
          source(EssentialBackboneMetabase): Instance of Essential where the action is coming from.
          method(str): Name of the method to be reflected.
          value(Any): Value to be passed to mirroring functions. Eg. ids to be removed.
          kwargs(dict): Remaining parameters passed to mirroring function.
          **kwargs: 

        Returns:
          dict: Dictionary with results for each `Essential`

        '''
        if len(self.__essentials)>0:
            tmp_rets = {source: value}
            self.__unbuckle_essentials()
            for essential in self.__essentials:
                if essential is not source and hasattr(essential,method):
                    essential_ret = getattr(essential,method)(value, _reflectin=True, **kwargs)
                    tmp_rets.update({essential:essential_ret})
            self.__reinitialize()
            self.__buckle_essentials()
            return tmp_rets
        else:
            raise RuntimeError('Controller has not been initialized yet.')

    def __buckle_essentials(self):
        """Buckle all controlled essentials so that no other change is made during mirroring."""
        for essential in self.__essentials:
            essential._buckle()

    def __unbuckle_essentials(self):
        """Unbuckle all controlled essentials."""
        for essential in self.__essentials:
            essential._unbuckle()

    def has_essential_by_types(self, *args):
        '''Helper function that checks if `Essentials` in `args` are controlled via current `Controller` instance.

        Args:
          args(list-like): Essentials`
          *args: 

        Returns:
          rtype: bool

        '''
        ret = []
        for arg in args:
            ret.append(any([isinstance(essential,arg) for essential in self.__essentials]))
        return all(ret)

    def take_essential_by_type(self, type):
        '''Get controlled essential by type.

        Args:
          type: type type:

        Returns:
          rtype: 

        '''
        ret = None
        for essential in self.__essentials:
            if isinstance(essential,type):
                ret = essential
        if ret is not None:
            return ret
        else:
            raise ValueError('Essential with given `type` is was not found.')

    @property
    def state(self):
        '''Is controller active.'''
        return len(self.__essentials)>0

    @property
    def count(self):
        '''Total controlled essentials.'''
        return len(self.__essentials)

    @property
    def essentials(self):
        '''Get controlled essentials.'''
        return self.__essentials

    @property
    def xrid(self):
        '''Feature axis of controlled essentials.'''
        return self.__feature_ids

    @property
    def xsid(self):
        '''Sample axis of controlled essentials.'''
        return self.__sample_ids




