import os
import glob
import cv2
import numpy as np

# ============================================================
# PATHS
# ============================================================

DYNAMIC_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/sorted_1460_labels/pred"
MAP_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/static_1460"

OUTPUT_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/sorted_1460_labels/merged_pred"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# GET ALL DYNAMIC FILES
# ============================================================

dynamic_files = sorted(
    glob.glob(os.path.join(DYNAMIC_DIR, "*_pred.png"))
)

print(f"Found {len(dynamic_files)} dynamic files")

# ============================================================
# PROCESS EACH FRAME
# ============================================================

for dynamic_path in dynamic_files:

    # --------------------------------------------------------
    # Extract frame id
    # Example:
    # 1319_gt.png -> 1319
    # --------------------------------------------------------

    filename = os.path.basename(dynamic_path)
    frame_id = filename.split("_")[0]

    map_path = os.path.join(MAP_DIR, f"{frame_id}.png")

    # --------------------------------------------------------
    # Check map exists
    # --------------------------------------------------------

    if not os.path.exists(map_path):
        print(f"Missing map for frame {frame_id}")
        continue

    # --------------------------------------------------------
    # Read images
    # --------------------------------------------------------

    dynamic_fig = cv2.imread(dynamic_path, 0)   # grayscale
    static_fig = cv2.imread(map_path)           # BGR

    if dynamic_fig is None:
        print(f"Failed reading dynamic image: {dynamic_path}")
        continue

    if static_fig is None:
        print(f"Failed reading map image: {map_path}")
        continue

    # --------------------------------------------------------
    # Binarize dynamic image
    # Any non-zero pixel -> 1
    # --------------------------------------------------------

    dynamic_mask = np.zeros_like(dynamic_fig)
    dynamic_mask[dynamic_fig > 0] = 1

    # --------------------------------------------------------
    # Overlay white onto static map
    # --------------------------------------------------------

    merged = static_fig.copy()

    merged[dynamic_mask == 1] = [255, 255, 255]

    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{frame_id}_merged.png"
    )

    cv2.imwrite(output_path, merged)

    print(f"Saved: {output_path}")

print("\nDone!")