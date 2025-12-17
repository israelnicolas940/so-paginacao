from typing import List, Type
from pagesim.core.models import ReplacementAlgo, PagingResult
from pagesim.core.page_table import PageTable
from pagesim.core.disk import Disk
from pagesim.core.ram import Ram
from pagesim.policies.base import ReplacementPolicy
from pagesim.policies.opt import OptPolicy


class PagingSimulator:
    def __init__(
        self, policy_cls: Type[ReplacementPolicy], frames: int, trace: List[int]
    ):
        self.ram = Ram(frames)
        self.disk = Disk()

        # Handle OptPolicy special case
        if policy_cls == OptPolicy:
            self.policy = policy_cls(self.ram, trace)
        else:
            self.policy = policy_cls(self.ram)

        self.page_table = PageTable(self.ram, self.disk, self.policy)
        self.trace = trace

    def run(self) -> PagingResult:
        for page_id in self.trace:
            self.page_table.access(page_id)

        return PagingResult(
            page_faults=self.page_table.page_faults,
            disk_writes=self.disk.write_count,
            ram_last_state=list(self.ram.pages.keys()),
        )
