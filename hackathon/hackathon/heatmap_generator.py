import numpy as np
import cv2
import os

heatmap_data = []

def update_heatmap_data(center_point):
    heatmap_data.append(center_point)

def generate_heatmap(filename='static/heatmap.png', width=640, height=480):
    heatmap = np.zeros((height, width), dtype=np.uint8)

    for (x, y) in heatmap_data:
        if 0 <= x < width and 0 <= y < height:
            heatmap[y, x] += 10  # Increase intensity

    heatmap = np.clip(heatmap, 0, 255).astype(np.uint8)

    # ✅ Apply Gaussian blur to make it smoother
    heatmap = cv2.GaussianBlur(heatmap, (31, 31), 0)

    # ✅ Apply color map - after converting to 8-bit grayscale
    heatmap_color = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # ✅ Save to static folder
    os.makedirs('static', exist_ok=True)
    cv2.imwrite(filename, heatmap_color)
