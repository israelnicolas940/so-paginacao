from pagesim.core.ram import Ram
from pagesim.core.disk import Disk
from pagesim.policies.base import ReplacementPolicy
from pagesim.core.models import TimeValue
from pagesim.core.models import Page


class PageTable:
    def __init__(self, ram: Ram, disk: Disk, policy: ReplacementPolicy):
        self.ram = ram
        self.disk = disk
        self.policy = policy
        self.page_faults = 0
        self.time = 0

    def access(self, page_id: int):
        self.time += 1

        if not self.ram.contains(page_id):
            self.page_faults += 1

            if self.ram.is_full():
                victim_id = self.policy.victim()
                victim_page = self.ram.remove(victim_id)
                self.disk.write(victim_page)

            page = Page(
                created_at=TimeValue(self.time),
                last_accessed_at=TimeValue(self.time),
                access_count=1,
            )
            self.ram.insert(page_id, page)
        else:
            page = self.ram.pages[page_id]
            page.last_accessed_at = TimeValue(self.time)
            page.access_count += 1

        self.policy.on_access(page_id, page)
