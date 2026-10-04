"""
Recorta os 16 personagens de reference_sheet.webp em sprites PNG com transparência
(char_01.png … char_16.png), sem os círculos numerados e sem a aquarela do fundo.

    pip install numpy scipy opencv-python-headless
    python3 characters/extract_sprites.py

Para trocar a arte depois, basta substituir os char_XX.png (mesmos nomes).
"""
import cv2, numpy as np, os
from scipy import ndimage as ndi

img = cv2.imread(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reference_sheet.webp'))
H, W = img.shape[:2]
L = img.astype(np.float32).mean(axis=2)
yy, xx = np.mgrid[0:H, 0:W]

# ---------- Círculos numerados (grade + ajustes) ----------
COLS = {0: [48, 160, 278, 401, 522, 650, 790, 908], 1: [48, 160, 276, 400, 522, 654, 798, 910]}
badges = []
for row, xs in COLS.items():
    for i, x in enumerate(xs):
        n = row * 8 + i + 1
        wy, by = (88, 192) if row == 0 else (280, 376)
        wx = x
        if n == 2: wy = 65
        if n == 13: wx = 528
        badges += [(wx, wy), (x, by)]
badge = np.zeros((H, W), bool)
for cx, cy in badges:
    badge |= (xx - cx) ** 2 + (yy - cy) ** 2 <= 12.5 ** 2

# ---------- Silhueta: traço escuro fechado + preenchimento, por célula ----------
ROW_SPLIT = 224
X_EDGES = {0: [22, 137, 250, 375, 500, 625, 755, 884, 1002],   # entre as colunas (por fileira)
           1: [22, 150, 253, 395, 496, 638, 770, 890, 1002]}
BG = float(np.median(L[40:410, 30:990]))  # cor do pergaminho
print('fundo', BG)
Y_RANGES = {0: (30, ROW_SPLIT), 1: (ROW_SPLIT, 413)}
OUT = os.path.dirname(os.path.abspath(__file__))
sheet = []
for row in (0, 1):
    for i in range(8):
        n = row * 8 + i + 1
        y0, y1 = Y_RANGES[row]
        x0, x1 = X_EDGES[row][i], X_EDGES[row][i + 1]
        roi = L[y0:y1, x0:x1]
        bg = BG
        fg = roi < bg - 55
        fg = ndi.binary_closing(fg, iterations=2)
        fg = ndi.binary_fill_holes(fg)
        fg &= ~badge[y0:y1, x0:x1]
        # aquarela do fundo (verde ou azul clarinhos) não é personagem
        c = img[y0:y1, x0:x1].astype(np.int16)
        Bc, Gc, Rc = c[..., 0], c[..., 1], c[..., 2]
        green_min = 110 if n in (8, 9, 16) else 160   # esses têm aquarela verde mais forte atrás
        wash = ((roi > green_min) & (Gc > Rc + 4) & (Gc >= Bc)) | ((roi > 160) & (Bc > Rc + 12))
        fg &= ~wash
        fg = ndi.binary_opening(fg, iterations=1)
        lab, k = ndi.label(fg)
        sizes = ndi.sum(fg, lab, range(1, k + 1))
        m = lab == (np.argmax(sizes) + 1)
        m = ndi.binary_fill_holes(m)
        ys, xs = np.where(m)
        bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
        pad = 2
        crop = img[y0 + by0 - pad:y0 + by1 + pad, x0 + bx0 - pad:x0 + bx1 + pad]
        a = np.zeros(crop.shape[:2], np.float32)
        a[pad:-pad, pad:-pad] = m[by0:by1, bx0:bx1]
        a = ndi.binary_dilation(a > 0, iterations=1).astype(np.float32)
        a = cv2.GaussianBlur(a, (3, 3), 0.6)
        rgba = np.dstack([crop, (a * 255).astype(np.uint8)])
        cv2.imwrite(os.path.join(OUT, f'char_{n:02d}.png'), rgba)
        print(n, 'tamanho', rgba.shape[1], 'x', rgba.shape[0])
        # folha de conferência: sprite sobre fundo escuro
        h = 200
        sc = h / rgba.shape[0]
        sp = cv2.resize(rgba, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA).astype(np.float32)
        tile = np.full((h, 120, 3), 40, np.float32)
        ox = (120 - sp.shape[1]) // 2
        al = sp[..., 3:] / 255
        tile[:, max(ox, 0):max(ox, 0) + sp.shape[1]] = tile[:, max(ox, 0):max(ox, 0) + sp.shape[1]] * (1 - al) + sp[..., :3] * al
        tile = tile.astype(np.uint8)
        cv2.putText(tile, str(n), (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        sheet.append(tile)
cv2.imwrite(os.path.join(OUT, 'contact_sheet_preview.png'), np.vstack([np.hstack(sheet[:8]), np.hstack(sheet[8:])]))
