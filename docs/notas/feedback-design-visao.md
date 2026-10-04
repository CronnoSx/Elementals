# Feedback sincero de design: visão, jogabilidade, PvP, venda e roadmap

_Escrito em 04/10/2026, com base na memória do projeto e no protótipo atual (grade 7x14, 6 elementos, campanha com 6 biomas, sistema de cristais combinado)._

## 1. O que eu entendi da visão

- **Agora:** um jogo de puzzle vendável, estilo "troca de blocos" (inspirado em Panel de Pon), com **PvP ranqueado online** + **single player com progressão**.
- **Depois:** sensação de progressão por customização de personagem e um **globo de neve próprio** para cada jogador (arte estilo It Takes Two). Algo tipo Clash of Clans fica como "talvez".
- **Arquivado:** MMO, guildas, conquista de castelos.
- **Restrições reais:** você não programa, constrói tudo com o Claude, hospeda estático no GitHub Pages, prefere mecânica sólida antes de arte e multiplayer, e precisa que dê dinheiro.

Acho a direção certa. O MMO seria um projeto de anos; um puzzle competitivo bem feito é um escopo que dá para terminar.

## 2. Copyright e identidade (resolver primeiro, custa pouco)

Mecânica de jogo não tem copyright. O que dá problema é **nome, marca e "trade dress"** (aparência que imita o original). O caso Tetris Holding vs. Xio (2012) perdeu justamente por copiar o visual.

- **Tirar "Tetris" de tudo:** nome do projeto, título, textos. "Tetris" é marca registrada e a Tetris Company processa ativamente.
- **Evitar "Panel de Pon", "Tetris Attack" e também "Panel Attack"** (esse último já é o nome de um jogo fã open-source conhecido). O arquivo `panel-attack.html` pode virar outro nome quando tivermos o título.
- **Visual próprio:** os elementos ajudam muito aqui. Blocos com ícones de Água/Fogo/Terra etc. já se afastam das cores/formas do original. Evitar copiar o layout da tela do SNES, o cursor exato, os sons e as músicas.
- **Personagens:** confirme de onde veio o `reference_sheet.webp`. Se foi gerado por você com IA, tudo bem, mas a Steam exige declarar conteúdo gerado por IA na página da loja. Se veio de outro artista ou de outro jogo, não dá para vender com ele.
- **Ideias de nome** (checar disponibilidade antes): _Elementa_, _Globo Elemental_, _Snowglobe Clash_, _Vitralis_, _Swap Realms_. Gosto de algo que amarre "globo" + "elementos", porque isso vira a sua marca.

## 3. Jogabilidade: o que faz um puzzle competitivo ser justo e de habilidade

Em ordem de importância:

1. **Trocar blocos durante quedas e limpezas** (está no backlog). Isso é *o* coração da habilidade no gênero: é o que permite montar cadeias "ao vivo" (skill chains) em vez de só pré-montar. Sem isso, o teto de habilidade fica baixo. Prioridade máxima.
2. **"Stop time" após combos/cadeias:** a pilha para de subir por um tempo proporcional ao combo. É o principal mecanismo de virada de jogo e recompensa jogar bem sob pressão.
3. **Tempo de graça no topo** (backlog também): quando um bloco encosta no teto, dar ~1–2s antes do game over. Morrer "de repente" parece injusto.
4. **Subida manual da pilha** (segurar um botão para subir mais rápido): jogadores bons querem controlar o ritmo.
5. **Fila de lixo visível:** mostrar o que está vindo antes de cair. Ataque sem aviso parece injusto; com aviso vira decisão.
6. **Mesma sequência de blocos para os dois jogadores no PvP** (semente aleatória compartilhada). Assim ninguém perde por sorte.
7. **6 elementos na grade de 7 colunas** deixa o jogo mais difícil de encontrar matches. Sugiro 5 elementos nos modos fáceis/iniciante e 6 no difícil/ranqueado (o original faz parecido).
8. **Duração de partida PvP de 2–3 min.** O "MODO FRENÉTICO" aos 5:00 é ótimo como morte súbita, mas no versus eu traria isso para ~2:00.

### Sobre o sistema de cristais combinado

O que eu manteria: janela de combo de 1,8s, cristal que cresce enquanto você continua combando, quebra pelo elemento certo. A parte do elemento é **o diferencial do seu jogo**, gosto muito.

O que eu mudaria:

- **Cadeias (eco) valem pouco nas regras atuais.** No gênero, cadeia é a jogada mais difícil e devia ser o ataque mais forte. Sugestão: combo (vários blocos de uma vez) manda cristal **largo e baixo**; cadeia (limpezas por gravidade em sequência) manda cristal **alto**, crescendo a cada elo. Assim os dois estilos são válidos, mas cadeia é o "golpe de mestre".
- **Rede de segurança contra situação sem saída:** se o jogador não tem o elemento certo perto, o cristal pode virar uma parede impossível. Proposta: match do elemento certo quebra o cristal inteiro; match de qualquer outro elemento encostado quebra só uma camada. Mantém a estratégia sem gerar derrota injusta.
- **Nada de vantagem elemental paga ou de personagem no ranqueado.** Se personagens tiverem poderes, no ranqueado eles devem ser só visuais (ou tudo liberado de graça). Senão vira pay-to-win e a comunidade some.

## 4. PvP ranqueado num site estático: dá?

Sim, mas o GitHub Pages sozinho não basta. Você precisa de um serviço pronto (sem servidor próprio):

- **Supabase** (recomendo): login, banco de dados para o ranking e canal em tempo real. Plano grátis serve para começar. O Claude consegue configurar com você passo a passo.
- **PeerJS/WebRTC**: conexão direto entre os dois jogadores, bom para "sala com código de amigo", mas sozinho não serve para ranking confiável.

**A boa notícia:** esse gênero é muito mais fácil de pôr online que jogo de luta. Cada um joga o próprio tabuleiro; os jogadores só trocam "mandei um cristal assim" e "perdi". Atraso de rede de 100–200ms quase não se sente.

**A parte difícil é trapaça.** Num ranking, o navegador do jogador pode mentir. A solução que cabe no seu caso: o jogo grava as teclas da partida (replay) e uma função no Supabase roda a mesma simulação para conferir o resultado antes de dar pontos. Dá para reaproveitar o próprio código do jogo. Isso exige o jogo ser **determinístico** (mesma semente + mesmas teclas = mesmo resultado), e vale começar a deixar o código assim desde já.

**O risco real não é técnico, é de público:** ranqueado precisa de gente online ao mesmo tempo. Com poucos jogadores, a fila fica vazia e o jogo parece morto. Por isso eu faria nesta ordem: versus local → sala com código de amigo → ranqueado (com ranking tipo Glicko/Elo), e bots para preencher fila nos horários vazios (avisando que é bot).

**Atalho ótimo se for para a Steam:** "Remote Play Together" deixa um versus local (dois jogadores na mesma tela) ser jogado online, sem você programar rede nenhuma.

## 5. Single player com progressão

- **Campanha de 6 biomas = 6 globos.** Cada globo com uma regra própria (ex.: Água com blocos que deslizam, Fogo com pilha mais rápida, Terra com blocos pesados, Ar com cristais leves, Planta com blocos que crescem, Vitalis com blocos que se espalham) e um **chefe com IA** no final. É a parte do backlog "regras por bioma".
- **Modo Puzzle** (resolver em X movimentos): conteúdo barato de fazer, ótimo para ensinar mecânicas, e jogadores de puzzle amam. 30–60 fases já enche o jogo.
- **Desafio diário** com semente igual para todo mundo e ranking do dia. Custo baixíssimo, ótimo para fazer o jogador voltar.
- **Contra-relógio e Endless** com recorde.

### A ponte para o "globinho"

Em vez de construir base agora, faça do globo de neve a **estante de troféus** do jogador: cada conquista, chefe vencido ou temporada do ranqueado coloca um objeto, um bioma ou um efeito no seu globo. Ele aparece no menu e no perfil do PvP. Isso entrega a sensação de progressão e de "meu mundinho" sem sistema de ataque/defesa, e prepara o terreno para o Clash-of-Clans-like no futuro.

## 6. História e tema

Sugestão leve, que não atrapalha o jogo: o mundo era um só, equilibrado pelos 6 elementos. Algo (o "Estilhaço") partiu tudo em pequenos globos de neve isolados, cada um dominado por um elemento desequilibrado. O herói (escolhido entre os 16) viaja de globo em globo, vence o guardião de cada elemento num duelo de blocos e restaura o equilíbrio. No fim, o seu próprio globo é o que você vai reconstruindo.

Isso justifica: o mapa, as regras por bioma, os chefes, o PvP ("duelos entre guardiões") e o globo pessoal. Não precisa mais que umas poucas falas por globo.

## 7. Monetização (opinião honesta)

- **Puzzle competitivo é nicho.** Dá para vender, mas não espere volume enorme. O caminho mais seguro é **preço único baixo** (US$ 5–10 / R$ 20–35) na Steam, com demo grátis.
- **Steam:** taxa de US$ 100 por jogo. Jogo HTML vira app de PC com Electron ou Tauri (o Claude faz). Participar do **Steam Next Fest** com demo é a melhor vitrine grátis que existe.
- **Antes da Steam:** soltar uma versão grátis no **itch.io** para colher feedback. Portais como CrazyGames e Poki pagam com anúncio, mas exigem integrar o SDK deles e têm curadoria; bom para divulgação.
- **Depois:** cosméticos (skins de blocos, objetos de globo, personagens) e passe de temporada só cosmético. **Nunca vender poder.**
- **Mobile:** possível no futuro, mas o toque precisa de controle próprio (arrastar o bloco direto, sem cursor de 2 casas).

## 8. Roadmap curto para lançar rápido

Etapas 1 a 4 não precisam de servidor nenhum.

1. **Identidade:** escolher nome, tirar "Tetris/Panel" de tudo, confirmar direitos dos personagens.
2. **Núcleo justo:** troca durante quedas, stop time, tempo de graça, subida manual, código determinístico com semente.
3. **Versus offline:** contra IA (3 dificuldades) e 2 jogadores na mesma tela, com o sistema de cristais e fila visível.
4. **Conteúdo solo:** Modo Puzzle, 6 globos com regra e chefe, desafio diário. **Demo no itch.io** e página na Steam para juntar wishlists.
5. **Online casual:** sala com código de amigo (Supabase).
6. **Ranqueado:** login, ranking, conferência por replay, bots na fila vazia.
7. **Globo pessoal e cosméticos.**

Se eu tivesse que escolher uma só coisa para fazer agora: **item 2**. É o que define se o jogo é bom de verdade, e todo o resto depende dele.
