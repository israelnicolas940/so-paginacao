from pagesim.core.models import Page


class Disk:
    def __init__(self):
        self.write_count = 0

    def write(self, page: Page):
        self.write_count += 1
