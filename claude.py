# import cv2
# import os
# import numpy as np
# import imageio

# folder_path = "/home/uchihadj/PhD_Uchiha/demo_shata/"
# output_gif  = "/home/uchihadj/PhD_Uchiha/output_WITHTITILE.gif"
# title_text  = "Uncertainty estimation: When communication volume decreases (524 KB to 8 KB)"

# # ── 1. Sort images numerically ──────────────────────────────────────────────
# images = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
# print(f"Found images: {images}")

# # ── 2. Get target H, W from first image ─────────────────────────────────────
# first = cv2.imread(os.path.join(folder_path, images[0]))
# TARGET_H, TARGET_W = first.shape[:2]
# print(f"Target size: {TARGET_W}x{TARGET_H}")

# TITLE_BAR_H = 180  # pixels reserved for title at top

# def add_title(canvas, text):
#     """Draw title bar on top of canvas."""
#     h, w = canvas.shape[:2]
#     titled = np.zeros((h + TITLE_BAR_H, w, 3), dtype=np.uint8)
#     titled[TITLE_BAR_H:] = canvas

#     # Dark background for title
#     titled[:TITLE_BAR_H] = (30, 30, 30)

#     # Auto-shrink font to fit width
#     font       = cv2.FONT_HERSHEY_SIMPLEX
#     font_scale = 0.7
#     thickness  = 2
#     (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)
#     while tw > w - 20 and font_scale > 0.3:
#         font_scale -= 0.05
#         (tw, th), _ = cv2.getTextSize(text, font, font_scale, thickness)

#     x = (w - tw) // 2
#     y = (TITLE_BAR_H + th) // 2
#     cv2.putText(titled, text, (x, y), font, font_scale, (255, 255, 255), thickness)
#     return titled


# def make_pair_column(img_a, img_b, label_a, label_b):
#     """Stack two images vertically with small labels."""
#     def label(img, text):
#         out = img.copy()
#         cv2.putText(out, text, (6, 22), cv2.FONT_HERSHEY_SIMPLEX,
#                     0.6, (0, 255, 0), 2)
#         return out
#     return np.vstack([label(img_a, label_a), label(img_b, label_b)])


# # ── 3. Build pairs ───────────────────────────────────────────────────────────
# pairs = []
# for i in range(0, len(images) - 1, 2):
#     name_a = images[i]
#     name_b = images[i + 1]

#     img_a = cv2.imread(os.path.join(folder_path, name_a))
#     img_b = cv2.imread(os.path.join(folder_path, name_b))

#     img_a = cv2.resize(img_a, (TARGET_W, TARGET_H))
#     img_b = cv2.resize(img_b, (TARGET_W, TARGET_H))

#     col = make_pair_column(img_a, img_b, name_a, name_b)
#     pairs.append(col)
#     print(f"Paired: {name_a}  <-->  {name_b}")

# # ── 4. Build accumulating frames ─────────────────────────────────────────────
# # Frame 1 → pair0
# # Frame 2 → pair0 | pair1
# # Frame 3 → pair0 | pair1 | pair2  ...
# frames = []
# for k in range(1, len(pairs) + 1):
#     canvas = np.hstack(pairs[:k])          # accumulate horizontally
#     canvas = add_title(canvas, title_text)
#     canvas_rgb = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
#     frames.append(canvas_rgb)

# # ── 5. Save GIF ───────────────────────────────────────────────────────────────
# # GIF frames must all be the same size → pad earlier frames to max width
# max_w = frames[-1].shape[1]
# max_h = frames[-1].shape[0]

# padded_frames = []
# for f in frames:
#     h, w = f.shape[:2]
#     if w < max_w:
#         pad = np.zeros((max_h, max_w - w, 3), dtype=np.uint8)
#         f = np.hstack([f, pad])
#     padded_frames.append(f)

# imageio.mimsave(output_gif, padded_frames, fps=0.8)   # ~1.25s per frame
# print(f"\nGIF saved: {output_gif}  ({len(padded_frames)} frames)")

# import cv2
# import os
# import numpy as np
# import imageio

# folder_path = "/home/uchihadj/PhD_Uchiha/demo_shata/"
# output_gif  = "/home/uchihadj/PhD_Uchiha/output_final_loop.gif"

# images = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
# print(f"Found images: {images}")

# first = cv2.imread(os.path.join(folder_path, images[0]))
# TARGET_H, TARGET_W = first.shape[:2]
# print(f"Target size: {TARGET_W}x{TARGET_H}")

# def make_pair_column(img_a, img_b, label_a, label_b):
#     def label(img, text):
#         out = img.copy()
#         cv2.putText(out, text, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
#         return out
#     return np.vstack([label(img_a, label_a), label(img_b, label_b)])

# pairs = []
# for i in range(0, len(images) - 1, 2):
#     name_a = images[i]
#     name_b = images[i + 1]

#     img_a = cv2.resize(cv2.imread(os.path.join(folder_path, name_a)), (TARGET_W, TARGET_H))
#     img_b = cv2.resize(cv2.imread(os.path.join(folder_path, name_b)), (TARGET_W, TARGET_H))

#     pairs.append(make_pair_column(img_a, img_b, name_a, name_b))
#     print(f"Paired: {name_a}  <-->  {name_b}")

# frames = []
# for k in range(1, len(pairs) + 1):
#     canvas = np.hstack(pairs[:k])
#     frames.append(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))

# max_w = frames[-1].shape[1]
# max_h = frames[-1].shape[0]

# padded_frames = []
# for f in frames:
#     h, w = f.shape[:2]
#     if w < max_w:
#         pad = np.zeros((max_h, max_w - w, 3), dtype=np.uint8)
#         f = np.hstack([f, pad])
#     padded_frames.append(f)

# imageio.mimsave(output_gif, padded_frames, fps=1.0, loop=0)
# print(f"GIF saved: {output_gif}  ({len(padded_frames)} frames)")

import cv2
import os
import numpy as np
import imageio

folder_path = "/home/uchihadj/PhD_Uchiha/demo_shata/"
output_gif  = "/home/uchihadj/PhD_Uchiha/output_final_loop_with_bar.gif"

PAIR_LABELS = [
    "CV - 524 KB",
    "264 KB",
    "132 KB",
    "66 KB",
    "16 KB",
    "8 KB",
]

images = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
print(f"Found images: {images}")

first = cv2.imread(os.path.join(folder_path, images[0]))
TARGET_H, TARGET_W = first.shape[:2]
print(f"Target size: {TARGET_W}x{TARGET_H}")

LABEL_BAR_H = 250
FONT        = cv2.FONT_HERSHEY_SIMPLEX
THICKNESS   = 20

# ── Compute ONE font scale using the longest label ───────────────────────────
longest_label = max(PAIR_LABELS, key=len)
FONT_SCALE = 3.0
(tw, _), _ = cv2.getTextSize(longest_label, FONT, FONT_SCALE, THICKNESS)
while tw > TARGET_W - 20 and FONT_SCALE > 0.3:
    FONT_SCALE -= 0.05
    (tw, _), _ = cv2.getTextSize(longest_label, FONT, FONT_SCALE, THICKNESS)
print(f"Uniform font scale: {FONT_SCALE:.2f}")


def make_label_bar(width, text):
    """White bar with centered black text — same font scale for every bar."""
    bar = np.ones((LABEL_BAR_H, width, 3), dtype=np.uint8) * 255
    (tw, th), _ = cv2.getTextSize(text, FONT, FONT_SCALE, THICKNESS)
    x = (width - tw) // 2
    y = (LABEL_BAR_H + th) // 2
    cv2.putText(bar, text, (x, y), FONT, FONT_SCALE, (0, 0, 0), THICKNESS)
    return bar


def make_pair_column(img_a, img_b, pair_label):
    bar = make_label_bar(img_a.shape[1], pair_label)
    return np.vstack([bar, img_a, img_b])


pairs = []
for i, pair_idx in enumerate(range(0, len(images) - 1, 2)):
    name_a = images[pair_idx]
    name_b = images[pair_idx + 1]

    img_a = cv2.resize(cv2.imread(os.path.join(folder_path, name_a)), (TARGET_W, TARGET_H))
    img_b = cv2.resize(cv2.imread(os.path.join(folder_path, name_b)), (TARGET_W, TARGET_H))

    label = PAIR_LABELS[i] if i < len(PAIR_LABELS) else f"Pair {i}"
    pairs.append(make_pair_column(img_a, img_b, label))
    print(f"Paired: {name_a} <--> {name_b}  |  label: '{label}'")

frames = []
for k in range(1, len(pairs) + 1):
    canvas = np.hstack(pairs[:k])
    frames.append(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))

max_w = frames[-1].shape[1]
max_h = frames[-1].shape[0]

padded_frames = []
for f in frames:
    h, w = f.shape[:2]
    if w < max_w:
        pad = np.ones((max_h, max_w - w, 3), dtype=np.uint8) * 255
        f = np.hstack([f, pad])
    padded_frames.append(f)

imageio.mimsave(output_gif, padded_frames, fps=1.0, loop=0)
print(f"\nGIF saved: {output_gif}  ({len(padded_frames)} frames)")