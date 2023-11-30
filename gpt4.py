import cv2
import imutils
from datetime import datetime, timedelta
from multiprocessing import Process, Queue

class Streamer():
    def __init__(self, src, resize=None,skip_frames=3):
        self.src = src
        self.resize = resize
        self.start_time = datetime.now()
        self.skip_frames=skip_frames

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
            i +=1
        
        cap.release()
        queue.put(None)  # End item

    def get_frame_rate(self):
        cap = cv2.VideoCapture(self.src)
        return int(cap.get(cv2.CAP_PROP_FPS))


class Detector():
    def __init__(self, min_area,frame_rate):
        self.min_area = min_area
        self.frame_rate =frame_rate

    def start(self, in_queue, out_queue):
        firstFrame = None
        frame_gap_for_detection = int(self.frame_rate/3)
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
            
            out_queue.put((frame, detections))


class Player():
    def __init__(self, blur, frame_rate, start_time,skip_frames=5):
        self.blur = blur
        self.frame_rate = frame_rate
        self.start_time = start_time
        self.skip_frames = skip_frames
    def empty_queue(self,queue):
        print(f" qs {queue.qsize()}" )
        print(f" empty {queue.empty()}" )
        while not queue.empty():
            
            queue.get()
            print(f" get" )
    def start(self, queue):
        i=0
        while True:
            item = queue.get()
            i +=1

            # if i % self.skip_frames != 0:
                # continue
            if item is None:  # End item
                cv2.destroyAllWindows()
                return
            
            frame, detections = item
            if self.blur:
                for (x, y, w, h) in detections:
                    frame[y:y+h, x:x+w] = cv2.blur(frame[y:y+h, x:x+w], (30, 30))
            
            for (x, y, w, h) in detections:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            seconds_since_start = (datetime.now() - self.start_time).total_seconds()
            cv2.putText(frame, str(timedelta(seconds=int(seconds_since_start))),
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            
            cv2.imshow('Frame', frame)
            self.empty_queue(queue)
            if cv2.waitKey(100) & 0xFF == ord('q'):
            # if cv2.waitKey(100) & 0xFF == ord('q'):
                break


if __name__ == "__main__":
    
    queue_stream_detect = Queue()
    queue_detect_play = Queue()
    
    streamer = Streamer('/mnt/Video-DB/Test_Videos/Short/Datatang-1-China-Location-0-2_S1.mp4')
    frame_rate = streamer.get_frame_rate()
    
    detector = Detector(500,frame_rate)
    
    player = Player(blur=False, frame_rate=frame_rate, start_time=streamer.start_time)
    
    p1 = Process(target=streamer.start, args=(queue_stream_detect,))
    p2 = Process(target=detector.start, args=(queue_stream_detect, queue_detect_play))
    p3 = Process(target=player.start, args=(queue_detect_play,))
    
    p1.start()  
    p2.start() 
    p3.start()   
    
    p1.join()
    queue_stream_detect.put(None)  # Signal detector to stop
    p2.join()
    queue_detect_play.put(None)
    p3.join()