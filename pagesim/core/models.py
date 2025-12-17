from dataclasses import dataclass
from typing import Dict, List
import enum


class ReplacementAlgo(enum.Enum):
    FIFO = enum.auto()
    LRU = enum.auto()
    OTIMO = enum.auto()
    SEGUNDA_CHANCE = enum.auto()
    CLOCK = enum.auto()
    NRU = enum.auto()
    LFU = enum.auto()
    MFU = enum.auto()


@dataclass(order=True, slots=True)
class TimeValue:
    value: int


@dataclass(slots=True)
class Page:
    created_at: TimeValue
    last_accessed_at: TimeValue
    access_count: int
    reference_bit: bool = True  # Para Segunda Chance/Clock
    modified_bit: bool = False  # Para NRU


@dataclass(slots=True)
class PagingResult:
    page_faults: int
    disk_writes: int
    ram_last_state: List[int]
