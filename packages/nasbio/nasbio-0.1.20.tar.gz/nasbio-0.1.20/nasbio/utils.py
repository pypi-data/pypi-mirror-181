from typing import Any, Optional
from enum import Enum
import operator

import strawberry

operator_keys = {
    '': operator.eq,
    '>': operator.ge,
    '<': operator.le,
}


def split(item_list: Any, n: int):
    k, m = divmod(len(item_list), n)

    return (item_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


@strawberry.enum(description='Selection of organisms.')
class OrganismSelect(Enum):
    NONE = ''
    HUMAN = 'human'
    MOUSE = 'mouse'
    RAT = 'rat'


organism_mapping = {
    'human': 9606,
    'mouse': 10090,
    'rat': 10116,
}


@strawberry.input
class InputWithOrganism:
    organism: Optional[OrganismSelect] = OrganismSelect.NONE
