# Motion Detection with Video Streaming Pipeline

This project implements a motion detection system using a pipeline of video processing stages. The pipeline consists of three main stages:

- **Streamer**
  - This stage reads frames from a video file and resizes them if necessary.

- **Detector**
  - This stage applies a motion detection algorithm to each frame and identifies bounding boxes around detected motion.

- **Player**
  - This stage displays the video frames with detected motion bounding boxes overlaid.

## Installation

```bash
pip install -r requirements.txt


## Usage

```bash
python main.py --video_path=People.mp4
