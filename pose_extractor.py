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

video = load_video( "Screen recording 2026-08-11 8.52.00 PM.mp4")


ret,frame = video.read()  #cap.read will capture the next frame, telling you wether it worked and the image iteslef
if ret:
  print("Frame 1 read")
  print("Frame Shape:",frame.shape)

else:
  print("Could not read the frame")



!wget -q https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task #downloads the AI model mediapipe
!pip install mediapipe

import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path="pose_landmarker_lite.task"),
    running_mode=VisionRunningMode.IMAGE)
landmarker = PoseLandmarker.create_from_options(options)


# Set up the detector using the model we just downloaded


video.set(cv2.CAP_PROP_POS_FRAMES, 30)
ret, frame = video.read()


rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

#change colors for Mediapipe


result = landmarker.detect(mp_image)
#run the detection

if result.pose_landmarks:
  left_elbow = result.pose_landmarks[0][13]
  print("Left elbow x:",left_elbow.x)
  print("Left elbow y:", left_elbow.y)
else:
  print("No pose landmarks detected.")

#shows the left elbow coordinates. left elbow is always number 13 in Mediapipe  
