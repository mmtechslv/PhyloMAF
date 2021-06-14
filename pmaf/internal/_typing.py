import numpy as np
import pandas as pd
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    AnyStr,
    Callable,
    Collection,
    Dict,
    Hashable,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

Label = Optional[Hashable]
Shape = Tuple[int, ...]
GenericIdentifier = Union[Sequence[Union[int,str]], np.ndarray, pd.Index, str, int]
Mapper = Union[Mapping[Label, Any], Callable[[Label], Label]]