# from PIL import Image

# objects_img = Image.open("/home/uchihadj/PhD_Uchiha/compression_uncertainity/iv_demo/64.png").convert("RGBA")
# map_img= Image.open("/home/uchihadj/PhD_Uchiha/compression_uncertainity/map.png").convert("RGBA")

# #merged = Image.alpha_composite(map_img, objects_img)
# # Adjust alpha (0.0 = all map, 1.0 = all objects)
# merged = Image.blend(map_img, objects_img, alpha=0.7)



# merged.save("/home/uchihadj/PhD_Uchiha/compression_uncertainity/merged_pred_uncert/merged_64_7.png")
# print("Saved merged.png")

import cv2
import numpy as np

# Hardcoded paths
dynamic_path = "/home/uchihadj/PhD_Uchiha/compression_uncertainity/iv_demo/0.png"
static_path  = "/home/uchihadj/PhD_Uchiha/compression_uncertainity/map.png"
output_path  = "/home/uchihadj/PhD_Uchiha/compression_uncertainity/merged_pred_uncert/merged_0.png"

# Read dynamic as grayscale, static as color
dynamic_fig = cv2.imread(dynamic_path, 0)        # grayscale
static_fig  = cv2.imread(static_path)            # BGR color

# Binarize dynamic: any non-zero pixel → 1
dynamic_fig[dynamic_fig > 0] = 1

# Wherever dynamic has content, paint white on static
static_fig[dynamic_fig == 1] = np.array([255, 255, 255])

cv2.imwrite(output_path, static_fig)
print(f"Saved: {output_path}")