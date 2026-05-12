# Avaliação Prática — ES 2026.1

---

## Tarefa 1.1 — Proposta de Tema (10 min)

Escolha um domínio de aplicação para o seu sistema. Descreva em até 10 linhas:
- O problema que o sistema resolve
- Quem são os usuários principais
- Por que esse problema é relevante

> Atenção: evite domínios extremamente genéricos (ex: "rede social") sem delimitação clara de escopo.

**Resposta:**

O sistema proposto é um aplicativo gerenciador de tarefas para o jogo Animal Crossing. O domínio é entretenimento assistido por produtividade, voltado a jogadores que possuem rotinas cheias e desejam gerenciar sua ilha de forma eficiente sem depender de memória ou anotações externas.
O jogo impõe ciclos diários e sazonais rígidos: coletas, construções, eventos e interações com NPCs, que expiram caso o jogador não os execute dentro de janelas específicas. Jogadores com pouco tempo disponível perdem progressão por falta de visibilidade sobre o que está pendente. O sistema resolve esse problema centralizando e priorizando as tarefas in-game de acordo com urgência e preferências do usuário. Além disso, o aplicativo contará com um preditor dos preços de turnip, baseado em um modelo preditivo, para que os jogadores sejam capazes de maximizar o seu lucro vendendo-as. Como diferencial, o aplicativo também contará com um matcher de villagers e jogador, que traçará o perfil do usuário e o combinará com um catálogo de villagers que possuem as personalidades mais adequadas ao seu perfil.

---

## Tarefa 1.2 — Planejamento de Entrevista (15 min)

Elabore um roteiro de entrevista semiestruturada com:
- Objetivo da entrevista (1 parágrafo)
- Pelo menos 8 perguntas, sendo:
  - No mínimo 3 perguntas abertas voltadas à compreensão do problema
  - No mínimo 2 perguntas que explorem fluxos de trabalho ou rotinas do usuário
  - No mínimo 2 perguntas que investiguem frustrações ou limitações com soluções atuais
  - No mínimo 1 pergunta de encerramento

**Objetivo:** Validar se o projeto atende a dores reais do público-alvo, bem como avaliar quais features seriam mais importantes.

1. Você sente falta de um aplicativo centralizado para controlar o seu progresso no jogo?
2. Quais features você gostaria de ter em um aplicativo do gênero?
3. O que te impede de jogar Animal Crossing de forma mais eficiente?
4. O que você costuma fazer diariamente no jogo?
5. Você se lembra de tudo que fez e/ou está pendente dentro do jogo?
6. Do que você sente falta em soluções atuais?
7. Você já utilizou ferramentas similares? Se sim, quais?
8. Há alguma pergunta omitida ou algo que você gostaria de sugerir para o app?

**Minha reflexão:** Acredito que as soluções disponíveis atualmente são bastante limitadas, por isso, seria importante validar a prospecto e o escopo da ideia com usuários em potencial. Os aplicativos disponíveis não possuem todas as features desejadas por mim, como jogador. 

---

## Tarefa 1.3 — Histórias de Usuário (20 min)

Escreva exatamente 5 histórias de usuário no formato:
> Como [perfil de usuário], quero [ação/funcionalidade] para [benefício/objetivo].

Para cada história, inclua:
- Critérios de aceitação (mínimo 3)
- Prioridade: Alta / Média / Baixa, com justificativa de 1 a 2 frases

**H1:** Como jogador com agenda limitada, quero ser notificado sobre eventos sazonais com antecedência para não perder datas que expiram.

- O sistema notifica o usuário com antecedência configurável (ex: 1 dia, 1 hora)
- Os eventos exibidos correspondem ao calendário oficial do jogo
- O usuário consegue dispensar ou adiar uma notificação

**Prioridade:** Alta. Eventos sazonais são irreversíveis; perdê-los representa perda permanente de progressão, o que é o problema central da proposta.

---

**H2:** Como jogador que negocia turnips, quero visualizar uma previsão de preços para a semana para decidir o melhor momento de venda.
- O usuário consegue inserir os preços observados ao longo da semana
- O sistema exibe uma projeção de preços para os dias restantes
- A projeção indica o intervalo de valores possíveis, não um valor único

**Prioridade:** Alta. Diferencial direto do produto; impacta jogadores que já têm intenção de otimizar lucro in-game.

---

**H3:** Como jogador que abre o jogo diariamente, quero visualizar as tarefas recorrentes do dia para concluí-las sem esquecer nenhuma.
- O sistema exibe apenas tarefas disponíveis na data atual
- Tarefas concluídas podem ser marcadas e são ocultadas ou destacadas visualmente
- A lista é atualizada automaticamente às 5 AM, respeitando o ciclo do jogo

**Prioridade:** Alta. Funcionalidade de uso diário; base de retenção do aplicativo.

---

**H4:** Como jogador que deseja montar sua ilha, quero receber sugestões de villagers compatíveis com meu perfil para tomar decisões de forma orientada.
- O sistema apresenta um questionário de perfil ao usuário
- As sugestões exibem nome, personalidade e características relevantes de cada villager
- O usuário pode filtrar sugestões por critérios adicionais (ex: espécie, personalidade)

**Prioridade:** Média. Agrega valor como diferencial, mas não compromete o uso do aplicativo se ausente.

---

**H5:** Como jogador ativo, quero gerar um resumo do meu progresso na ilha para compartilhar externamente.
- O sistema consolida dados de progresso registrados pelo usuário em um resumo visual
- O resumo pode ser exportado como imagem ou link
- O conteúdo exibido é configurável pelo usuário antes de compartilhar

**Prioridade:** Baixa. Funcionalidade social sem impacto no fluxo principal; removível sem afetar as demais histórias.

**Minha reflexão:** As reflexões apresentam perfis variados de jogadores, bem como destacam possíveis diferenciais do produto e forma de reter usuários. Talvez a prioridade de história 5 deva ser reavaliada para cima, já que hoje em dia features como essa podem servir como uma forma de divulgar o app boca a boca, organicamente.

---

## Tarefa 1.4 — Validação de Requisitos (15 min)

Escolha 2 histórias e verifique:
- Ambiguidades nos critérios de aceitação
- Conflitos potenciais com outras histórias
- Informações que precisam ser elucidadas com o usuário

**História escolhida: H3**
- Ambiguidades: Quais são as tarefas diárias? 
- Conflitos: O que diferencia esta história de H1? 
- Pontos a elucidar: Diferentes usuários podem priorizar diferentes tarefas. Há forma de escolher?

**História escolhida: H4**
- Ambiguidades: O que define se um villager é compatível com o perfil do jogador? Isso satisfaria o usuário final?
- Conflitos: Nenhum conflito entre outras histórias.
- Pontos a elucidar: O usuário quer fazer o questionário e receber quantas sugestões? Como seria o questionário?

**Revisão crítica:** Qual história você removeria se o escopo fosse reduzido pela metade? Justifique em 2 a 3 frases.

Eu removeria as histórias 2 e 4. Dessa forma, o app tornaria-se apenas um gerenciador de tarefas comum, sem ter essas features de predição como diferencial. Tornaria a implementação bem mais fácil.

...