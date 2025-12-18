from pagesim.policies.base import ReplacementPolicy
from pagesim.core.models import Page


class OptPolicy(ReplacementPolicy):
    def __init__(self, ram, trace):
        super().__init__(ram)
        self.trace_position = 0
        self.trace = trace

    def on_access(self, page_id: int, page: Page):
        self.trace_position += 1

    def victim(self) -> int:
        future = self.trace[self.trace_position:]

        farthest_page = None
        farthest_distance = -1

        for page_id in self.ram.pages:
            if page_id not in future:
                return page_id

            next_use = future.index(page_id)

            if next_use > farthest_distance:
                farthest_distance = next_use
                farthest_page = page_id

        return farthest_page
