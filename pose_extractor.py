"""
pose_extractor.py — Phase 1 of the AI Swimming Coach.

Takes a swimming video, finds the swimmer's 33 body joints on every frame with
MediaPipe, calculates joint angles, and saves two files:
    joint_angles.json    -> joint positions + angles for every frame
    skeleton_output.mp4  -> the video with a skeleton drawn on top

Run it:
    python pose_extractor.py my_swim_video.mp4
"""

import json
import os
import sys
import urllib.request

import cv2               # OpenCV: opens videos and draws on frames
import mediapipe as mp   # Google's AI that finds body joints
import numpy as np       # does the angle math

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task"
MODEL_PATH = "pose_landmarker_full.task"

# MediaPipe always returns the 33 joints in this order, so position i in the list = joint number i.
# "left" and "right" mean the swimmer's own left and right.
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

# Pairs of joint numbers to connect with a line (MediaPipe's official skeleton)
POSE_CONNECTIONS = [
    # face
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8), (9, 10),
    # torso
    (11, 12), (11, 23), (12, 24), (23, 24),
    # left arm and hand
    (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    # right arm and hand
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    # left leg and foot
    (23, 25), (25, 27), (27, 29), (27, 31), (29, 31),
    # right leg and foot
    (24, 26), (26, 28), (28, 30), (28, 32), (30, 32),
]

# Each angle is measured at the middle joint: (first joint, middle joint, last joint)
ANGLES_TO_MEASURE = {
    "left_elbow_angle_degrees": ("left_shoulder", "left_elbow", "left_wrist"),
    "right_elbow_angle_degrees": ("right_shoulder", "right_elbow", "right_wrist"),
    "left_knee_angle_degrees": ("left_hip", "left_knee", "left_ankle"),
    "right_knee_angle_degrees": ("right_hip", "right_knee", "right_ankle"),
}


def download_model():
    # Only downloads the first time; after that the file is already there
    if not os.path.exists(MODEL_PATH):
        print("Downloading MediaPipe pose model...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def create_landmarker():
    options = mp.tasks.vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp.tasks.vision.RunningMode.VIDEO)  # VIDEO mode follows the swimmer from frame to frame
    return mp.tasks.vision.PoseLandmarker.create_from_options(options)


def load_video(filepath):
    cap = cv2.VideoCapture(filepath)  # Opens up the video file and hands you back the control
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {filepath}")

    print("Video Loaded")
    print("Total frames:", int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    return cap


def extract_joints(landmarker, frame, timestamp_ms):
    # Runs MediaPipe on one frame. Returns the 33 joints, or None if no person was found.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV stores colors as BGR, MediaPipe wants RGB
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    result = landmarker.detect_for_video(mp_image, timestamp_ms)
    if not result.pose_landmarks:
        return None
    return result.pose_landmarks[0]


def landmarks_to_dict(landmarks):
    # enumerate gives both the position number and the joint while looping. Match correct number with name
    joints = {}
    for i, landmark in enumerate(landmarks):
        joints[LANDMARK_NAMES[i]] = {
            "x": round(landmark.x, 4),
            "y": round(landmark.y, 4),
            # How sure MediaPipe is that the joint is visible (0-1). Low = hidden, e.g. the far arm underwater
            "visibility": round(landmark.visibility, 3),
        }
    return joints


def to_pixels(joint, width, height):
    # MediaPipe's x and y are fractions (0-1) of the frame's width and height.
    # Converting to pixels first stops tall or wide videos from stretching the angles.
    return (joint["x"] * width, joint["y"] * height)


def calculate_angle(a, b, c):
    # Angle at point b, in degrees, made by points a-b-c (each an (x, y) in pixels).
    # Straight line = 180 degrees, smaller = more bent.
    ba = np.array(a) - np.array(b)  # vector from the middle joint to a
    bc = np.array(c) - np.array(b)  # vector from the middle joint to c

    lengths = np.linalg.norm(ba) * np.linalg.norm(bc)
    if lengths == 0:  # two joints are on top of each other, so there is no angle
        return None

    cosine = np.dot(ba, bc) / lengths
    angle = np.degrees(np.arccos(np.clip(cosine, -1.0, 1.0)))  # clip guards against tiny rounding errors
    return round(float(angle), 1)


def add_angles(joints, width, height):
    for angle_name, (a, b, c) in ANGLES_TO_MEASURE.items():
        joints[angle_name] = calculate_angle(
            to_pixels(joints[a], width, height),
            to_pixels(joints[b], width, height),
            to_pixels(joints[c], width, height))
    return joints


def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved to", filename)


def draw_skeleton_lines(frame, landmarks, connections):
    height, width, _ = frame.shape
    for start_idx, end_idx in connections:
        start = landmarks[start_idx]
        end = landmarks[end_idx]
        start_point = (int(start.x * width), int(start.y * height))
        end_point = (int(end.x * width), int(end.y * height))
        cv2.line(frame, start_point, end_point, (255, 255, 255), 2)   # white line
    return frame


def draw_skeleton_dots(frame, landmarks):
    height, width, _ = frame.shape
    for landmark in landmarks:
        x = int(landmark.x * width)
        y = int(landmark.y * height)
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # green dot
    return frame


def process_video(video_path, json_path="joint_angles.json", output_video_path="skeleton_output.mp4"):
    download_model()
    cap = load_video(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # some files don't report their speed; 30 is a safe guess

    all_frames_data = {}
    out = None
    frame_number = 0

    with create_landmarker() as landmarker:
        while True:
            success, frame = cap.read()
            if not success:
                break

            height, width, _ = frame.shape
            if out is None:
                # Size the output video from a real frame so it always matches (phone videos can be rotated)
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

            timestamp_ms = int(frame_number * 1000 / fps)  # VIDEO mode needs to know when each frame happens
            landmarks = extract_joints(landmarker, frame, timestamp_ms)

            if landmarks:   # only save and draw if a person was actually detected in this frame
                joints = landmarks_to_dict(landmarks)
                add_angles(joints, width, height)
                all_frames_data[f"frame_{frame_number:03d}"] = joints

                frame = draw_skeleton_lines(frame, landmarks, POSE_CONNECTIONS)
                frame = draw_skeleton_dots(frame, landmarks)   # dots last so the lines don't cover them

            out.write(frame)   # save this frame into the output video
            frame_number += 1

    cap.release()
    if out is not None:
        out.release()

    print("Processed", frame_number, "frames,", len(all_frames_data), "with a swimmer detected")
    save_to_json(all_frames_data, json_path)
    print("Saved skeleton video to", output_video_path)
    return all_frames_data


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pose_extractor.py <video file>")
        sys.exit(1)
    process_video(sys.argv[1])
