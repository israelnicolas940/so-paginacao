from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class LruPolicy(ReplacementPolicy):
    def on_access(self, page_id: int, page: Page):
        pass

    def victim(self) -> int:
        return min(
            self.ram.pages.keys(), key=lambda pid: self.ram.pages[pid].last_accessed_at
        )
