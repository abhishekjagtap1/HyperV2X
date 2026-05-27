import os
import re
import cv2
import glob
import numpy as np

# ============================================================
# CONFIG
# ============================================================

CAM_DIR = "/home/uchihadj/PhD_Uchiha/1319/all/folder"

GT_DIR   = "/home/uchihadj/PhD_Uchiha/1319/sorted_1319_labels/merged_gt"
PRED_DIR = "/home/uchihadj/PhD_Uchiha/1319/sorted_1319_labels/merged_pred"
UNC_DIR  = "/home/uchihadj/PhD_Uchiha/1319/sorted_1319_labels/merged_pred_unc_total"

OUTPUT_VIDEO = "/home/uchihadj/PhD_Uchiha/1319/final_video_fixed.mp4"

AGENT_ID = "160"
FPS = 10

UNC_SCALE = 1.5  # width scaling only

# ============================================================
# LOAD CAMERA FRAMES
# ============================================================

pattern = re.compile(r"(\d+)_agent160_cam([0-3])\.png")

cam_frames = {}

for fp in glob.glob(os.path.join(CAM_DIR, f"*agent{AGENT_ID}_cam*.png")):
    name = os.path.basename(fp)
    m = pattern.match(name)
    if not m:
        continue

    seq = int(m.group(1))
    cam = int(m.group(2))

    cam_frames.setdefault(seq, {})[cam] = fp

required_cams = [0, 1, 2, 3]
frame_ids = sorted(cam_frames.keys())

print(f"Total frames: {len(frame_ids)}")

# ============================================================
# GET REFERENCE SIZE FROM FIRST VALID FRAME
# ============================================================

first_valid = None

for fid in frame_ids:
    if all(c in cam_frames[fid] for c in required_cams):
        first_valid = fid
        break

if first_valid is None:
    raise ValueError("No valid camera frames found")

sample_cam = cv2.imread(cam_frames[first_valid][0])
h, w = sample_cam.shape[:2]

# ============================================================
# UNC SIZE (FORCE CONSISTENT HEIGHT)
# ============================================================

unc_sample_path = os.path.join(UNC_DIR, f"{first_valid}_merged.png")
unc_sample = cv2.imread(unc_sample_path)

if unc_sample is None:
    raise ValueError("Cannot read UNC sample image")

unc_h, unc_w = unc_sample.shape[:2]

unc_w = int(w * UNC_SCALE)   # scale based on cam width
unc_h = h                   # FORCE SAME HEIGHT (IMPORTANT FIX)

# ============================================================
# VIDEO WRITER
# ============================================================

out_w = w * 3 + unc_w
out_h = h * 2

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (out_w, out_h))

# ============================================================
# PROCESS FRAMES
# ============================================================

for fid in frame_ids:

    # -------------------------
    # CHECK CAMERAS
    # -------------------------
    if fid not in cam_frames:
        continue

    if not all(c in cam_frames[fid] for c in required_cams):
        print(f"Skipping cams {fid}")
        continue

    cams = []
    skip = False

    for c in required_cams:
        img = cv2.imread(cam_frames[fid][c])
        if img is None:
            skip = True
            break

        cams.append(cv2.resize(img, (w, h)))

    if skip:
        continue

    # -------------------------
    # LOAD GT / PRED / UNC
    # -------------------------

    gt_path   = os.path.join(GT_DIR, f"{fid}_merged.png")
    pred_path = os.path.join(PRED_DIR, f"{fid}_merged.png")
    unc_path  = os.path.join(UNC_DIR, f"{fid}_merged.png")

    gt   = cv2.imread(gt_path)
    pred = cv2.imread(pred_path)
    unc  = cv2.imread(unc_path)

    if gt is None or pred is None or unc is None:
        print(f"Missing labels {fid}")
        continue

    # -------------------------
    # FORCE SAME HEIGHT (CRITICAL FIX)
    # -------------------------

    gt   = cv2.resize(gt, (w, h))
    pred = cv2.resize(pred, (w, h))
    unc  = cv2.resize(unc, (unc_w, h))   # IMPORTANT: SAME HEIGHT

    # -------------------------
    # BUILD GRID
    # -------------------------

    top = np.hstack([cams[0], cams[1], gt])

    bottom = np.hstack([cams[2], cams[3], pred, unc])

    # pad top row to match bottom width
    top = cv2.copyMakeBorder(
        top,
        0,
        bottom.shape[0] - top.shape[0],
        0,
        bottom.shape[1] - top.shape[1],
        cv2.BORDER_CONSTANT,
        value=(0, 0, 0)
    )

    frame = np.vstack([top, bottom])

    # -------------------------
    # LABEL
    # -------------------------

    cv2.putText(
        frame,
        f"Frame {fid}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    writer.write(frame)

    print(f"Processed {fid}")

# ============================================================
# CLEANUP
# ============================================================

writer.release()
print(f"\nSaved video → {OUTPUT_VIDEO}")