from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class OptPolicy(ReplacementPolicy):
    def __init__(self, ram, trace):
        pass

    def on_access(self, page_id: int, page: Page):
        pass

    def victim(self) -> int:
        pass
