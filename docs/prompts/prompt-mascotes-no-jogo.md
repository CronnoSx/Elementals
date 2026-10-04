# Prompt: Mascotes no jogo (com animações)

> Cole tudo abaixo no Claude Code, com o repositório `cronnosx/another-x-indie-experience` aberto. As imagens já estão no repositório, então não precisa anexar nada.

---

Olá! Este repositório tem o meu jogo de puzzle de navegador no arquivo `panel-attack.html`. O resto do repositório (`index.html`, `script.js`, `style.css`, "Axie Desert Rush") é **outro projeto**. Não mexa nele.

Trabalhe na branch `claude/bold-clarke-o2zvt6` e puxe a versão mais recente antes de começar.

Quero colocar os **mascotes** no jogo, com animações. Leia tudo antes de começar.

## 0. Regras gerais

- **Mantenha tudo que já existe funcionando**: campanha, Endless, Versus contra IA, cristais, stop time, tempo de graça, sons, controles, gamepad, configurações e saves no `localStorage`.
- Continua sendo **um único arquivo HTML** (`panel-attack.html`). As imagens ficam em `mascots/`.
- **Os mascotes são só visuais.** Eles não mudam nenhuma regra, velocidade, pontuação ou cristal. Isso vale em todos os modos, principalmente no Versus.
- Coloque os valores ajustáveis (tempos e tamanhos das animações) em constantes bem nomeadas.

## 1. As imagens (já estão no repositório)

Cada mascote tem uma pasta em `mascots/<id>/` com imagens `.webp` de fundo transparente:

- `full.webp`: corpo inteiro, a pose principal
- `happy.webp`, `angry.webp`, `scared.webp`, `celebrate.webp`: expressões (só a cabeça, ou meio corpo)
- alguns também têm `side.webp` ou `front.webp` (extras, não são obrigatórios)

| Bioma (id) | Mascote | Pasta | Personalidade (para as animações) |
|---|---|---|---|
| Água (`water`) | Gotico | `mascots/gotico/` | brincalhão e curioso, corpo de água gelatinoso |
| Fogo (`fire`) | Fornalinho | `mascots/fornalinho/` | esquentadinho e corajoso, tem fogo na barriga |
| Terra (`earth`) | Seixo | `mascots/seixo/` | calmo, sonolento e leal, pesado |
| Ar (`air`) | Brisa | `mascots/brisa/` | leve e alegre, sempre flutuando |
| Floresta (`forest`) | Bonsai | `mascots/bonsai/` | sábio e paciente, lento |
| Metal (`metal`) | Rebite | `mascots/rebite/` | orgulhoso e meio rabugento, de corda |

Crie uma lista `MASCOTS` com id, nome, bioma, pasta e personalidade. Pré-carregue as imagens. Se alguma faltar, mostre um marcador simples no lugar, sem quebrar o jogo.

## 2. Como o jogador ganha mascotes (campanha)

- No começo, o jogador **não tem mascote**.
- Na campanha, o adversário de cada bioma vem **acompanhado do mascote daquele bioma**.
- Ao **vencer** a partida de um bioma pela primeira vez, o jogador **conquista** o mascote dele. Mostre uma telinha curta de "Novo mascote!" com a imagem `celebrate`, o nome e uma frase curta de apresentação.
- O mascote conquistado fica **selecionado automaticamente** se o jogador ainda não tinha nenhum.
- Salve em `panelAttack.hero`, sem quebrar saves antigos: `mascots: ["fire", ...]` (biomas conquistados) e `mascot: "fire"` (o selecionado, ou `null`).
- No **mapa**, mostre em cada bioma um ícone pequeno do mascote: colorido se já foi conquistado, ou como silhueta escura se ainda não foi.

## 3. Tela de mascotes

- Adicione no menu principal a opção **Mascotes**.
- Ela mostra os 6 mascotes em grade. Os conquistados aparecem com nome, bioma e a animação de "parado". Os não conquistados aparecem como silhueta, com o texto "Vença o bioma X para conquistar".
- O jogador escolhe qual mascote acompanha ele (ou "nenhum"). Funciona com teclado, gamepad e toque, como o resto dos menus.

## 4. Onde o mascote aparece na partida

- **Versus e campanha:** o mascote fica ao lado do personagem, no HUD de cada tabuleiro (`.board-hud` / `.hud-art`), um pouco maior que o personagem e virado para o centro da tela. O mascote do adversário (IA) fica do lado dele.
- **Endless:** o mascote do jogador fica ao lado do tabuleiro.
- **Adversário:** na campanha, a IA usa o mascote do bioma. No Versus contra IA fora da campanha, ela usa um mascote aleatório, diferente do mascote do jogador.
- **Telas estreitas (celular):** hoje o `.hud-art` some. Nelas, mostre só o mascote, em versão pequena, para ele não sumir.

## 5. Animações

Faça tudo com CSS (keyframes e transform) e troca de imagem. Nada pesado.

### 5.1 Parado (idle), sempre rodando, cada um com o seu jeito
- **Gotico:** balança mole, como gelatina (scale X/Y alternando de leve).
- **Fornalinho:** pulinhos curtos e impacientes, com um brilho laranja pulsando atrás dele (drop-shadow).
- **Seixo:** respiração lenta e funda, quase parado.
- **Brisa:** flutua para cima e para baixo, com uma sombra no chão que cresce e diminui.
- **Bonsai:** balança devagar de um lado para o outro, como árvore no vento.
- **Rebite:** pequenos "tiques" de corda (gira 2 a 3 graus e volta em passos), com um brilho azul piscando de vez em quando.

### 5.2 Reações aos eventos do jogo

Ao reagir, o mascote troca a imagem para a expressão indicada, faz uma animação curta e depois volta para `full` + idle.

| Evento | Expressão | Animação | Duração |
|---|---|---|---|
| Combo de 4+ ou cadeia x2 | `happy` | pulinho | ~0,8 s |
| Cadeia x3 ou mais | `celebrate` | pulo maior com giro curto, e um "x3!" pequeno saindo dele | ~1,2 s |
| Enviar um cristal para o adversário | `angry` | avança na direção do adversário e volta (investida) | ~0,7 s |
| Receber um cristal (quando ele cai) | `scared` | tremida rápida | ~0,6 s |
| Quebrar um cristal | `happy` | pulinho | ~0,8 s |
| Pilha em perigo (perto do topo) / tempo de graça | `scared` | tremida contínua enquanto durar o perigo | contínua |
| Vitória | `celebrate` | pulos em loop | até sair da tela |
| Derrota | `scared` | encolhe e cai um pouco | fica assim |

- **Prioridade**, quando duas coisas acontecem juntas: vitória/derrota > perigo > cadeia x3+ > enviar cristal > receber cristal > combo/cadeia x2 > quebrar cristal. Uma reação nova de prioridade menor não interrompe uma maior que ainda está tocando.
- As reações valem para os **dois lados** do Versus: o mascote da IA reage às jogadas da IA.
- Na **pausa**, as animações param.
- Respeite `prefers-reduced-motion`: nesse caso, só troque a expressão, sem pulos ou tremidas.
- Use os pontos do código que já disparam os sons desses eventos (`Sound.play(...)` de chain, cristal, warning, vitória e game over) para disparar as reações, em vez de duplicar a lógica.

## 6. Teste e entrega

- Teste no navegador headless (Playwright, o Chromium já vem instalado). Comprove pelo menos:
  1. Vencer um bioma da campanha conquista o mascote dele, e ele aparece no mapa e na tela de Mascotes.
  2. Escolher e trocar de mascote na tela de Mascotes, e a escolha continuar salva ao recarregar a página.
  3. O mascote aparece ao lado do tabuleiro no Endless, no Versus e na campanha, com o do adversário do outro lado.
  4. Cada reação da tabela 5.2 troca a expressão e anima (pode forçar os eventos por código no teste).
  5. Pausa congela as animações.
  6. Saves antigos sem `mascots` carregam sem erro.
  7. Tudo que já existia continua funcionando, sem erros no console.
- Tire screenshots do Versus com os dois mascotes e da tela de Mascotes, e me mostre.
- Faça commit e push para a branch `claude/bold-clarke-o2zvt6`.
- No final, me mande um resumo curto em português do que mudou, de como testar jogando e de quais constantes eu posso ajustar.
- Se alguma coisa daqui não fizer sentido com o código atual, explique a alternativa antes de mudar.
