import os
import re
import cv2
import glob
import numpy as np
import imageio  # ✅ ADDED FOR GIF

# ============================================================
# CONFIG
# ============================================================

CAM_DIR = "/home/uchihadj/PhD_Uchiha/scene_741/scene_741"

GT_DIR   = "/home/uchihadj/PhD_Uchiha/scene_741/sorted_741_labels/merged_gt"
PRED_DIR = "/home/uchihadj/PhD_Uchiha/scene_741/sorted_741_labels/merged_pred"
UNC_DIR  = "/home/uchihadj/PhD_Uchiha/scene_741/sorted_741_labels/merged_pred_unc_total"

OUTPUT_VIDEO = "/home/uchihadj/PhD_Uchiha/scene_741/final_multi_agent_scne741.mp4"
OUTPUT_GIF   = "/home/uchihadj/PhD_Uchiha/scene_741/final_multi_agent_scene_741.gif"  # ✅ ADDED

AGENT1 = "886"
AGENT2 = "895"

FPS = 10

# ============================================================
# LOAD CAMERA FRAMES (two agents)
# ============================================================

pattern1 = re.compile(r"(\d+)_agent886_cam([0-3])\.png")
pattern2 = re.compile(r"(\d+)_agent895_cam([0-3])\.png")

cam_a = {}
cam_b = {}

for fp in glob.glob(os.path.join(CAM_DIR, "*.png")):
    name = os.path.basename(fp)

    m1 = pattern1.match(name)
    m2 = pattern2.match(name)

    if m1:
        seq = int(m1.group(1))
        cam = int(m1.group(2))
        cam_a.setdefault(seq, {})[cam] = fp

    if m2:
        seq = int(m2.group(1))
        cam = int(m2.group(2))
        cam_b.setdefault(seq, {})[cam] = fp

frame_ids = sorted(set(cam_a.keys()) & set(cam_b.keys()))

required_cams = [0, 1, 2, 3]

print(f"Total frames: {len(frame_ids)}")

# ============================================================
# SIZE
# ============================================================

first = frame_ids[0]

sample = cv2.imread(cam_a[first][0])
h, w = sample.shape[:2]

unc_path = os.path.join(UNC_DIR, f"{int(first):04d}_merged.png")
unc_sample = cv2.imread(unc_path)
h_u, w_u = unc_sample.shape[:2]

w_u = w

# ============================================================
# VIDEO WRITER
# ============================================================

out_w = w * 3
out_h = h * 3

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (out_w, out_h))

# ============================================================
# GIF BUFFER  ✅ ADDED
# ============================================================

gif_frames = []

# ============================================================
# HELPER: label image
# ============================================================

def label(img, text):
    cv2.putText(img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)
    return img

# ============================================================
# PROCESS
# ============================================================

for fid in frame_ids:

    # -------------------------
    # CAMS AGENT 160
    # -------------------------
    if fid not in cam_a or fid not in cam_b:
        continue

    cams_a = []
    cams_b = []

    for c in required_cams:
        if c not in cam_a[fid] or c not in cam_b[fid]:
            break

        img_a = cv2.imread(cam_a[fid][c])
        img_b = cv2.imread(cam_b[fid][c])

        cams_a.append(cv2.resize(img_a, (w, h)))
        cams_b.append(cv2.resize(img_b, (w, h)))

    if len(cams_a) != 4:
        continue

    # -------------------------
    # GT / PRED / UNC
    # -------------------------

    # gt   = cv2.imread(os.path.join(GT_DIR, f"{fid}_merged.png"))
    # pred = cv2.imread(os.path.join(PRED_DIR, f"{fid}_merged.png"))
    # unc  = cv2.imread(os.path.join(UNC_DIR, f"{fid}_merged.png"))
    gt   = cv2.imread(os.path.join(GT_DIR,   f"{int(fid):04d}_merged.png"))
    pred = cv2.imread(os.path.join(PRED_DIR, f"{int(fid):04d}_merged.png"))
    unc  = cv2.imread(os.path.join(UNC_DIR,  f"{int(fid):04d}_merged.png"))

    if gt is None or pred is None or unc is None:
        continue

    gt   = cv2.resize(gt, (w, h))
    pred = cv2.resize(pred, (w, h))
    unc  = cv2.resize(unc, (w, h))

    # ========================================================
    # LABEL CAMERAS
    # ========================================================

    for i in range(4):
        cams_a[i] = label(cams_a[i], f"Agent886 Cam{i}")
        cams_b[i] = label(cams_b[i], f"Agent895 Cam{i}")

    gt   = label(gt, "GT")
    pred = label(pred, "PRED")
    unc  = label(unc, "UNCERTAINTY")

    # ========================================================
    # BUILD GRID
    # ========================================================

    row1 = np.hstack([cams_a[0], cams_a[1], gt])
    row2 = np.hstack([cams_a[2], cams_a[3], unc])
    row3 = np.hstack([cams_b[0], cams_b[1], pred])

    frame = np.vstack([row1, row2, row3])

    # ========================================================
    # WRITE MP4
    # ========================================================

    writer.write(frame)

    # ========================================================
    # STORE FOR GIF (RGB REQUIRED)
    # ========================================================

    gif_frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    print(f"Processed {fid}")

# ============================================================
# FINALIZE MP4
# ============================================================

writer.release()
print(f"\nSaved MP4 → {OUTPUT_VIDEO}")

# ============================================================
# SAVE GIF  ✅ ADDED
# ============================================================

print("Saving GIF... this may take time")

imageio.mimsave(
    OUTPUT_GIF,
    gif_frames,
    fps=FPS,
    loop=0
)

print(f"Saved GIF → {OUTPUT_GIF}")