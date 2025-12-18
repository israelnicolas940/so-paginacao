from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page
from collections import deque


class SegundaChancePolicy(ReplacementPolicy):
    def __init__(self, ram: Ram):
        super().__init__(ram)
        self.queue = deque()
        self.capacity = ram.capacity

    def on_access(self, page_id: int, page: Page):
        if page_id not in self.queue:
            self.queue.append(page_id)

        page.reference_bit = True

    def victim(self) -> int:
        while True:
            current_page_id = self.queue.popleft()
            current_page = self.ram.get_page(current_page_id)

            if current_page.reference_bit:
                current_page.reference_bit = False
                self.queue.append(current_page_id)
            else:
                return current_page_id
