import cv2
import time
from roi_manager import RoiManager
from object_detection import detect
from numpy import random
from models.experimental import attempt_load
from utils.general import select_device
import numpy as np
class LoiteringDetection:
    def __init__(self, model, device, img_size, colors, names, conf_thres, iou_thres, loitering_time_threshold=5):
        self.model = model
        self.device = device
        self.img_size = img_size
        self.colors = colors
        self.names = names
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.half = self.device.type != 'cpu'
        self.loitering_time_threshold = loitering_time_threshold

    def run(self, input_video):
        if self.half:
            self.model.half()

        roi_manager = RoiManager()
        cap = cv2.VideoCapture(input_video)

        cv2.namedWindow('Original Frame')
        cv2.setMouseCallback('Original Frame', roi_manager.mouse_callback)
        loitering_detected = False
        reset_timer = False
        timer = time.time()
        loitering_start_time = None
        loitering_end_time = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame. Exiting.")
                break

            overlay = roi_manager.draw_roi_overlay(frame, thickness=2)
            roi = roi_manager.extract_roi(frame)

            #v1 
            # if roi is not None and roi.size > 0:
            #     result,detections = detect(roi, self.model, self.device, self.img_size, self.colors, self.names, self.conf_thres, self.iou_thres, self.half)
            #     print(detections)
            #     if any(label == 'person' for label, *_ in detections):
            #         if time.time() - timer > self.loitering_time_threshold:
            #             print("A person is loitering")
                        
            #             cv2.putText(overlay, "A person is loitering", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            #             timer = time.time()    
            #             time.sleep(3)

            #v2
            if roi is not None and roi.size > 0:
                result,detections = detect(roi, self.model, self.device, self.img_size, self.colors, self.names, self.conf_thres, self.iou_thres, self.half)
                print(detections)
                person_detected = False
                if detections:
                    for detection in detections:
                        if len(detection) > 0 and detection[0] == 'person':
                            person_detected = True
                            break
                if person_detected:
                    if loitering_start_time is None:
                        loitering_start_time = time.time()
                    elif time.time() - loitering_start_time > self.loitering_time_threshold:
                        loitering_detected = True
                        loitering_end_time = time.time() + self.loitering_time_threshold
                else:
                    loitering_start_time = None
                    if loitering_detected and not reset_timer:
                        reset_timer = True
                        timer = time.time()
                    elif reset_timer and time.time() - timer > self.loitering_time_threshold:
                        loitering_detected = False
                        reset_timer = False

                if loitering_detected and time.time() < loitering_end_time:
                    cv2.putText(overlay, "LOITERING DETECTED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow('Original Frame', overlay)    
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                roi_manager.roi_points.clear()
                roi_manager.current_point = None
            elif key == 27:  # Escape key
                break
            
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    weights = 'yolov7-tiny.pt'
    conf_thres = 0.3
    iou_thres = 0.45
    device = ''
    img_size = 640
    device = select_device(device)
    half = device.type != 'cpu'
    model = attempt_load(weights, map_location=device)
    names = model.module.names if hasattr(model, 'module') else model.names
    input_video = "input1.mp4"
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    loitering_time_threshold = 3
    loitering_detection = LoiteringDetection(model, device, img_size, colors, names, conf_thres, iou_thres,loitering_time_threshold)
    loitering_detection.run(input_video)
