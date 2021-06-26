import numpy as np
import pandas as pd
from typing import (
    Any,
    Callable,
    Hashable,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

Label = Optional[Hashable]
Shape = Tuple[int, ...]
GenericIdentifier = Union[str, int]
AnyGenericIdentifier = Union[Sequence[GenericIdentifier], np.ndarray, pd.Index, GenericIdentifier]
Mapper = Union[Mapping[Label, Any], Callable[[Label], Label]]
AggFunc = Union[str, Callable]