from logging import getLogger
from multiprocessing import shared_memory

import cv2
import imutils
import numpy as np

from utils import clear_queue


class Detector():
    def __init__(self, min_area, frame_rate, skip_frames=1):
        self.min_area = min_area
        self.frame_rate = frame_rate
        self.skip_frames = skip_frames
        self.logger = getLogger(self.__class__.__name__)

    def start(self, in_memory_name, out_memory_name, event, out_event):
        # Shared memories
        shared_in_memory = shared_memory.SharedMemory(name=in_memory_name)
        shared_out_memory = shared_memory.SharedMemory(name=out_memory_name)

        # Numpy Array
        in_np_array = np.ndarray((720, 1280, 3), dtype=np.uint8, buffer=shared_in_memory.buf)
        out_np_array = np.ndarray((720, 1280, 3), dtype=np.uint8, buffer=shared_out_memory.buf)

        firstFrame = None
        frame_gap_for_detection = int(self.frame_rate / 3)
        self.logger.info('Starting detector')
        i = 0
        detections = []
        while True:
            event.wait()  # wait for event from streamer
            frame = in_np_array.copy()  # copy frame from shared memory
            event.clear()  # clear event

            detections = []
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ...

            if i % self.skip_frames == 0:
                np.copyto(out_np_array, frame)  # copy frame to shared memory
                out_event.set()  # set event for player

            i += 1
            ...

        # Close shared memory
        shared_in_memory.close()
        shared_out_memory.close()