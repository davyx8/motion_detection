from multiprocessing import Process, Queue, shared_memory, Event

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
    sm_in_frame = shared_memory.SharedMemory(create=True, size=720 * 1280 * 3)
    sm_out_frame = shared_memory.SharedMemory(create=True, size=720 * 1280 * 3)

    # Events for synchronization
    events = Event()
    out_event = Event()

    streamer = Streamer(args.video_path, skip_frames=args.skip_frames)
    frame_rate = streamer.get_frame_rate()

    detector = Detector(args.min_area, frame_rate, skip_frames=args.skip_frames)

    player = Player(blur=args.blur, frame_rate=frame_rate, start_time=streamer.start_time, skip_frames=args.skip_frames,out_shm_frame=sm_out_frame)

    p1 = Process(target=streamer.start, args=(sm_in_frame.name, events,))
    p2 = Process(target=detector.start, args=(sm_in_frame.name, sm_out_frame.name, events, out_event))
    p3 = Process(target=player.start, args=())  # This must be adapted similarly

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    # Don't forget to close and unlink shared memory
    sm_in_frame.close()
    sm_in_frame.unlink()
    sm_out_frame.close()
    sm_out_frame.unlink()