import argparse
import time
from pathlib import Path
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized


def mouse_callback(event, x, y, flags, param):
    global roi_points, drawing, current_point

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        roi_points.append((x, y))
        current_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            current_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        roi_points.append((x, y))
        current_point = None

    elif event == cv2.EVENT_RBUTTONDOWN:
        roi_points.clear()
        current_point = None

def gradient_color(point_a, point_b, steps):
    delta = (np.array(point_b) - np.array(point_a)) / steps
    colors = [tuple(np.array(point_a) + delta * i) for i in range(steps + 1)]
    return colors

def draw_roi_overlay(frame, roi_points, thickness=4):
    global current_point
    num_points = len(roi_points)
    color_line = (0, 165, 255)
    color_outer_circle = (0, 165, 255)
    color_inner_circle = (0, 0, 0)

    overlay = frame.copy()

    if num_points > 1:
        for i in range(num_points - 1):
            cv2.line(overlay, roi_points[i], roi_points[i + 1], color_line, thickness, cv2.LINE_AA)
            cv2.circle(overlay, roi_points[i], 6, color_outer_circle, -1, cv2.LINE_AA)
            cv2.circle(overlay, roi_points[i], 3, color_inner_circle, -1, cv2.LINE_AA)
        if current_point is not None:
             cv2.line(overlay, roi_points[-1], current_point, color_line, thickness, cv2.LINE_AA)
    elif num_points == 1:
        cv2.circle(overlay, roi_points[0], 6, color_outer_circle, -1, cv2.LINE_AA)
        cv2.circle(overlay, roi_points[0], 3, color_inner_circle, -1, cv2.LINE_AA)
    # Add this part to show the completed ROI polygon when the user is not drawing
    if not drawing and num_points > 2:
        cv2.line(overlay, roi_points[-1], roi_points[0], color_line, thickness, cv2.LINE_AA)

    return overlay

def extract_roi(image, roi_points):
    if len(roi_points) < 3:
        return None

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [np.array(roi_points, dtype=np.int32)], 255)

    roi = cv2.bitwise_and(image, image, mask=mask)
    x, y, w, h = cv2.boundingRect(np.array(roi_points, dtype=np.int32))
    roi_cropped = roi[y:y+h, x:x+w]
    return roi_cropped