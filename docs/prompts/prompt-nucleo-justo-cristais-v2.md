# Prompt: Núcleo justo + Cristais v2

> Cole tudo abaixo no Claude Code, com o repositório `cronnosx/another-x-indie-experience` aberto.

---

Olá! Este repositório tem o meu jogo de puzzle de navegador no arquivo `panel-attack.html`. É um jogo de troca de blocos com 6 elementos, feito em HTML/CSS/JS puro, sem frameworks. O resto do repositório (`index.html`, `script.js`, `style.css`, "Axie Desert Rush") é **outro projeto**. Não mexa nele.

Trabalhe na branch `claude/bold-clarke-o2zvt6`.

Quero deixar o jogo **justo e de habilidade** antes de partir para o online. Leia tudo antes de começar e confira no código o que já existe.

## 0. Regras gerais

- **Mantenha todas as funcionalidades existentes**: campanha (gênero, 16 personagens, nome, mapa com 6 biomas), Endless, MODO FRENÉTICO, turbo, pausa, sons, controles remapeáveis, gamepad, configurações em `localStorage` (`panelAttack.settings`, `panelAttack.bindings`, `panelAttack.hero`). O versus contra IA, a campanha com partidas versus e os cristais já existem (commit `2d21a35`): mantenha tudo e aplique as mudanças abaixo.
- O jogo continua sendo **um único arquivo HTML** (`panel-attack.html`), com os sons e personagens nas pastas atuais.
- Coloque cada valor ajustável numa **constante bem nomeada** no topo do script.
- Não renomeie as chaves do `localStorage`, para ninguém perder o progresso.

## 1. Identidade (sem nomes de terceiros)

- Remova de **todos os textos visíveis** (título da aba, tela inicial, menus, créditos) as palavras "Tetris", "Panel de Pon", "Tetris Attack" e "Panel Attack".
- Crie uma constante `GAME_TITLE` e use-a em todos os lugares onde o nome do jogo aparece. Por enquanto, o valor é `"Edição Elemental"`. Eu escolho o nome definitivo depois.
- Não renomeie o arquivo `panel-attack.html` agora.

## 2. Núcleo justo e de habilidade

### 2.1 Troca durante quedas e limpezas (prioridade máxima)
- Hoje o jogador fica travado enquanto o tabuleiro está em `FALLING` ou `CLEARING`. Isso tem que acabar: as trocas devem funcionar **a qualquer momento**, como no gênero original.
- Regras por painel, não pelo tabuleiro inteiro:
  - Um painel que está **sumindo** (animação de clear) não pode ser trocado.
  - Um painel **parado** pode ser trocado com outro parado ou com um espaço vazio, mesmo enquanto outras colunas estão caindo ou limpando.
  - Trocar um painel com um espaço vazio que tem um painel **caindo logo acima** não é permitido nesse instante (evita sobreposição).
  - Um painel trocado para cima de um buraco começa a cair depois da troca.
- Isso provavelmente exige que cada painel tenha o próprio estado (`idle`, `swapping`, `falling`, `clearing`) em vez de uma fase global. Faça essa refatoração com cuidado.
- **Cadeias continuam contando:** um painel que caiu porque algo embaixo sumiu continua marcado como "parte da cadeia" até parar. Se ele formar um match ao parar, ou logo depois de ser trocado pelo jogador ainda nesse estado, a cadeia sobe (x2, x3...). Isso é o que permite montar cadeias "ao vivo" (skill chains).

### 2.2 Pausa da pilha (stop time)
- Depois de um combo (4+) ou de uma cadeia (x2+), a pilha **para de subir** por um tempo.
- Sugestão: `STOP_TIME_COMBO_MS = 1000 + 150 * (painéis - 4)` e `STOP_TIME_CHAIN_MS = 1500 * (elos da cadeia - 1)`. Novos stops **somam** ao que falta, até `STOP_TIME_MAX_MS = 8000`.
- Mostre um contador visual pequeno ao lado do tabuleiro enquanto o stop time estiver ativo.
- O turbo (subir manualmente) cancela o stop time restante.

### 2.3 Tempo de graça no topo
- Quando a pilha encosta no topo, o jogador **não perde na hora**: a pilha para e começa um tempo de graça de `GRACE_TIME_MS = 1500`.
- Durante a graça, o tabuleiro pisca/treme e toca um som de perigo. Se o jogador limpar painéis e abrir espaço, a graça zera.
- O jogador só perde se a pilha precisar subir de novo sem espaço.
- Stop time ativo também impede o game over.

### 2.4 Turbo (subida manual)
- Confira se o turbo já sobe a pilha **imediatamente** e de forma contínua enquanto o botão estiver pressionado. Se não, ajuste.
- O turbo **não** funciona durante o tempo de graça (evita suicídio sem querer).

### 2.5 Sequência determinística (semente)
- Todo sorteio de painéis (tabuleiro inicial, novas linhas, painéis que surgem de cristais quebrados) deve usar um **gerador aleatório com semente** (por exemplo, mulberry32), nunca `Math.random()`.
- Cada tabuleiro tem o próprio gerador. No versus, os dois começam com a **mesma semente**, para os dois jogadores receberem as mesmas peças.
- Efeitos puramente visuais (partículas) podem continuar usando `Math.random()`.
- Isso prepara o jogo para replays e para o ranqueado online no futuro: mesma semente + mesmas jogadas = mesmo resultado.

### 2.6 Quantidade de elementos
- O padrão continua **6 elementos em todos os modos**, inclusive Versus e campanha. O competitivo é com 6.
- Crie a constante `ELEMENTS_COUNT_DEFAULT = 6` e uma opção extra **"Iniciante"** só no Endless e no Versus contra IA Fácil, que usa 5 elementos (`ELEMENTS_COUNT_BEGINNER = 5`). Ela serve para quem está aprendendo. Não use 5 em nenhum outro lugar.

## 3. Cristais v2 (sistema de lixo/ataque)

Se o sistema de cristais ainda **não existir** no código, implemente-o com todas as regras abaixo. Se já existir, ajuste para ficar assim.

### 3.1 Como o ataque é gerado
- **Janela de combo:** `CRYSTAL_COMBO_WINDOW_MS = 1800`. Clears que geram cristal dentro dessa janela se somam num **cristal pendente**, que aparece num indicador ao lado do tabuleiro. Quando a janela fecha, o cristal é enviado.
- **Combo** (um clear de 4+ painéis de uma vez) gera um cristal **largo e baixo**:
  - 4 painéis: 1 linha x 3 colunas
  - 5 painéis: 1 x 4
  - 6 painéis: 1 x 5
  - 7+ painéis: 1 x 7 (a largura inteira)
- **Cadeia** (clears em sequência pela gravidade, x2, x3...) gera um cristal **alto, da largura inteira (7 colunas)**:
  - x2: 1 linha de altura
  - x3: 2 linhas
  - cada elo a mais: +1 linha, até `CRYSTAL_MAX_HEIGHT = 8`
- Um clear de 3 simples, feito pela troca do jogador, **não gera cristal**. Um clear de 3 que é um elo de cadeia gera, pelas regras de cadeia.
- Se combo e cadeia acontecerem na mesma janela, envie os dois como cristais separados (o largo primeiro).
- O elemento do cristal é o do clear que o criou. Numa cadeia, use o elemento do **último** elo.

### 3.2 Aviso e cancelamento
- Cristais enviados não caem na hora: ficam numa **fila visível acima do tabuleiro de quem vai receber**, mostrando tamanho e elemento de cada um, por `CRYSTAL_DROP_DELAY_MS = 1500`.
- Se quem vai receber gerar um cristal enquanto há cristais na fila dele, o novo **cancela primeiro** os da fila (casa por casa). Só a sobra é enviada ao adversário.
- Cristais da fila só caem quando o tabuleiro de quem recebe não está no meio de uma cadeia.

### 3.3 Cristal no tabuleiro
- Cai no topo como **bloco único**, obedece à gravidade, sobe junto com a pilha e não pode ser trocado.
- Visual cristalino e translúcido, com a cor e o ícone do elemento.

### 3.4 Quebra (com rede de segurança)
- Um match **do mesmo elemento do cristal** encostado nele (adjacência horizontal ou vertical) **quebra o cristal inteiro**.
- Um match de **qualquer outro elemento** encostado nele quebra **só a linha de baixo** do cristal.
- As casas quebradas viram **painéis normais** (sorteados pelo gerador com semente do tabuleiro). Eles ficam um instante parados e depois caem, e podem formar matches que **contam como cadeia**.
- Cristais encostados um no outro que sejam do mesmo elemento quebram juntos (efeito dominó).
- Animação de partículas de cristal e um som de quebra.

## 4. Correções encontradas na revisão do código atual

Uma revisão do commit `2d21a35` achou estes problemas. Corrija todos:

- **Novo conjunto de elementos e biomas (decisão de design):**
  - O elemento **Orgânico sai do tabuleiro** e entra o **Metal**. As 6 pedras passam a ser: **Água, Fogo, Terra, Ar, Planta e Metal**.
  - Visual provisório do Metal: prata frio levemente azulado, polido, com brilho forte, e ícone de lingotes escuros. Ele precisa ser bem diferente da Terra, que deve ficar **marrom/ocre e fosca** (ajuste a cor da Terra se hoje ela for cinza). A arte final dos blocos vem depois, como imagens.
  - Os 6 biomas iniciais do mapa passam a ser um por pedra: **Água, Fogo, Terra, Ar, Floresta (Planta) e Metal**. O bioma de **Água é novo** e entra no lugar do Vitalis.
  - O **Vitalis** sai do mapa por enquanto. Ele volta no futuro como subbioma (evolução da Floresta). Não apague os dados dele do código, só deixe ele fora do mapa.
  - Progresso salvo: quem já tinha avançado no Vitalis ganha esse progresso no bioma de Água. Nada pode quebrar com saves antigos que ainda tenham o elemento Orgânico.
  - Cristais, IA, sons e textos que citam Orgânico passam a usar Metal.
  - **Imagem do bloco de Metal:** junto com este prompt vai anexada a imagem `tile-metal-v2-512.png`. Salve ela no repositório (por exemplo em `tiles/metal.png`, junto das imagens dos outros blocos, se já existirem) e use-a para desenhar o bloco de Metal no tabuleiro, no mesmo tamanho e do mesmo jeito que os outros blocos. Se os outros blocos ainda forem desenhados em código, use a imagem só no Metal por enquanto, e aplique nela os mesmos efeitos dos outros (linha nova escurecida, brilho ao sumir).
- **Cristal alto que mata sem a pilha estar no topo:** hoje um cristal de altura `h` só entra se as `h` primeiras linhas do topo estiverem livres, e se não couber por 2 s é game over. Mude: o cristal entra **pelo topo, linha por linha**, ocupando o espaço que houver. Só conta como perigo/game over pelas regras do tempo de graça (item 2.3), nunca por "não caber".
- **Cancelamento arredondando para cima:** em `sendCrystal`, um cristal de 3 casas cancela uma linha inteira de 6. O cancelamento deve ser **casa por casa**: 3 casas cancelam 3 casas. Se sobrar uma linha incompleta no cristal que estava chegando, ela continua na fila com a largura que restou.
- **Eco só conta sem cristal pendente:** uma cadeia x5 de trincas manda só 1x3. Com as regras de cadeia do item 3.1, cada elo conta sempre, haja cristal pendente ou não.
- **Efeitos visuais gastando a semente:** `spawnShards` usa `state.rng`. Partículas e efeitos visuais devem usar `Math.random()`, e o gerador com semente fica só para a lógica do jogo (item 2.5).
- **IA Difícil tímida:** num teste de 40 s ela fez 520 pontos, mandou 2 cristais e ficou 10 s sem pontuar. Depois do v2, ajuste a IA para usar as novas mecânicas (trocar durante quedas para estender cadeias, buscar cadeias x2/x3 no Difícil, aproveitar o stop time) e para não ficar parada quando existe jogada disponível.

## 5. Teste e entrega

- Teste no navegador headless (Playwright, o Chromium já vem instalado) antes de entregar. Comprove pelo menos:
  1. Trocar painéis enquanto outra coluna está caindo.
  2. Uma cadeia x2 montada "ao vivo", com troca durante a queda.
  3. O stop time segurando a pilha.
  4. Tempo de graça: encostar no topo e se salvar.
  5. Mesma semente gerando as mesmas peças nos dois tabuleiros do versus.
  6. Um cristal largo e um alto sendo enviados, o cancelamento e as duas formas de quebra.
  7. Cristal alto entrando com a pilha pela metade sem matar, e cancelamento casa por casa.
  8. As 6 pedras novas (com Metal) no tabuleiro e os 6 biomas no mapa, incluindo o de Água.
  9. A campanha, o Endless, os controles e as configurações continuando a funcionar.
- Faça commit e push para a branch `claude/bold-clarke-o2zvt6`.
- No final, me mande um resumo curto em português do que mudou e de como testar cada item jogando, e liste as constantes que eu posso ajustar.
- Se alguma regra daqui não fizer sentido com o código atual, explique a alternativa antes de mudar.
