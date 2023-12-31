import cv2
import imutils
from datetime import datetime, timedelta
from multiprocessing import Process, Queue



import argparse
from detector import Detector
from player import Player
from streamer import Streamer
from logging import getLogger, INFO, basicConfig
logger = getLogger(__name__)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, required=True,
                        help='Path to the video file')
    parser.add_argument('--min_area', type=int, default=500, help='Minimum area of a detected motion')
    parser.add_argument('--blur', action='store_true', help='Enable blur for detected motion')
    parser.add_argument('--skip_frames', type=int, default=1, help='Skip frames to reduce processing time')
    args = parser.parse_args()

    queue_stream_detect = Queue(300)
    queue_detect_play = Queue(300)

    streamer = Streamer(args.video_path, skip_frames=args.skip_frames)
    frame_rate = streamer.get_frame_rate()

    detector = Detector(args.min_area, frame_rate,skip_frames=args.skip_frames)

    player = Player(blur=args.blur, frame_rate=frame_rate, start_time=streamer.start_time, skip_frames=args.skip_frames)

    p1 = Process(target=streamer.start, args=(queue_stream_detect,))
    p2 = Process(target=detector.start, args=(queue_stream_detect, queue_detect_play))
    p3 = Process(target=player.start, args=(queue_detect_play,))
    logger.info('Starting processes ')
    p1.start( )
    p2.start()
    p3.start()

    p1.join()
    logger.info('Processing wrapup')
    queue_stream_detect.put(None)  # Signal detector to stop
    p2.join()
    queue_detect_play.put(None)
    p3.join()
    logger.info("Done!")