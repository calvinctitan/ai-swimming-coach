# AI-Swimming-Coach 🏊
An AI system that analyzes swimming technique using computer vision to generate personalized coaching feedback.

## Demo

Watch the skeletal tracking system in action:

https://www.loom.com/share/acb502c9f455495eb6fa97f4ecbdd095

**Built with:** MediaPipe · OpenCV · Google Gemini AI · Python · Streamlit

**Status:** Phase 2 — The Biomechanics Brain

**Current task:** Researching elite swimming biomechanics (step 2.1)

**Started:** July 2026

## How to run

1. Install the libraries: `pip install -r requirements.txt`
2. Download the MediaPipe pose model into this folder: https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task
3. Put your video in this folder, set `video_file` in `pose_extractor.py` to its name, then run `python pose_extractor.py`

In Google Colab, put a `!` in front of each command.

It saves `joint_angles.json` (joint positions in pixels and elbow/knee angles) and `skeleton_output.mp4` (the video with the skeleton drawn on it).
