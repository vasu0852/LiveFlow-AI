import cv2
import numpy as np
import os

# Update heatmap data based on detected people (dummy example)
heatmap_data = np.zeros((500, 500), dtype=np.uint8)  # Create a blank grayscale image

# Simulate adding points to the heatmap (you should update this with real data)
def update_heatmap_data(center):
    x, y = center
    if 0 <= x < heatmap_data.shape[1] and 0 <= y < heatmap_data.shape[0]:
        heatmap_data[y, x] += 1  # Increment intensity where people are detected

# Generate a heatmap with proper colormap
def generate_heatmap():
    # Normalize the heatmap data to range [0, 255]
    heatmap_normalized = cv2.normalize(heatmap_data, None, 0, 255, cv2.NORM_MINMAX)

    # Apply colormap (ensuring it's grayscale before applying)
    heatmap_colored = cv2.applyColorMap(heatmap_normalized, cv2.COLORMAP_JET)

    # Save the heatmap image
    if not os.path.exists('static'):
        os.makedirs('static')

    cv2.imwrite('static/heatmap.png', heatmap_colored)

    return 'static/heatmap.png'  # Return path to the image

