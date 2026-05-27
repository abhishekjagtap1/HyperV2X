import cv2
import os
import numpy as np
import imageio

# Hardcoded folder path
folder_path = "/home/uchihadj/PhD_Uchiha/hyper_iv_demo"
output_gif  = "/home/uchihadj/PhD_Uchiha/hyper_iv_demo/output.gif"
output_mp4  = "/home/uchihadj/PhD_Uchiha/hyper_iv_demo/output.mp4"

# Load images sorted by filename index (0.png, 1.png, ... 12.png)
images = sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
print(f"Found images: {images}")

frames = []
target_size = None  # (width, height) — set from first frame

for i in range(0, len(images) - 1, 2):
    pred_name = images[i]
    heat_name = images[i + 1]

    pred_img = cv2.imread(os.path.join(folder_path, pred_name))
    heat_img = cv2.imread(os.path.join(folder_path, heat_name))

    if pred_img is None or heat_img is None:
        print(f"Skipping pair ({pred_name}, {heat_name}) — could not read image")
        continue

    # Resize heatmap to match pred
    if pred_img.shape != heat_img.shape:
        heat_img = cv2.resize(heat_img, (pred_img.shape[1], pred_img.shape[0]))

    combined = np.hstack([pred_img, heat_img])

    # Set target size from first valid frame
    if target_size is None:
        target_size = (combined.shape[1], combined.shape[0])  # (W, H)

    # Resize combined frame to match target if needed
    if (combined.shape[1], combined.shape[0]) != target_size:
        combined = cv2.resize(combined, target_size)

    # Labels
    cv2.putText(combined, f"Pred ({pred_name})", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(combined, f"Heatmap ({heat_name})", (target_size[0] // 2 + 10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    combined_rgb = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
    frames.append(combined_rgb)
    print(f"Paired: {pred_name}  <-->  {heat_name}  | frame size: {combined.shape}")

print(f"\nTotal frames: {len(frames)}")

# ---------- Save as GIF ----------
imageio.mimsave(output_gif, frames, fps=1)
print(f"GIF saved: {output_gif}")

# ---------- Save as MP4 ----------
h, w = frames[0].shape[:2]
writer = cv2.VideoWriter(output_mp4, cv2.VideoWriter_fourcc(*'mp4v'), 1, (w, h))
for frame in frames:
    writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
writer.release()
print(f"MP4 saved: {output_mp4}")