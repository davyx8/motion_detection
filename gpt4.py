import cv2
import imutils
from datetime import datetime
from multiprocessing import Process, Queue

class Streamer():
    def __init__(self, src, resize=None):
        self.src = src
        self.resize = resize

    def start(self, queue):
        cap = cv2.VideoCapture(self.src)
        while cap.isOpened():
          ret, frame = cap.read()
          if not ret: break
          
          if self.resize is not None:
            frame = cv2.resize(frame, self.resize)
          
          queue.put(frame)
        cap.release()

    def get_frame_rate(self):
        cap = cv2.VideoCapture(self.src)
        return int(cap.get(cv2.CAP_PROP_FPS))

class Detector():
  def __init__(self, min_area):
    self.min_area = min_area

  def start(self, in_queue, out_queue):
    firstFrame = None
    while True:
      frame = in_queue.get()
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

      detections = []
      for c in cnts:
        if cv2.contourArea(c) < self.min_area:
          continue
        
        (x, y, w, h) = cv2.boundingRect(c)
        detections.append((x, y, w, h))
      
      out_queue.put((frame, detections))

class Player():
  def __init__(self, blur,frame_rate):
    self.blur = blur
    self.frame_rate = frame_rate

  def start(self, queue):
    while True:
      frame, detections = queue.get()
      if self.blur:
        for (x, y, w, h) in detections:
          frame[y:y+h, x:x+w] = cv2.blur(frame[y:y+h, x:x+w], (30, 30))

      for (x, y, w, h) in detections:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

      cv2.putText(frame, datetime.now().strftime("%H:%M:%S:%f"),
          (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1)
      
      cv2.imshow("Frame", frame)
      if cv2.waitKey(int(1000 / self.frame_rate)) & 0xFF == ord('q'):
        break

if __name__ == "__main__":
  queue_stream_detect = Queue()
  queue_detect_play = Queue()

  streamer = Streamer('/home/david/Downloads/People-6387.mp4')
  frame_rate = streamer.get_frame_rate()
  detector = Detector(500)
  player = Player(blur = False,frame_rate=frame_rate)

  p1 = Process(target=streamer.start, args=(queue_stream_detect,))
  p2 = Process(target=detector.start, args=(queue_stream_detect, queue_detect_play))
  p3 = Process(target=player.start, args=(queue_detect_play,))

  p1.start()
  p2.start()
  p3.start()
  
  p1.join()
  p2.join()
  p3.join()