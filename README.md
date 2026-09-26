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

1. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
2. Run the pose extractor on a swimming video:
   ```
   python pose_extractor.py my_swim_video.mp4
   ```
   The first run downloads MediaPipe's pose model automatically.

In Google Colab, put a `!` in front of each command, e.g. `!python pose_extractor.py my_swim_video.mp4`.

It creates:
- `joint_angles.json` — joint positions and elbow/knee angles for every frame where a swimmer is found
- `skeleton_output.mp4` — the video with the skeleton drawn on top

## Project files

| File | What it does |
| --- | --- |
| `pose_extractor.py` | Finds the 33 body joints on every frame, calculates joint angles, and draws the skeleton |
| `time_standards.py` | USA Swimming 100 free time standards for each age group |
| `research/measurement_definitions.md` | How each metric is measured, so it can be compared with research papers |
