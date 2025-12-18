# Simulador de Paginação – Decisões de Implementação

## 1. Visão Geral

Este projeto implementa um **simulador de paginação de memória**, típico da disciplina de Sistemas Operacionais, com foco na simulação de **page faults** e **algoritmos de substituição de páginas (replacement policies)**. A arquitetura foi projetada de forma modular, permitindo a troca e extensão de políticas de substituição sem alterar o restante do sistema.

Os principais componentes do simulador são:

* **RAM**: representa a memória física com capacidade limitada;
* **Page Table**: responsável pelo controle de acessos, page faults e integração entre RAM, disco e política de substituição;
* **Replacement Policies**: abstração e implementações concretas dos algoritmos de substituição;
* **Modelos auxiliares** (`Page`, `TimeValue`): encapsulam metadados das páginas.

---

## 2. Estrutura Geral do Projeto

O núcleo do sistema está organizado em módulos bem definidos, seguindo o princípio de **separação de responsabilidades**:

* `ram.py` → Gerencia a memória física
* `page_table.py` → Controla acessos e page faults
* `policies/base.py` → Define a abstração para políticas de substituição

Essa divisão facilita a manutenção, leitura do código e extensão do simulador.

---

## 3. RAM (Memória Física)

### Classe: `Ram`

A classe `Ram` modela a memória física como um conjunto limitado de quadros de página.

#### Estrutura de Dados

* Utiliza um **dicionário (`Dict[int, Page]`)**, onde:

  * a chave é o `page_id`
  * o valor é o objeto `Page`

Essa escolha permite:

* Busca em tempo constante (O(1));
* Remoção eficiente de páginas vítimas;
* Acesso direto aos metadados da página.

#### Principais Métodos

* `is_full()` → verifica se a capacidade foi atingida;
* `insert(page_id, page)` → insere uma página na RAM;
* `remove(page_id)` → remove e retorna uma página (usado na substituição);
* `contains(page_id)` → verifica se a página está na RAM;
* `get_page(page_id)` → retorna a página armazenada.

A classe **não decide qual página remover**, delegando essa responsabilidade para a política de substituição.

---

## 4. Page Table

### Classe: `PageTable`

A `PageTable` é o **componente central do simulador**, responsável por:

* Processar acessos a páginas;
* Detectar **page faults**;
* Coordenar a interação entre RAM, disco e política de substituição;
* Manter estatísticas de execução.

#### Atributos Principais

* `ram`: instância de `Ram`;
* `disk`: instância de `Disk` (armazenamento secundário);
* `policy`: política de substituição ativa;
* `page_faults`: contador de falhas de página;
* `time`: relógio lógico do simulador.

#### Fluxo do Método `access(page_id)`

1. Incrementa o tempo lógico;
2. Verifica se a página está na RAM:

   * **Se não estiver**:

     * Incrementa o contador de page faults;
     * Se a RAM estiver cheia:

       * Solicita à política a página vítima (`victim()`);
       * Remove a página da RAM e grava no disco;
     * Cria uma nova instância de `Page` e insere na RAM;
   * **Se estiver**:

     * Atualiza o tempo de último acesso;
     * Incrementa o contador de acessos;
3. Notifica a política de substituição por meio de `on_access()`.

Essa lógica centraliza o controle do sistema, mantendo as demais estruturas desacopladas.

---

## 5. Replacement Policies (Políticas de Substituição)

### Abstração: `ReplacementPolicy`

As políticas de substituição seguem uma **abstração comum**, definida pela classe base `ReplacementPolicy`.

#### Interface Definida

* `on_access(page_id, page)`

  * Chamado a cada acesso de página;
  * Permite que a política atualize seus dados internos (listas, contadores, etc.).

* `victim()`

  * Retorna o `page_id` da página que deve ser removida da RAM;
  * A decisão depende exclusivamente da lógica da política concreta.

#### Estrutura Interna

* Cada política mantém uma referência à RAM;
* Pode utilizar estruturas auxiliares próprias (listas, filas, mapas, etc.).

---

## 6. Padrões de Projeto Utilizados

### Strategy Pattern (Padrão Strategy)

O projeto aplica claramente o **padrão Strategy**:

* `ReplacementPolicy` define a interface comum;
* As políticas concretas implementam diferentes estratégias de substituição;
* A `PageTable` opera de forma genérica, sem conhecer os detalhes da política utilizada.

Benefícios desse padrão:

* Facilidade de extensão (novos algoritmos);
* Baixo acoplamento;
* Código mais limpo e organizado.

---

## 7. Modelos Auxiliares

### Classe `Page`

Cada página mantém metadados essenciais para as políticas:

* `created_at`: momento de criação (útil para FIFO);
* `last_accessed_at`: último acesso (útil para LRU);
* `access_count`: número de acessos (útil para LFU).

Esses atributos permitem que múltiplas políticas reutilizem a mesma estrutura de dados.

---

## 8. Considerações Finais

O simulador apresenta uma arquitetura simples, porém bem estruturada, adequada para fins educacionais. As principais decisões de implementação priorizam:

* Clareza conceitual;
* Modularidade;
* Extensibilidade;
* Separação entre mecanismo (PageTable/RAM) e política (ReplacementPolicy).

Essa abordagem facilita tanto a análise dos algoritmos de substituição quanto a evolução futura do projeto.
