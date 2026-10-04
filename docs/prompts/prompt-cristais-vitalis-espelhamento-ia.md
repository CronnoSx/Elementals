# Prompt: Sistema de Cristais + Vitalis + Espelhamento + IA

> Cole tudo abaixo no Claude junto com o arquivo `panel-attack.html` atual.

---

Olá! Vou te enviar o arquivo `panel-attack.html`, que é o meu jogo **Panel Attack – Edição Elemental**, um puzzle de navegador inspirado em Tetris Attack / Panel de Pon, feito em HTML/CSS/JS puro (sem frameworks).

Quero que você implemente o sistema de **Cristais**, o modo **Espelhamento** e a **IA**, e renomeie um bioma para **Vitalis**. Leia todas as regras abaixo antes de começar.

## 1. Contexto do jogo (o que já existe e deve continuar funcionando)

- Grade de **7 colunas x 14 linhas**, cursor de **2 casas**, trocas **horizontais**.
- Matches de **3 ou mais** painéis iguais, **chains** (combos em cascata), pilha que **sobe** continuamente.
- Velocidade aumenta com o tempo até o **"MODO FRENÉTICO"** aos 5:00.
- **Turbo** (subir a pilha manualmente) e **pausa**.
- **6 elementos**: Água, Fogo, Terra, Ar, Planta, Orgânico.
- Fases internas do jogo: `IDLE → SWAPPING → FALLING → CLEARING → IDLE`, e `GAME_OVER`.
- **Campanha**: escolha de gênero, personagens 1–8 femininos / 9–16 masculinos (`characters/char_01..16.png`), nome do herói, mapa com 6 biomas (todos jogam o modo Endless por enquanto).
- Sons em `sounds/*.wav`.
- Configurações salvas em `localStorage`: `panelAttack.settings`, `panelAttack.bindings`, `panelAttack.hero`.
- Controles por teclado com remapeamento (e suporte a gamepad).

**Importante:** mantenha **todas** as funcionalidades existentes. Não remova nem simplifique nada que já funciona, a não ser que eu peça explicitamente.

## 2. Sistema de Cristais (regras finais)

Cristais são o "ataque" do jogo: ao fazer boas jogadas, o jogador envia cristais para o tabuleiro do adversário.

### 2.1 Janela de combo
- A janela de combo é de **1,8 segundos**.
- A janela começa (ou reinicia) a cada clear que gera cristal.
- Enquanto o jogador fizer novos clears válidos (4+) **dentro de 1,8s** do clear anterior, o combo continua.
- Se passar 1,8s sem um novo clear válido, o combo fecha e o cristal é **enviado** ao adversário.
- Use um valor configurável no código, por exemplo `CRYSTAL_COMBO_WINDOW_MS = 1800`.

### 2.2 Quando um clear gera cristal
- **Clear de 4 ou mais painéis** do mesmo elemento: **gera cristal**.
- **Clear de 3 painéis**: **não gera cristal**, com uma única exceção:
  - **"Eco"**: se o clear de 3 acontecer **apenas por gravidade** (peças caíram e formaram o match sozinhas, sem uma troca do jogador naquele momento, ou seja, como consequência de outro movimento anterior), ele conta como **eco** e envia um **cristal pequeno**.
  - Para detectar isso, marque cada match com a origem: `swap` (formado imediatamente pela troca do jogador) ou `gravity` (formado após painéis caírem). Um clear de 3 com origem `swap` nunca gera cristal.
- Chains continuam funcionando como hoje (pontuação etc.). Elas só influenciam os cristais pelas regras acima.

### 2.3 Crescimento do cristal
- O primeiro clear válido cria um **cristal pendente** (ainda não enviado), mostrado num indicador perto do tabuleiro do jogador.
- Cada novo clear de 4+ **dentro da janela de 1,8s** **aumenta o tamanho** do cristal pendente.
- Sugestão de tamanho (deixe em constantes fáceis de ajustar):
  - Eco (3 por gravidade): cristal **pequeno**, 1 linha x 3 colunas.
  - Clear de 4: 1 linha x 4 colunas.
  - Clear de 5: 1 linha x 5 colunas.
  - Clear de 6+: 1 linha x 6 colunas.
  - Cada clear 4+ adicional dentro da janela: **+1 linha** de altura (máximo de 4 linhas).
- O elemento do cristal é o elemento do **primeiro** clear que o criou (pode ser mostrado com a cor/ícone do elemento).
- Quando a janela fecha, o cristal é enviado e o indicador zera.

### 2.4 Cristal no tabuleiro de quem recebe
- O cristal cai no topo do tabuleiro adversário como um **bloco único** (ocupa várias casas, como os "garbage blocks" do Panel de Pon).
- Ele obedece à gravidade e sobe junto com a pilha.
- Não pode ser trocado pelo cursor.
- Visual: aparência cristalina e translúcida, com a cor do elemento dele, brilho suave. Deve ser fácil de distinguir dos painéis normais.

### 2.5 Quebra do cristal
- O cristal **quebra inteiro de uma vez** quando um match **do elemento correto** (o mesmo elemento do cristal) acontece **encostado** nele (algum painel do match adjacente na horizontal ou vertical a qualquer casa do cristal).
- Matches de outro elemento não afetam o cristal.
- Ao quebrar, **todas** as casas do cristal viram **painéis normais de elementos aleatórios**, que então caem com a gravidade (e podem formar novos matches/chains).
- Animação de quebra com partículas de cristal e um som próprio (pode reaproveitar/gerar um som no estilo dos existentes).

### 2.6 Cancelamento (opcional, mas recomendado)
- Se o jogador tiver cristais **chegando** (já enviados pelo adversário, ainda não caíram) e fizer um clear que gera cristal, o cristal novo primeiro **cancela** o que está chegando, e só o restante é enviado.
- Mostre um pequeno aviso de "cristal chegando" acima do tabuleiro antes de ele cair (por exemplo, ~1 segundo de antecedência).

## 3. Vitalis (renomear bioma)

- **Vitalis** é apenas o novo nome do bioma **"Fungos"** (bioma do elemento Orgânico) no mapa da Campanha.
- Troque o nome em todos os lugares onde ele aparece (mapa, textos, títulos, telas de fase). Não mude as regras nem o visual do bioma além do nome.
- Se algum dado salvo no `localStorage` usar o nome antigo, mantenha compatibilidade para não perder o progresso.

## 4. Espelhamento (modo versus)

- Novo modo **Versus** com **dois tabuleiros lado a lado**: jogador à esquerda e adversário à direita, espelhados na tela.
- Os dois tabuleiros começam com a **mesma semente** de geração de painéis (mesmas peças iniciais e mesmas linhas novas), para a disputa ser justa.
- Cada lado tem seu próprio HUD: personagem, nome, indicador de cristal pendente e aviso de cristal chegando.
- Cristais enviados por um lado caem no tabuleiro do outro.
- Vence quem fizer a pilha do adversário estourar no topo (game over dele) primeiro. Mostre tela de vitória/derrota com opção de jogar de novo ou voltar ao menu.
- O layout precisa caber na tela; em telas estreitas os tabuleiros podem ser reduzidos.

## 5. IA (adversário controlado pelo computador)

- No modo Versus, o tabuleiro da direita é controlado por uma **IA**.
- A IA joga com as **mesmas regras** que o jogador: move o cursor casa por casa (sem teletransporte), faz trocas, faz matches, chains, envia e recebe cristais, e quebra cristais com o elemento certo.
- A IA deve procurar jogadas boas: priorizar clears de 4+, montar chains simples, quebrar cristais que estão no tabuleiro dela e fugir do topo quando estiver em perigo.
- **3 níveis de dificuldade**: Fácil, Normal e Difícil, variando velocidade de ação (tempo entre movimentos), chance de erro e profundidade de busca.
- Na campanha, o adversário de cada bioma pode usar um dos outros personagens (escolhido aleatoriamente entre os 16, exceto o do jogador).
- A IA não pode "ver o futuro" (não pode usar as próximas linhas que ainda não apareceram).

## 6. Menus e integração

- Adicione no menu principal a opção **Versus vs IA**, com escolha de dificuldade.
- Mantenha o modo Endless/solo e a campanha funcionando.
- Salve a última dificuldade escolhida em `panelAttack.settings`.
- Pausa deve pausar os dois tabuleiros.

## 7. Entrega

- Me envie o **código completo** em um **único arquivo HTML** (`panel-attack.html`), pronto para substituir o atual. Não mande só trechos ou diffs.
- Mantenha todos os sons, personagens, controles, configurações e funcionalidades existentes.
- Deixe as regras ajustáveis em constantes bem nomeadas no topo do script (janela de combo, tamanhos de cristal, dificuldades da IA).
- No final, faça um resumo curto do que foi implementado e de como testar cada sistema.

## 8. Suposições que fiz (ajuste se quiser)

Espelhamento e IA ainda não tinham regras fechadas, então defini assim:

1. **Espelhamento** = modo versus com dois tabuleiros espelhados lado a lado, com a mesma semente de painéis.
2. **IA** = adversário controlado pelo computador, com 3 dificuldades, que também envia e quebra cristais.
3. Tamanhos de cristal (1x3 eco, 1x4 a 1x6, +1 linha por clear extra, até 4 linhas) e o cancelamento de cristais são sugestões minhas.
4. O cristal "encostado" quebra por adjacência horizontal ou vertical ao match do elemento correto.

Se algo aqui não fizer sentido com o código atual, me avise antes de mudar e explique a alternativa.
