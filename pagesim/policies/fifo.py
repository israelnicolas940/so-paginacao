from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page
from collections import deque


class FifoPolicy(ReplacementPolicy):

    def __init__(self, ram: Ram):
        super().__init__(ram)
        self.queue = deque()
        self.capacity = ram.capacity

    def on_access(self, page_id: int, page: Page):
        if page_id not in self.queue:
            self.queue.append(page_id)

    def victim(self) -> int:
        return self.queue.popleft()
