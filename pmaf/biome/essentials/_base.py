from ._metakit import EssentialBackboneMetabase,EssentialControllerBackboneMetabse
from pmaf.biome._base import BiomeBackboneBase

class EssentialBackboneBase(BiomeBackboneBase,EssentialBackboneMetabase):
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
        if self.__buckled and (self.__controller is not None):
            ret = self.__controller.reflect_action(self, method, value, **kwargs)
        else:
            ret = value
        if rlog or _reflectin:
            return ret
        else:
            return None

    def _buckle(self):
        self.__buckled = True

    def _unbuckle(self):
        self.__buckled = False

    def _mount_controller(self, controller):
        if self.__controller is None:
            if isinstance(controller, EssentialControllerBackboneMetabse):
                self.__controller = controller
            else:
                raise TypeError('`controller` has invalid type.')
        else:
            raise RuntimeError('Controller is already mounted.')

    @property
    def is_mounted(self):
        return self.__controller is not None

    @property
    def controller(self):
        return self.__controller

    @property
    def _isbuckled(self):
        return self.__buckled