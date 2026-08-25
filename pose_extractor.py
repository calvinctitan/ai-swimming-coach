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

# Initial load of the image and read its single frame
video_capture_object = load_video( "IMG_7411.JPG")
ret,frame = video_capture_object.read()  #cap.read will capture the next frame, telling you wether it worked and the image iteslef
if ret:
  print("Frame 1 read")
  print("Frame Shape:",frame.shape)

else:
  print("Could not read the frame")



!wget -q https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task #download the mediapipe
!pip install mediapipe

import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker_full.task"),
    running_mode=VisionRunningMode.IMAGE)
landmarker = PoseLandmarker.create_from_options(options)
# Set up the detector using the model we just downloaded


# This section was problematic for images. Using the frame from the initial load.
# The 'target_frame' loop is only necessary for processing multiple frames of a video.
# Since IMG_7411.JPG is a single image, we use the 'frame' already read.

print("Actually on frame:", video_capture_object.get(cv2.CAP_PROP_POS_FRAMES))

if ret: # Using the 'ret' and 'frame' from the initial successful read
    from google.colab.patches import cv2_imshow
    cv2_imshow(frame)
else:
    print("No frame to display as initial read failed.")




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


  #enumerate gives both the position number and the body part while looping. Match correct number with name
  for i, landmark in enumerate(result.pose_landmarks[0]):
    name = LANDMARK_NAMES[i]
    joints[name]={"x": landmark.x, "y": landmark.y}
  return joints

# Call extracting_joints with the valid 'frame' if it was successfully loaded
joints = None
if ret:
    joints = extracting_joints(frame)


if joints:
   for name, coords in joints.items():
    print(name,coords)

else:
  print("No joints/pose landmarks found")




#shows the left elbow coordinates. left elbow is always number 13 in Mediapipe


import json

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved to", filename)

video = load_video("Swimtestone (1).mp4")

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

    
    all_frames_data[frame_number] = joints

  frame_number += 1

print ("Processed", len(all_frames_data),"frames with detected joints" )
save_to_json(all_frames_data, "joint_angles.json")

  
#put everything into one single file 
