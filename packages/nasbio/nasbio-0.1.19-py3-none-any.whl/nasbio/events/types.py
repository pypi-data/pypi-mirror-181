from typing import TypedDict
from enum import Enum


class Subjects(Enum):
    StructureComputed = 'structure.computed'


class StructureComputedData(TypedDict):
    target_id: int
    id: int
    openness: list[float]
