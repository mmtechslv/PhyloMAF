from ._metakit import EssentialBackboneMetabase,EssentialControllerBackboneMetabse
from pmaf.biome._base import BiomeBackboneBase
from typing import Union, Any
from pmaf.internal._typing import GenericIdentifier, Optional

class EssentialBackboneBase(BiomeBackboneBase,EssentialBackboneMetabase):
    """Base class for `essentials`."""
    def __init__(self,
                 _controller: Optional[EssentialControllerBackboneMetabse] = None,
                 **kwargs: Any) -> None:
        """Constructor of the `essentials` base class.

        Args:
            _controller: Instance of :class:`~pmaf.biome.essentials._controller.EssentialsController` or None to create an independent `essential`.
            **kwargs: Compatibility 
        """
        if _controller is not None:
            if isinstance(_controller, EssentialControllerBackboneMetabse):
                self.__controller = _controller
            else:
                raise TypeError('Private parameter `_controller` has invalid type.')
        else:
            self.__controller = None
        super().__init__(**kwargs)
        self.__buckled = False

    def _ratify_action(self,
                       method: str,
                       value: Any,
                       _reflectin: bool = False,
                       rlog: bool = False,
                       **kwargs: Any) -> Union[dict, GenericIdentifier, None]:
        """Ratify the action. This method perform reflection process handled by :class:`~pmaf.biome.essentials._controller.EssentialsController`.

        Args:
            method: Name of the method to mirror.
            value: Value of the method to mirror.
            _reflectin: Is the beginning of reflection or continuation.
            rlog: Return the result or not. Used while debugging
            **kwargs:

        Returns:
            Result of called method.

        """
        if self.__buckled and (self.__controller is not None):
            ret = self.__controller.reflect_action(self, method, value, **kwargs)
        else:
            ret = value
        if rlog or _reflectin:
            return ret
        else:
            return None

    def _buckle(self) -> None:
        """Mark `Essental` istance as buckled. When buckled some methods, which are ratified change their return behavior."""
        self.__buckled = True

    def _unbuckle(self) -> None:
        """Unmark `Essental` istance as buckled. When unbuckled some methods, which are ratified return to their original behavior. """
        self.__buckled = False

    def _mount_controller(self,
                          controller: EssentialControllerBackboneMetabse) -> None:
        """Mount the :class:`~pmaf.biome.essentials._controller.EssentialsController` to current instance of `essentials`

        Args:
          controller: :class:`~pmaf.biome.essentials._controller.EssentialsController` instance
        """
        if self.__controller is None:
            if isinstance(controller, EssentialControllerBackboneMetabse):
                self.__controller = controller
            else:
                raise TypeError('`controller` has invalid type.')
        else:
            raise RuntimeError('Controller is already mounted.')

    @property
    def is_mounted(self) -> bool:
        """True if current `essentials` instance is mounted or not."""
        return self.__controller is not None

    @property
    def controller(self) -> EssentialControllerBackboneMetabse:
        """Return the active :class:`pmaf.biome.essentials._controller.EssentialsController` instance. """
        return self.__controller

    @property
    def is_buckled(self) -> bool:
        """ Is current `essentials` instance is mounted or not. """
        return self.__buckled