import time
from datetime import datetime, timedelta
from logging import getLogger, INFO, basicConfig

import cv2
from utils import clear_queue
class Player():
    def __init__(self, blur, frame_rate, start_time, skip_frames=5):
        self.blur = blur
        self.frame_rate = frame_rate
        self.start_time = start_time
        self.skip_frames = skip_frames
        self.logger =getLogger(self.__class__.__name__)
        basicConfig(level=INFO)

    def start(self, queue):
        i = 0
        self.logger.info('Starting player')
        while True:
            item = queue.get()
            i += 1
            if item is None:  # End item
                cv2.destroyAllWindows()
                return

            frame, detections = item
            if self.blur:
                for (x, y, w, h) in detections:
                    frame[y:y + h, x:x + w] = cv2.blur(frame[y:y + h, x:x + w], (30, 30))

            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            seconds_since_start = (datetime.now() - self.start_time).total_seconds()
            cv2.putText(frame, str(timedelta(seconds=int(seconds_since_start))),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

            cv2.imshow('Frame', frame)
            clear_queue(queue,num_to_clear=int(1e5))
            delay =int(1000 / self.frame_rate)

            # Uncomment the next line to use the adjusted delay
            # time.sleep(delay / 1000.0)

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
        self.logger.info('player stopped')