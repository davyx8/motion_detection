import time
from datetime import datetime, timedelta

import cv2
from utils import clear_queue
class Player():
    def __init__(self, blur, frame_rate, start_time, skip_frames=5):
        self.blur = blur
        self.frame_rate = frame_rate
        self.start_time = start_time
        self.skip_frames = skip_frames

    def empty_queue(self, queue):
        print(f" qs {queue.qsize()}")
        print(f" empty {queue.empty()}")
        while not queue.empty():
            queue.get()
            print(f" get")

    def start(self, queue):
        i = 0
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
            print(f"qsize {queue.qsize()}")
            print(int( (self.frame_rate)))
            # time.sleep(100)
            # if cv2.waitKey(int( 1e4 / (self.frame_rate))) & 0xFF == ord('q'):
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
            #     break
