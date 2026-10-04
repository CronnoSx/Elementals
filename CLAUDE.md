# Elementals

- O dono do projeto escreve em português (pt-BR): responda em português.
- O jogo inteiro fica em um único arquivo, `panel-attack.html` (HTML/CSS/JS puro, sem frameworks e sem build). Mantenha assim.
- Mantenha todas as funcionalidades existentes, a menos que o pedido diga o contrário.
- Saves no `localStorage`: `panelAttack.settings`, `panelAttack.bindings`, `panelAttack.hero`. Não renomeie essas chaves; saves antigos precisam continuar carregando.
- Toda geração de peças usa o gerador com semente (mulberry32), nunca `Math.random()` (efeitos visuais podem usar).
- Mascotes e personagens são só visuais: nunca dão vantagem de jogo.
- Não use os nomes "Tetris", "Panel de Pon", "Tetris Attack" ou "Panel Attack" em textos visíveis; o título vem de `GAME_TITLE`.
- Antes de entregar, teste no navegador headless (Playwright) e confira que não há erros no console.
