from dataclasses import dataclass
from typing import List, Type

from pagesim.core.models import PagingResult
from pagesim.policies.base import ReplacementPolicy
from pagesim.policies.fifo import FifoPolicy
from pagesim.policies.lfu import LfuPolicy
from pagesim.policies.lru import LruPolicy
from pagesim.policies.mfu import MfuPolicy
from pagesim.policies.nru import NruPolicy
from pagesim.policies.opt import OptPolicy
from pagesim.policies.segunda_chance import SegundaChancePolicy
from pagesim.core.simulator import PagingSimulator
from pagesim.core.models import ReplacementAlgo


@dataclass(slots=True)
class Report:
    algo: ReplacementAlgo
    frames: int
    trace_size: int
    algo_res: PagingResult

    def __str__(self) -> str:
        sep = "\n"
        return sep.join(
            [
                f"Algoritmo: {self.algo.name}",
                f"Frames: {self.frames}",
                f"Referências: {self.trace_size}",
                f"Faltas de página: {self.algo_res.page_faults}",
                f"Taxa de faltas: {(self.algo_res.page_faults / self.trace_size)*100:.2f}%",
                f"Evicções: {self.algo_res.disk_writes}",
                "Conjunto residente final:",
                f"frame_ids: {[i for i, _ in enumerate(self.algo_res.ram_last_state)]}",
                f"page_ids: {[v for v in self.algo_res.ram_last_state]}",
            ]
        )


class PagerService:
    def __init__(self, algo: ReplacementAlgo, frames: int, trace_filename: str):
        self.algo = algo
        self.frames = frames
        self.trace_list = self._read_trace(trace_filename)

    def run_pager(self) -> Report:
        policy_cls = self._get_policy_class(self.algo)
        simulator = PagingSimulator(policy_cls, self.frames, self.trace_list)
        result = simulator.run()

        return Report(
            algo=self.algo,
            frames=self.frames,
            trace_size=len(self.trace_list),
            algo_res=result,
        )

    def _get_policy_class(self, algo: ReplacementAlgo) -> Type[ReplacementPolicy]:
        match algo:
            case ReplacementAlgo.FIFO:
                return FifoPolicy
            case ReplacementAlgo.LRU:
                return LruPolicy
            case ReplacementAlgo.OTIMO:
                return OptPolicy
            case ReplacementAlgo.SEGUNDA_CHANCE:
                return SegundaChancePolicy
            case ReplacementAlgo.CLOCK:
                return SegundaChancePolicy  # É o mesmo que segunda chance
            case ReplacementAlgo.NRU:
                return NruPolicy
            case ReplacementAlgo.LFU:
                return LfuPolicy
            case ReplacementAlgo.MFU:
                return MfuPolicy
            case _:
                raise ValueError(f"Unsupported replacement algorithm: {algo}")

    def _read_trace(self, filename: str) -> List[int]:
        trace: List[int] = []
        try:
            with open(filename, "r") as infile:
                for line_num, line in enumerate(infile, 1):
                    try:
                        trace.append(int(line.strip()))
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid integer at line {line_num}: '{line.strip()}'"
                        ) from e
        except FileNotFoundError:
            raise FileNotFoundError(f"Trace file not found: {filename}")
        except OSError as e:
            raise OSError(f"Error reading trace file '{filename}': {e}") from e
        return trace
