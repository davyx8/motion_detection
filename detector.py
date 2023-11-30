import cv2
import imutils
from utils import clear_queue
class Detector():
    def __init__(self, min_area ,frame_rate ,skip_frames=1):
        self.min_area = min_area
        self.frame_rate =frame_rate
        self.skip_frames = skip_frames

    def start(self, in_queue, out_queue):
        firstFrame = None
        frame_gap_for_detection = int(self.frame_rate / 3)
        print(frame_gap_for_detection)

        i = 0
        detections = []
        while True:
            print(in_queue.qsize())
            print(out_queue.qsize())
            frame = in_queue.get()

            if frame is None:  # End item
                out_queue.put(None)
                return

            detections = []

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if firstFrame is None:
                firstFrame = gray
                continue

            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            for c in cnts:
                if cv2.contourArea(c) < self.min_area:
                    continue

                (x, y, w, h) = cv2.boundingRect(c)
                detections.append((x, y, w, h))
            if i % self.skip_frames == 0:
                out_queue.put((frame, detections))
            i += 1
            if i%10 == 0:
                clear_queue(out_queue)