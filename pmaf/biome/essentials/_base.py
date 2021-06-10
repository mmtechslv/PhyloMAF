from ._metakit import EssentialBackboneMetabase,EssentialControllerBackboneMetabse
from pmaf.biome._base import BiomeBackboneBase

class EssentialBackboneBase(BiomeBackboneBase,EssentialBackboneMetabase):
    '''Base class for `Essentials` with common methods and properties.'''
    def __init__(self, _controller=None, **kwargs):
        if _controller is not None:
            if isinstance(_controller,EssentialControllerBackboneMetabse):
                self.__controller = _controller
            else:
                raise TypeError('Private parameter `_controller` has invalid type.')
        else:
            self.__controller = None
        super().__init__(**kwargs)
        self.__buckled = False

    def _ratify_action(self, method, value, _reflectin=False, rlog=False, **kwargs):
        '''Ratify the action. Actual reflection handled by `Controller`.

        Args:
          method(str): Name of the method to mirror.
          value(Any): Value of the method to mirror.
          _reflectin(bool, optional): Is the beginning of reflection or continuation. (Default value = False)
          rlog(bool, optional): Return the result or not. (Default value = False)
          kwargs: type kwargs:
          **kwargs: 

        Returns:
          Any: Result of called method.

        '''
        if self.__buckled and (self.__controller is not None):
            ret = self.__controller.reflect_action(self, method, value, **kwargs)
        else:
            ret = value
        if rlog or _reflectin:
            return ret
        else:
            return None

    def _buckle(self):
        '''Mark `Essental` istance as buckled.
        When buckled some methods, which are ratified change their return behavior.

        Args:

        Returns:

        '''
        self.__buckled = True

    def _unbuckle(self):
        '''Unmark `Essental` istance as buckled.
        When unbuckled some methods, which are ratified return to their original behavior.

        Args:

        Returns:

        '''
        self.__buckled = False

    def _mount_controller(self, controller):
        '''Mount the `Controller` to instance of `Essentials`

        Args:
          controller(EssentialControllerBackboneMetabse): Controller` instance

        Returns:

        '''
        if self.__controller is None:
            if isinstance(controller, EssentialControllerBackboneMetabse):
                self.__controller = controller
            else:
                raise TypeError('`controller` has invalid type.')
        else:
            raise RuntimeError('Controller is already mounted.')

    @property
    def is_mounted(self):
        ''' '''
        return self.__controller is not None

    @property
    def controller(self):
        ''' '''
        return self.__controller

    @property
    def is_buckled(self):
        ''' '''
        return self.__buckled