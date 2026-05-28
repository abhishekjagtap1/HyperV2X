import os
import glob
import shutil

# ============================================================
# CONFIG
# ============================================================

INPUT_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/scene_1460"
out = "/home/uchihadj/PhD_Uchiha/scene_1460/sorted_1460_labels"
OUTPUT_GT_DIR = os.path.join(out, "gt")
OUTPUT_PRED_DIR = os.path.join(out, "pred")
OUTPUT_UNC_DIR = os.path.join(out, "unc_total")

# Create output folders
os.makedirs(OUTPUT_GT_DIR, exist_ok=True)
os.makedirs(OUTPUT_PRED_DIR, exist_ok=True)
os.makedirs(OUTPUT_UNC_DIR, exist_ok=True)

# ============================================================
# COPY GT FILES
# ============================================================

gt_files = glob.glob(os.path.join(INPUT_DIR, "*_gt.png"))

for file in gt_files:
    shutil.copy(file, OUTPUT_GT_DIR)

print(f"Copied {len(gt_files)} GT files")

# ============================================================
# COPY PRED FILES
# ============================================================

pred_files = glob.glob(os.path.join(INPUT_DIR, "*_pred.png"))

for file in pred_files:
    shutil.copy(file, OUTPUT_PRED_DIR)

print(f"Copied {len(pred_files)} PRED files")

# ============================================================
# COPY UNCERTAINTY FILES
# ============================================================

unc_files = glob.glob(os.path.join(INPUT_DIR, "*_unc_total.png"))

for file in unc_files:
    shutil.copy(file, OUTPUT_UNC_DIR)

print(f"Copied {len(unc_files)} UNC_TOTAL files")

print("\nDone!")