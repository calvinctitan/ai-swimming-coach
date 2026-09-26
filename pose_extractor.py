import cv2   # this line load openCV for the machine to use

def load_video(filepath):
  cap = cv2.VideoCapture(filepath)  # Opens up the video file and hands you back the control


  if cap.isOpened():         # checks if the file is opened or not
    print("Video Loaded")

    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) #counts how many frames there are.
    print("Total frames:", frame_count)

  else:
    print("Video Not Loaded")
  return cap

import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker_full.task"),
    running_mode=VisionRunningMode.IMAGE)
landmarker = PoseLandmarker.create_from_options(options)
# Set up the detector using the model file pose_landmarker_full.task (download link in README)


LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear", "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_pinky", "right_pinky",
    "left_index", "right_index", "left_thumb", "right_thumb",
    "left_hip", "right_hip", "left_knee", "right_knee",
    "left_ankle", "right_ankle", "left_heel", "right_heel",
    "left_foot_index", "right_foot_index"
]



def extracting_joints(frame):
  # Ensure frame is not empty before processing
  if frame is None or frame.size == 0:
      print("Error: Empty frame passed to extracting_joints.")
      return None

  rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

#change colors for Mediapipe
  result = landmarker.detect(mp_image)
#run the detection

  if not result.pose_landmarks:
    return None

  joints = {}
  height, width, _ = frame.shape   # size of the frame in pixels


  #enumerate gives both the position number and the body part while looping. Match correct number with name
  for i, landmark in enumerate(result.pose_landmarks[0]):
    name = LANDMARK_NAMES[i]
    joints[name]={"x": landmark.x * width, "y": landmark.y * height}   # turn MediaPipe's 0-1 values into pixels so angles aren't stretched
  return joints


import json

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved to", filename)

#Angle calculator

import numpy as np # introduce arrays in this python
#as np introduces it as a shortcut
def calculate_angle(A,B,C):

  a = np.array([A["x"], A["y"]])
  b = np.array([B["x"], B["y"]])   # elbow — the middle point
  c = np.array([C["x"], C["y"]])

  ba = a - b   # arrow from elbow to shoulder
  bc = c - b   # arrow from elbow to wrist
  cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
  angle = np.degrees(np.arccos(cosine_angle))  #mediapipe angle calculation formula

  return angle


video_file = "Jumping.MOV"   # can be changed with different files
video = load_video(video_file)

all_frames_data = {}
frame_number = 0

while True:
  ret, frame = video.read()
  if not ret:
    break

  if frame_number %10 ==0:  
    joints = extracting_joints(frame)

    if joints is not None:
      frame_key =  f"frame_{frame_number:03d}"

      joints["left_elbow_angle_degrees"] = calculate_angle(
        joints["left_shoulder"], joints["left_elbow"], joints["left_wrist"])

      joints["right_elbow_angle_degrees"] = calculate_angle(
        joints["right_shoulder"], joints["right_elbow"], joints["right_wrist"])

      joints["left_knee_angle_degrees"] = calculate_angle(
        joints["left_hip"], joints["left_knee"], joints["left_ankle"])

      joints["right_knee_angle_degrees"] = calculate_angle(
         joints["right_hip"], joints["right_knee"], joints["right_ankle"])

      all_frames_data[frame_key] = joints   # only save frames where a person was found

  frame_number += 1

print ("Processed", len(all_frames_data),"frames with detected joints" )
save_to_json(all_frames_data, "joint_angles.json")



# Pairs of joint numbers to connect with lines (MediaPipe's official list)
POSE_CONNECTIONS = [
    (0, 1), (0, 4), (1, 2), (2, 3), (4, 5), (5, 6), (3, 7), (6, 8),
    (9, 10), (11, 12), (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    (11, 23), (12, 24),   # shoulders to hips
    (23, 24), (23, 25), (25, 27), (27, 29), (29, 31), (27, 31),
    (24, 26), (26, 28), (28, 30), (30, 32), (28, 32)
]


def extract_joints(frame):
    if frame is None or frame.size == 0:
        print("Error: Empty frame passed to extract_joints.")
        return None

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    result = landmarker.detect(mp_image)

    if not result.pose_landmarks:
        return None
    return result.pose_landmarks[0] 

def draw_skeleton_dots(frame, landmarks):
    height, width, _ = frame.shape
    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  #turns into green 
    return frame

def draw_skeleton_lines(frame, landmarks, connections):
    height, width, _ = frame.shape
    for start_idx, end_idx in connections:
        
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            start = landmarks[start_idx]
            end = landmarks[end_idx]
            start_point = (int(start.x * width), int(start.y * height))
            end_point = (int(end.x * width), int(end.y * height))
            cv2.line(frame, start_point, end_point, (255, 255, 255), 2)   # white line
    return frame



cap = load_video(video_file)

# Get the video's own width, height, and speed, so our output video matches it
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)

# Set up a writer that will save our drawn-on frames into a new video file
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("skeleton_output.mp4", fourcc, fps, (width, height))

while True:
    success, frame = cap.read()
    if not success:
        break   

    landmarks = extract_joints(frame)

    if landmarks:   # only draw if a person was actually detected in this frame
        frame = draw_skeleton_dots(frame, landmarks)
        frame = draw_skeleton_lines(frame, landmarks, POSE_CONNECTIONS)

    out.write(frame)   # save this frame into the output video

cap.release()
out.release()
print("Done! Check colab for output")
