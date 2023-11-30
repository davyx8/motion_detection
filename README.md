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
```

## Usage

```bash
python main.py --video_path=People.mp4 --min_area 500 --blur
```

## Limitations
- Variable FPS videos are not supported, video might get jumpy
- The video is not saved, only displayed.
- RTSP and HLS streams are not supported.
- The motion detection algorithm is not very robust and might detect false positives.
- The motion detection algorithm is not very efficient and might not run in real-time on low-end machines.

# DISCLAIMER
ALL the code included was generated using WizardCoder LLM ( https://huggingface.co/WizardLM/WizardCoder-15B-V1.0) and also  Phind-CodeLlama-34B-v2 (https://huggingface.co/Phind/Phind-CodeLlama-34B-v2).
Prompts used are included in prompts.txt file. 
Yes i write code like this, and yes i am proud of it, so long as it works and i can understand it.
even this readme was generated using WizardCoder LLM. 
