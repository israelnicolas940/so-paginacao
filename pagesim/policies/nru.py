from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class NruPolicy(ReplacementPolicy):
    def on_access(self, page_id: int, page: Page):
        pass

    def victim(self) -> int:
        pass
