import cv2   # this line load openCV for the machine to use

def load_video(filepath):
  cap = cv2.VideoCapture(filepath)  # Opens up the video file and hands you back the control


  if cap.isOpened():         # checks if the file is opened or not
    print("Video Loaded")
    
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) #countes the number of Frames
    print("Total frames:", frame_count)

  else:
    print("Video Not Loaded")
  return cap

video = load_video( "Screen recording 2026-08-11 8.52.00 PM.mp4")
