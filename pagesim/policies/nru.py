from pagesim.policies.base import ReplacementPolicy
from pagesim.core.ram import Ram
from pagesim.core.models import Page
import random


class NruPolicy(ReplacementPolicy):
    def on_access(self, page_id: int, page: Page):
        # Sinaliza que a página foi referenciada...
        page.reference_bit = True
        # e vamos sempre supor que toda página acessada foi modificada
        page.modified_bit = True

    def victim(self) -> int:
        # Criam-se as classes possíveis de páginas
        classes = {0: [], 1: [], 2: [], 3: []}

        for page_id, page in self.ram.pages.items():
            r = page.reference_bit
            m = page.modified_bit

            # Insere a página no grupo em que não houve referencia e nem modificação
            if(not r and not m):
                classes[0].append(page_id)
            # Insere a página no grupo em que não houve referencia, mas houve modificação
            elif(not r and m):
                classes[1].append(page_id)
            # Insere a página no grupo em que não houve modificação, mas houve referencia
            elif(r and not m):
                classes[2].append(page_id)
            # Insere a página no grupo em que houve referencia e modificação
            elif(r and m):
                classes[3].append(page_id)

        # Seleciona aleatoriamente uma vítima do melhor grupo que existir
        for cls in range(4):
            if(classes[cls]):
                victim_id = random.choice(classes[cls])
                break
        
        # Ajusta o bit de referência de todas as paginas para zero depois de cada page fault
        # esse ajuste poderia ser feito a cada N faltas, mas para simplificar faremos N=1
        for page in self.ram.pages.values():
            page.reference_bit = False
            
        return victim_id

