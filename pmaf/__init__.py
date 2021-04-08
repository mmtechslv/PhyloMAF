import warnings as __warnings_
import tables as __tables_
import sys as __sys_
import os as __os_

if __sys_.platform == 'win32':
    __sep_ = ';'
else:
    __sep_ = ':'

__os_.environ['PATH'] += __sep_ + __sys_.prefix
__os_.environ['PATH'] += __sep_ + __sys_.prefix + '/bin'


__warnings_.filterwarnings(action='ignore', category=__tables_.NaturalNameWarning,module='tables')
__warnings_.filterwarnings(action='ignore', category=__tables_.PerformanceWarning,module='tables')

from . import database
from . import biome
from . import alignment
from . import classifier
from . import phylo
from . import pipe
from . import remote
from . import sequence

__all__ = ['database','biome','alignment','classifier','phylo','pipe','remote','sequence']
