import os
import glob
from PIL import Image

# ============================================================
# PATHS
# ============================================================

HEATMAP_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/sorted_1460_labels/unc_total"
MAP_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/static_1460"

OUTPUT_DIR = "/home/uchihadj/PhD_Uchiha/scene_1460/sorted_1460_labels/merged_pred_unc_total"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# GET ALL HEATMAP FILES
# ============================================================

heatmap_files = sorted(glob.glob(os.path.join(HEATMAP_DIR, "*_unc_total.png")))

print(f"Found {len(heatmap_files)} heatmap files")

# ============================================================
# PROCESS EACH FRAME
# ============================================================

for heatmap_path in heatmap_files:

    filename = os.path.basename(heatmap_path)
    frame_id = filename.split("_")[0]

    map_path = os.path.join(MAP_DIR, f"{frame_id}.png")

    if not os.path.exists(map_path):
        print(f"Missing map for frame {frame_id}")
        continue

    # --------------------------------------------------------
    # Load images as RGBA (IMPORTANT for blending)
    # --------------------------------------------------------

    map_img = Image.open(map_path).convert("RGBA")
    heatmap_img = Image.open(heatmap_path).convert("RGBA")

    # --------------------------------------------------------
    # Ensure same size (safety check)
    # --------------------------------------------------------

    if map_img.size != heatmap_img.size:
        heatmap_img = heatmap_img.resize(map_img.size)

    # --------------------------------------------------------
    # Blend (your desired logic)
    # --------------------------------------------------------

    merged = Image.blend(map_img, heatmap_img, alpha=0.8)

    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{frame_id}_merged.png"
    )

    merged.save(output_path)

    print(f"Saved: {output_path}")

print("\nDone!")