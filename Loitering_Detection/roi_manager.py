
import cv2
import numpy as np

class RoiManager:
    """
    RoiManager class is responsible for handling user interactions and drawing
    the region of interest (ROI) polygon on the input frame.
    """
    def __init__(self):
        self.roi_points = []
        self.drawing = False
        self.current_point = None

    def mouse_callback(self, event, x, y, flags, param):
        """
        Mouse callback function to handle mouse events.
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.roi_points.append((x, y))
            self.current_point = (x, y)

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                self.current_point = (x, y)

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.roi_points.append((x, y))
            self.current_point = None

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.roi_points.clear()
            self.current_point = None

    def draw_roi_overlay(self, frame, thickness=4):
        """
        Draw the ROI polygon overlay on the input frame.
        """
        num_points = len(self.roi_points)
        color_line = (0, 165, 255)
        color_outer_circle = (0, 165, 255)
        color_inner_circle = (0, 0, 0)

        overlay = frame.copy()

        if num_points > 1:
            for i in range(num_points - 1):
                cv2.line(overlay, self.roi_points[i], self.roi_points[i + 1], color_line, thickness, cv2.LINE_AA)
                cv2.circle(overlay, self.roi_points[i], 6, color_outer_circle, -1, cv2.LINE_AA)
                cv2.circle(overlay, self.roi_points[i], 3, color_inner_circle, -1, cv2.LINE_AA)
            if self.current_point is not None:
                 cv2.line(overlay, self.roi_points[-1], self.current_point, color_line, thickness, cv2.LINE_AA)
        elif num_points == 1:
            cv2.circle(overlay, self.roi_points[0], 6, color_outer_circle, -1, cv2.LINE_AA)
            cv2.circle(overlay, self.roi_points[0], 3, color_inner_circle, -1, cv2.LINE_AA)

        if not self.drawing and num_points > 2:
            cv2.line(overlay, self.roi_points[-1], self.roi_points[0], color_line, thickness, cv2.LINE_AA)

        return overlay

    def extract_roi(self, image):
        """
        Extract the ROI from the input image.
        """
        if len(self.roi_points) < 8:
            return None

        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [np.array(self.roi_points, dtype=np.int32)], 255)

        roi = cv2.bitwise_and(image, image, mask=mask)
        x,y, w, h = cv2.boundingRect(np.array(self.roi_points, dtype=np.int32))
        roi_cropped = roi[y:y+h, x:x+w]
        return roi_cropped