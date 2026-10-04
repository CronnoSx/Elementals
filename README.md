# Elementals (nome provisório)

Jogo de puzzle de navegador: troca de blocos de 6 elementos (Água, Fogo, Terra, Ar, Planta e Metal), cadeias, cristais de ataque, versus contra IA e campanha com 6 biomas e mascotes. HTML/CSS/JS puro, sem frameworks.

## Jogar

Abra `index.html` (ou `panel-attack.html`) no navegador.

## Pastas

- `panel-attack.html`: o jogo inteiro.
- `index.html`: abre o jogo (usado pelo GitHub Pages).
- `characters/`: 16 personagens, a folha original e o script de recorte.
- `sounds/`: efeitos e música, e `generate_sounds.py` (numpy + scipy) que gera os sons.
- `tiles/`: imagens dos blocos usadas no jogo.
- `mascots/<nome>/`: imagens dos 6 mascotes usadas no jogo (`full`, `happy`, `angry`, `scared`, `celebrate`).
- `art/`: artes originais (blocos e folhas de modelo dos mascotes), com os recortes.
- `docs/prompts/` e `docs/notas/`: prompts e anotações de design.

Separado do repositório `another-x-indie-experience` (commit `4232e1c` da branch `claude/bold-clarke-o2zvt6`).
