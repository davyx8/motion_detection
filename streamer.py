from datetime import datetime
import cv2

class Streamer():
    def __init__(self, src, resize=None, skip_frames=5):
        self.src = src
        self.resize = resize
        self.start_time = datetime.now()
        self.skip_frames = skip_frames

    def start(self, queue):
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

    def get_frame_rate(self):
        cap = cv2.VideoCapture(self.src)
        return int(cap.get(cv2.CAP_PROP_FPS))