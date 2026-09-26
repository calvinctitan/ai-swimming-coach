# Measurement Definitions
This page will show how my code measures each metric, which is important so the research numbers are compared correctly with my own.

## 1. Elbow Catch Angle
- MediaPipe landmarks: shoulder (12), elbow (14), wrist (16) — right arm
- Math: Dot product (the dot product of two vectors is an algebraic operation that multiplies matching coordinates and adds the results to produce a single number, or scalar value), the inside angle of the elbow. Code: `calculate_angle()` in `pose_extractor.py`
- Coordinates: MediaPipe gives x and y as fractions (0–1) of the frame's width and height. They are converted to pixels before the math, otherwise tall (portrait) or wide videos stretch the angle
- Test: Ran the coordinates of the three points that form a line, result 180 degrees
- Catch frame: Picked by my eyes where the wrist stopped moving
- Conventions: Straight arms = 180 degrees, smaller angle = more bent
- Converting from papers that use flexion (bending a joint) (straight = 0°): flexion = 180 - my angle
- Camera: Side view, better if underwater

## Body roll, hand entry, stroke rate, kick pattern
Not defined yet.
