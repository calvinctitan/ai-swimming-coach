# Measurements Definitions 
This page will show how my code measures each metric, which is important so the research numbers are compared correctly with my own.

## 1, Elbow Catch Angle
- Mediapipe landmarks: shoulder (12), elbow (14), wrist (16) — right arm
- Math: Dot product(The dot product of two vectors is an algebraic operation that multiplies matching coordinates and adds the results to produce a single number, or scalar value), the inside angle of the elbow. 
- Test: Ran the coordinates of the three points that form a line, result 180 degrees
- Catch frame: Picked by my eyes where the wrist stops moving forward but moves backwards.
- Conventions: Straight arms = 180 degrees, smaller angle = more bent
- Converting from papers that use flexion(bending a joint) (straight = 0°): flexion = 180 - my angle
- Camera: Side view, better if underwater


## 2, Stroke Rate
- Stroke rate = full arm movement cycle per minute with both hands. One cycle = right arm + left arm.
- Landmark: wrist (15 = left, 16 = right), tracked across frames.
- Finding a cycle: count the frames between two times the same hand enters the water for one cycle.
- Math: cycles per minute = 60 × fps ÷ frames per cycle. Average over several cycles, not just one.
- fps: read from the video with `cv2.CAP_PROP_FPS` 
- Camera: side view, top view, or any other view that includes the motion of the hand.
- Units note: some papers report stroke frequency in Hz (cycles per second), so Hz × 60 = cycles per minute. Also check whether a paper counts one arm or both arms as one stroke (single-arm counts would double the number).
- Pace: stroke rate changes a lot with pace (sprint vs. distance), so always record the pace next to the number.
- Test: 45 frames per cycle at 30 fps gives 40 cycles per minute. Test program:https://colab.research.google.com/drive/1RgusBphoAbx0oTZMmGaDVgAGTK9i_uyN
  

## Body roll, hand entry,  kick pattern
Not defined yet.
