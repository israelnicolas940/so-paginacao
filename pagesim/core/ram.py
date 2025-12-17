from pagesim.core.models import Page
from typing import Dict


class Ram:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.pages: Dict[int, Page] = {}

    def is_full(self) -> bool:
        return len(self.pages) >= self.capacity

    def insert(self, page_id: int, page: Page):
        self.pages[page_id] = page

    def remove(self, page_id: int) -> Page:
        return self.pages.pop(page_id)

    def contains(self, page_id: int) -> bool:
        return page_id in self.pages

    def get_page(self, page_id: int) -> Page:
        return self.pages[page_id]
