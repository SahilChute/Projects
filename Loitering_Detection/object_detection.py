import time
import torch
import cv2
from numpy import random
import numpy as np
from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords, xyxy2xywh, select_device
from utils.plots import plot_one_box

def detect(img0, model, device, imgsz, colors, names, conf_thres, iou_thres, half):
    # Run inference
    img = letterbox(img0, imgsz, stride=int(model.stride.max()))[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()
    img /= 255.0

    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    with torch.no_grad():
        pred = model(img)[0]

    pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=True)
    
    # Process detections
    detections = []
    for i, det in enumerate(pred):
        if len(det):
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], img0.shape).round()

            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, img0, label=label, color=colors[int(cls)], line_thickness=1)
                detections.append((names[int(cls)], conf.item(), *map(int, xyxy)))
    return img0,detections 