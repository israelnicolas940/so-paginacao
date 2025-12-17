from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class MfuPolicy(ReplacementPolicy):
    def on_access(self, page_id: int, page: Page):
        pass

    def victim(self) -> int:
        return max(
            self.ram.pages.keys(), key=lambda pid: self.ram.pages[pid].access_count
        )
