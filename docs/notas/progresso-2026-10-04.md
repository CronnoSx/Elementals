# Progresso do jogo em 04/10/2026

Lido da branch `claude/bold-clarke-o2zvt6`, último commit `2d21a35` ("crystals, Versus vs AI with mirrored boards, Vitalis biome"). `panel-attack.html` tem ~3.900 linhas. Rodei uma partida Versus (IA Difícil) por 40 s no navegador headless: sem erros de JavaScript.

## Feito (prompt antigo de Cristais + Vitalis + Espelhamento + IA)

- Cristais: clear 4+ ou "eco" (3 só por gravidade) monta cristal pendente, janela de 1,8 s, cresce +1 linha por clear extra (máx. 4), cancelamento do que está chegando, aviso de 1 s, cai como bloco, sobe com a pilha, não troca, quebra inteiro com match do mesmo elemento.
- Versus vs IA com dois tabuleiros espelhados e a mesma semente (mulberry32), HUD por lado, tela de vitória/derrota, pausa nos dois.
- IA com 3 níveis (Fácil/Normal/Difícil), anda casa por casa, não vê a próxima linha.
- Campanha: cada bioma agora é uma partida Versus contra um personagem aleatório. "Fungos" virou Vitalis (id interno continua `fungi`, sem perder progresso).
- Sons novos de cristal e vitória. Tudo que já existia continua.

## Falta (prompt v2 "Núcleo justo + Cristais v2", ainda não aplicado)

1. Nomes de terceiros: a aba ainda diz "Panel Attack – Protótipo", a tela inicial "PANEL ATTACK" e os créditos "inspirado em Tetris Attack / Panel de Pon". Não existe `GAME_TITLE`.
2. Troca durante quedas e limpezas: `trySwap` só aceita com o tabuleiro inteiro parado (fase global). É a prioridade máxima.
3. Stop time após combo/cadeia: não existe (a pilha só para enquanto algo está caindo/limpando).
4. Tempo de graça no topo: não existe. `pushRow` dá game over na hora se a linha do topo tiver algo.
5. Turbo bloqueado na graça: depende do item 4.
6. 5 elementos nos modos fáceis: não existe, sempre 6.
7. Cristais v2: tamanhos ainda são os antigos (combo 1x4/1x5/1x6, cadeia só manda eco 1x3). Faltam cristal alto por cadeia, quebra de uma linha com elemento errado, efeito dominó e fila visível com tamanho de cada cristal.
8. Semente: tabuleiro e linhas já usam semente. Partículas visuais e a IA ainda usam o gerador do jogo ou `Math.random()` (veja bugs).

## Bugs e pontos estranhos que encontrei

- Biomas não batem com os elementos: o mapa tem Terra, Floresta, **Metal**, Fogo, Vitalis, Ar. Não há bioma de **Água**, e "Metal" não é um elemento do jogo.
- Cadeias valem quase nada: uma cadeia x5 de trincas manda só um cristal 1x3 (o eco só conta se não houver cristal pendente). O v2 corrige.
- Cancelamento arredonda para cima: um cristal de 3 casas contra um de 6 de largura cancela a linha inteira de 6 (`sendCrystal`).
- Cristal alto chegando com pilha média pode matar: ele só entra se as `h` primeiras linhas do topo estiverem livres; se não couber por 2 s, é game over, mesmo sem a pilha encostar no topo.
- Os estilhaços (efeito visual) gastam o gerador com semente do tabuleiro (`spawnShards` usa `state.rng`). Para replays/ranqueado, o visual deveria usar `Math.random()`.
- IA Difícil foi tímida no teste: 520 pontos e 2 cristais em 40 s, e ficou 10 s sem pontuar no fim. Pode ser só falta de jogadas, mas vale olhar quando o v2 entrar.
