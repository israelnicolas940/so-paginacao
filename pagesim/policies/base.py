from abc import ABC, abstractmethod
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class ReplacementPolicy(ABC):
    def __init__(self, ram: Ram):
        self.ram = ram

    @abstractmethod
    def on_access(self, page_id: int, page: Page):
        """Called when a page is accessed"""
        pass

    @abstractmethod
    def victim(self) -> int:
        """Return page_id to evict"""
        pass
