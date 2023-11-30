from datetime import datetime
import cv2
from logging import getLogger, INFO, basicConfig
class Streamer():
    def __init__(self, src, resize=None, skip_frames=5):
        self.src = src
        self.resize = resize
        self.start_time = datetime.now()
        self.skip_frames = skip_frames
        self.logger = getLogger(self.__class__.__name__)
    def start(self, queue):
        self.logger.info('Starting streamer')
        cap = cv2.VideoCapture(self.src)
        i = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if self.resize is not None:
                frame = cv2.resize(frame, self.resize)

            if i % self.skip_frames == 0:
                queue.put(frame)
            i += 1
            # if i % 300 == 0:  # Check every 300 frames (adjust as needed)
            #     clear_queue(queue, num_to_clear=1e6)

        cap.release()
        queue.put(None)  # End item

        self.logger.info('streamer stopped')
    def get_frame_rate(self):
        cap = cv2.VideoCapture(self.src)
        return int(cap.get(cv2.CAP_PROP_FPS))