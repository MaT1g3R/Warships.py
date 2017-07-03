from enum import Enum
from typing import List, Union


class Region(Enum):
    NA = 'com'
    EU = 'eu'
    RU = 'ru'
    AS = 'asia'


def lst_of_int(id_, name):
    if id_ is None:
        return None
    if not isinstance(id_, int) and any(not isinstance(x, int) for x in id_):
        raise ValueError('{} must be an int or a list of ints'.format(name))
    return ','.join([str(i) for i in id_]) if isinstance(id_, list) else id_


l_int = Union[int, List[int]]
