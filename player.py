import time
from datetime import datetime, timedelta
from logging import getLogger, INFO, basicConfig

import cv2
from utils import clear_queue
import numpy as np
from multiprocessing import shared_memory
class Player():
    def __init__(self, blur, frame_rate, start_time, end_event, shared_frame, shared_detections, skip_frames=5):
       ...
       self.shared_frame = shared_frame
       self.shared_detections = shared_detections
       ...

    def start(self):
        ...
        while not end_event.is_set():
            ...
            frame_jpg = bytes(shared_frame.buf)
            frame = cv2.imdecode(np.frombuffer(frame_jpg, np.uint8), cv2.IMREAD_COLOR)
            ...
            detections = _get_shared_memory_list(shared_detections)
            ...
        ...
class Player():
    def __init__(self, blur, frame_rate, start_time, out_shm_frame, skip_frames=5):
        self.blur = blur
        self.frame_rate = frame_rate
        self.start_time = start_time
        self.out_shm_frame = out_shm_frame
        self.skip_frames = skip_frames
        self.logger = getLogger(self.__class__.__name__)
        basicConfig(level=INFO)

    def start(self):
        i = 0
        self.logger.info('Starting player')
        shm_frame = shared_memory.SharedMemory(name=self.out_shm_frame)
        frame_size = shm_frame.size // 3  # Assuming 3 channels (BGR)
        frame_shape = (int(frame_size ** 0.5), int(frame_size ** 0.5), 3)
        frame = np.ndarray(frame_shape, dtype=np.uint8, buffer=shm_frame.buf)

        while True:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            if i % self.skip_frames == 0:
                seconds_since_start = (datetime.now() - self.start_time).total_seconds()
                cv2.putText(frame, str(timedelta(seconds=int(seconds_since_start))),
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

                cv2.imshow('Frame', frame)

            i += 1

        shm_frame.close()
        cv2.destroyAllWindows()
        self.logger.info('Player stopped')
