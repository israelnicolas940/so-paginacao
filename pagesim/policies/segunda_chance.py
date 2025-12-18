from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page


class SegundaChancePolicy(ReplacementPolicy):
    def __init__(self, ram: Ram):
        self.ram = ram
        self.fila: list[int] = [] # Fila de páginas 
        self.pos: int = 0 # Posição inicial na fila

    def on_access(self, page_id: int, page: Page):
        # Quando a página entra ela tem 1 chance a mais de não ser retirada, essa chance renova 
        # Se a página for refernciada
        page.reference_bit = True 

        # Se a página já não estiver na fila, ela é inserida
        if(page_id not in self.fila):
            self.fila.append(page_id)

    def victim(self) -> int:
        while True:
            page_id = self.fila[self.pos]
            page = self.ram.pages[page_id]

            # Se a página não tiver mais uma chance...
            if(not page.reference_bit):
                # Remove a página da fila...
                self.fila.pop(self.pos)
                # e ajusta o ponteiro do relógio, se necessário
                if(self.pos >= len(self.fila)):
                    self.pos = 0
                return page_id
            else:
                # Retira a segunda chance...
                page.reference_bit = False
                # e reposiciona o ponteiro para a próxima página
                self.pos = (self.pos + 1) % len(self.fila)


