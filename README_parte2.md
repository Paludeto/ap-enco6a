# Avaliação Prática: ES 2026.1

---

## Tarefa 2.1: Definição da Arquitetura (15 min)

### Padrão Arquitetural Escolhido: Arquitetura em Camadas (Layered Architecture)

Escolhi a **Arquitetura em Camadas (N-Tier Layered Architecture)**, organizada em quatro camadas: Apresentação, Aplicação, Domínio e Infraestrutura.

**Justificativa em relação ao domínio e às histórias de usuário:**

O sistema tem responsabilidades bem separadas. Existe o gerenciamento de tarefas (H1, H3), a predição por modelo estatístico (H2), o matching por questionário (H4) e a exportação de progresso (H5). Essa divisão dos módulos se acomoda bem em camadas estáveis. Cada serviço de negócio (TaskService, PredictionService, MatcherService) pode evoluir de forma isolada dentro da camada de Domínio sem afetar a interface nem a persistência. Como o contexto é o de um app móvel com backend centralizado, o modelo cliente-servidor implícito nas camadas já cobre o cenário.

---

### Representação dos Componentes e Relacionamentos

```
┌─────────────────────────────────────────────────────────┐
│                  CAMADA DE APRESENTAÇÃO                 │
│                    Mobile Client (App)                  │
│        UI · Notificações · Navegação · Formulários      │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼────────────────────────────────┐
│                  CAMADA DE APLICAÇÃO                    │
│                  API Gateway (REST)                     │
│     Roteamento · Autenticação · Validação de entrada    │
└──┬──────────────┬──────────────┬──────────────┬─────────┘
   │              │              │              │
┌──▼───┐   ┌─────▼────┐  ┌──────▼─────┐  ┌────▼──────┐
│Task  │   │Turnip    │  │ Villager   │  │ User /    │
│Svc   │   │Prediction│  │ Matcher    │  │ Progress  │
│      │   │Service   │  │ Service    │  │ Service   │
└──┬───┘   └─────┬────┘  └──────┬─────┘  └────┬──────┘
   │              │              │              │
┌──▼──────────────▼──────────────▼──────────────▼────────┐
│                  CAMADA DE DOMÍNIO                      │
│   Entidades · Regras de negócio · Interfaces de repo    │
│   Task · Event · TurnipEntry · Villager · UserProfile   │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                 CAMADA DE INFRAESTRUTURA                │
│   ┌──────────────┐  ┌─────────────┐  ┌───────────────┐  │
│   │  Banco de    │  │  Game Data  │  │  Notification │  │
│   │  Dados (DB)  │  │  Store      │  │  Provider     │  │
│   │  PostgreSQL  │  │  (estático) │  │  (Push/FCM)   │  │
│   └──────────────┘  └─────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

### Componentes Principais e Responsabilidades

| Componente | Camada | Responsabilidade |
|---|---|---|
| **Mobile Client** | Apresentação | Interface com o usuário. Exibe tarefas, previsões e sugestões, e recebe notificações push |
| **API Gateway** | Aplicação | Ponto de entrada único. Autentica requisições, roteia para os serviços corretos e valida inputs |
| **TaskService** | Aplicação | Gerencia tarefas diárias e sazonais. Controla a marcação de conclusão e o reset às 5 AM (H1, H3) |
| **TurnipPredictionService** | Aplicação | Recebe os preços inseridos pelo usuário, executa o modelo preditivo e retorna intervalos de projeção (H2) |
| **VillagerMatcherService** | Aplicação | Processa o questionário de perfil e aplica a lógica de matching sobre o catálogo de villagers (H4) |
| **UserProgressService** | Aplicação | Consolida os dados de progresso do usuário e gera a exportação (H5) |
| **Entidades de Domínio** | Domínio | Definem a estrutura e as regras de negócio de Task, Event, TurnipEntry, Villager e UserProfile |
| **Banco de Dados (PostgreSQL)** | Infraestrutura | Persiste os dados transacionais como perfil, progresso e histórico de preços de turnips |
| **Game Data Store** | Infraestrutura | Armazena dados semi-estáticos do jogo, como calendário de eventos, catálogo de villagers e lista de tarefas recorrentes |
| **Notification Provider (FCM)** | Infraestrutura | Entrega notificações push ao dispositivo do usuário via Firebase Cloud Messaging |

---

### Limitação / Trade-off

**Acoplamento de deploy entre o preditor e o resto do sistema:**

Como a aplicação é um monólito em camadas, o `TurnipPredictionService` compartilha o ciclo de deploy com todo o backend. O modelo de predição pode demandar atualizações e retreinamento próprios, e cada ajuste no modelo força o redeploy completo, no lugar da substituição isolada do serviço. A rigidez vem do monólito, não das camadas. Mesmo mantendo a divisão em camadas, seria possível extrair o preditor como serviço independente. Microsserviços resolveriam o problema de forma definitiva, mas trariam complexidade operacional desproporcional ao escopo atual.

---

**Minha reflexão:** Escolhi camadas pela clareza na separação de responsabilidades e porque o escopo do projeto é acadêmico. Ainda assim, o `TurnipPredictionService` é o ponto que mais incomoda nessa escolha. Um modelo preditivo tem ciclo de vida diferente de um CRUD de tarefas, e no futuro pode fazer sentido isolar o preditor como serviço próprio, mesmo que hoje o overhead não compense. Manter tudo em um monólito em camadas é um trade-off, troquei escalabilidade por simplicidade.

---

## Tarefa 2.2: Protótipo Funcional e Padrões de Projeto

**Histórias implementadas:** H2 (preditor de preços de turnip) e H3 (gerenciador de tarefas diárias).

**Estrutura do projeto:**
```
acnh_prototype/
├── main.py
├── tasks/
│   ├── observer.py       # interfaces Subject e Observer
│   ├── task.py           # entidade Task
│   ├── task_manager.py   # Subject concreto
│   └── notifiers.py      # Observers concretos
└── turnip/
    ├── strategies.py     # estratégias de predição
    └── predictor.py      # contexto da estratégia
```

---

### Padrão 1: Observer

**Categoria:** Comportamental

**Onde foi aplicado:**

- `tasks/observer.py` define as interfaces `Observer` (método `update`) e `Subject` (métodos `attach`, `detach`, `notify`).
- `tasks/task_manager.py` faz o `TaskManager` herdar de `Subject` e chamar `self.notify(...)` em `complete_task` e `reset_daily_tasks`.
- `tasks/notifiers.py` traz `ConsoleNotifier` e `TaskLogger`, ambos implementando `Observer`.
- O ponto de uso fica em `main.py`, nas chamadas `manager.attach(ConsoleNotifier())` e `manager.attach(logger)`.

**Diagrama aplicado ao projeto:**

```
        «abstract»                       «abstract»
        Observer                         Subject
        ──────────────────               ──────────────────────────
        + update(event, data)            - _observers: list[Observer]
                △                        + attach(observer)
                │                        + detach(observer)
        ┌───────┴────────┐               + notify(event, data)
        │                │                        △
ConsoleNotifier      TaskLogger                   │
────────────────     ──────────────          TaskManager
+ update(...)        + update(...)          ─────────────────────────
                     + get_log()            - _tasks: list[Task]
                                            + add_task(task)
                                            + get_today_tasks()
                                            + complete_task(name)  ──► notify("task_completed", ...)
                                            + reset_daily_tasks()  ──► notify("daily_reset", ...)
```

---

### Padrão 2: Strategy

**Categoria:** Comportamental

**Onde foi aplicado:**

- `turnip/strategies.py` define a interface `PredictionStrategy` (método abstrato `predict`) e três estratégias concretas: `DecreasingPatternStrategy`, `LargeSpikeStrategy` e `SmallSpikeStrategy`.
- `turnip/predictor.py` traz o `TurnipPredictor`, que age como contexto. Ele armazena `_strategy` e delega a chamada em `predict` e `display_prediction`.
- A troca de estratégia acontece em `main.py`, com `predictor.set_strategy(strategy)` dentro do loop de demonstração.

**Diagrama aplicado ao projeto:**

```
        «abstract»
        PredictionStrategy
        ─────────────────────────────────────────────────
        + predict(observed: list[int]) -> list[tuple]
                △
                │
    ┌───────────┼─────────────────┐
    │           │                 │
Decreasing  LargeSpike       SmallSpike
Pattern     Strategy         Strategy
Strategy    ────────────     ────────────
            spike: slots     spike: slots
            4,5,6 → 200–600  6,7,8 → 140–200

                                    TurnipPredictor  (contexto)
                                    ──────────────────────────────
                                    - _strategy: PredictionStrategy
                                    + set_strategy(strategy)
                                    + predict(observed) ──► _strategy.predict(observed)
                                    + display_prediction(observed, buy_price)
```

---

**Revisão crítica:** O Observer funciona bem no protótipo, mas tem um problema previsível em escala. Não existe mecanismo de prioridade nem filtragem de eventos. Qualquer Observer novo, adicionado por outro membro da equipe, recebe tudo o que os Subjects emitem, sem distinção. Se o sistema crescer e passar a incluir notificações push reais, sincronização com servidor e analytics ao mesmo tempo, a cadeia de observers acoplada ao `TaskManager` vai deixar o fluxo de execução opaco e o debug caro.

---

## Tarefa 2.3: Testes Automatizados

**Arquivo:** `test_prototype.py`, com 15 casos de teste, todos passando.

**Métodos testados:** `TaskManager.complete_task` (8 casos) e `TurnipPredictor.predict` (7 casos).

### Estratégia de teste adotada

Adotei **teste de unidade com isolamento por mock** sobre os métodos de maior responsabilidade de cada módulo. Em `complete_task`, substituí o Observer por um `MagicMock`. Isso elimina dependências externas e permite verificar o contrato de notificação sem subir infraestrutura real. Em `predict`, testei o `TurnipPredictor` como contexto do padrão Strategy, cobrindo tanto a delegação para a estratégia atual quanto a validação de entrada.

A abordagem faz sentido aqui porque ambos os métodos encapsulam regras de negócio com entradas e saídas previsíveis, o que torna os testes rápidos e determinísticos. Priorizei cenários de borda para deixar registradas as limitações do design atual, como tarefas com nomes duplicados e o caso da semana inteira já observada.

**Aspectos não cobertos e por quê:**

- `get_today_tasks` depende de `date.today()`. Testar cenários de dias diferentes exigiria monkey-patching da data. Ficou de fora por escopo, não por impossibilidade.
- `display_prediction` só produz efeito colateral em `stdout`. É testável com `unittest.mock.patch('builtins.print')`, mas não traz valor de negócio relevante neste momento.
- `reset_daily_tasks` tem lógica simples de iteração. O risco de regressão é baixo comparado ao custo de manter os testes.
- A integração entre `TaskManager` e `ConsoleNotifier` já está coberta de forma implícita pelo teste de notificação com mock. Um teste de integração real seria redundante no escopo atual.

---

**Revisão crítica:** O método `display_prediction` em `turnip/predictor.py` é o mais difícil de testar de forma útil. Ele mistura lógica de formatação com chamadas diretas a `print` e não retorna nada. Em um projeto maior, essa ausência de retorno obrigaria todos os testes a capturar `stdout` via patch ou redirecionamento, o que é frágil. Qualquer mudança cosmética na formatação (espaçamento, símbolo de moeda, idioma) quebraria testes que não têm relação com regra de negócio. O caminho correto seria separar a construção dos dados de exibição da renderização propriamente dita, mas isso exigiria refatorar a interface do método.
