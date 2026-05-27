import os
import re
import cv2
import glob
import numpy as np

# ============================================================
# CONFIG
# ============================================================

INPUT_DIR = "/data/s2/abhi_workspace/sanath/Hyper-V2X/demo_vide_sequence/folder"
OUTPUT_VIDEO = "/home/uchihadj/PhD_Uchiha/1319/agent160_4cam_grid.mp4"

AGENT_ID = "160"

FPS = 10

# ============================================================
# FILE PATTERN
# Example:
# 1319_agent160_cam0.png
# ============================================================

pattern = re.compile(r"(\d+)_agent160_cam([0-3])\.png")

# sequence_id -> {cam_id: filepath}
frames = {}

for filepath in glob.glob(os.path.join(INPUT_DIR, f"*_agent{AGENT_ID}_cam*.png")):
    filename = os.path.basename(filepath)

    match = pattern.match(filename)
    if not match:
        continue

    seq_id = int(match.group(1))
    cam_id = int(match.group(2))

    if seq_id not in frames:
        frames[seq_id] = {}

    frames[seq_id][cam_id] = filepath

# Sort sequence ids
sequence_ids = sorted(frames.keys())

if len(sequence_ids) == 0:
    raise ValueError("No matching images found!")

# ============================================================
# READ FIRST IMAGE TO GET SIZE
# ============================================================

first_seq = sequence_ids[0]

required_cams = [0, 1, 2, 3]

for cam in required_cams:
    if cam not in frames[first_seq]:
        raise ValueError(f"Missing cam{cam} in sequence {first_seq}")

sample_img = cv2.imread(frames[first_seq][0])

if sample_img is None:
    raise ValueError("Failed to read sample image")

h, w, _ = sample_img.shape

# Grid output size:
# cam0 | cam1
# cam2 | cam3
out_h = h * 2
out_w = w * 2

# ============================================================
# VIDEO WRITER
# ============================================================

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

video_writer = cv2.VideoWriter(
    OUTPUT_VIDEO,
    fourcc,
    FPS,
    (out_w, out_h)
)

# ============================================================
# CREATE VIDEO
# ============================================================

for seq_id in sequence_ids:

    cam_images = []

    missing = False

    for cam_id in required_cams:
        if cam_id not in frames[seq_id]:
            print(f"Skipping sequence {seq_id}, missing cam{cam_id}")
            missing = True
            break

        img = cv2.imread(frames[seq_id][cam_id])

        if img is None:
            print(f"Failed reading {frames[seq_id][cam_id]}")
            missing = True
            break

        cam_images.append(img)

    if missing:
        continue

    # ========================================================
    # GRID
    # ========================================================

    top_row = np.hstack((cam_images[0], cam_images[1]))
    bottom_row = np.hstack((cam_images[2], cam_images[3]))

    grid = np.vstack((top_row, bottom_row))

    # Optional: add sequence text
    cv2.putText(
        grid,
        f"Sequence: {seq_id}",
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )

    video_writer.write(grid)

    print(f"Processed sequence {seq_id}")

# ============================================================
# CLEANUP
# ============================================================

video_writer.release()

print(f"\nVideo saved to: {OUTPUT_VIDEO}")