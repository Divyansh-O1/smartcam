"""
SMARTCAM AI

Copyright (c) 2026
Divyansh Tiwari

All Rights Reserved.

Unauthorized copying,
modification,
distribution,
or commercial use
is prohibited.
"""
from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import time
from deepface import DeepFace

app = Flask(__name__)

# ----------------------------------
# CAMERA
# ----------------------------------
camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

# ----------------------------------
# MEDIAPIPE
# ----------------------------------
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=10,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# ----------------------------------
# GLOBALS
# ----------------------------------
prev_time = time.time()

emotion_cache = {}
face_memory = {}

next_face_id = 1

# ----------------------------------
# TRACKER
# ----------------------------------
def get_face_id(cx, cy):

    global next_face_id

    for fid, pos in face_memory.items():

        px, py = pos

        distance = ((cx - px) ** 2 + (cy - py) ** 2) ** 0.5

        if distance < 100:

            face_memory[fid] = (cx, cy)

            return fid

    fid = next_face_id

    face_memory[fid] = (cx, cy)

    next_face_id += 1

    return fid

# ----------------------------------
# STREAM
# ----------------------------------
def generate_frames():

    global prev_time

    while True:

        success, frame = camera.read()

        if not success:
            continue

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(rgb)

        face_count = 0

        if results.multi_face_landmarks:

            face_count = len(results.multi_face_landmarks)

            for face_landmarks in results.multi_face_landmarks:

                h, w, _ = frame.shape

                xs = [int(lm.x * w) for lm in face_landmarks.landmark]
                ys = [int(lm.y * h) for lm in face_landmarks.landmark]

                x_min = max(min(xs), 0)
                x_max = min(max(xs), w)

                y_min = max(min(ys), 0)
                y_max = min(max(ys), h)

                cx = (x_min + x_max) // 2
                cy = (y_min + y_max) // 2

                face_id = get_face_id(cx, cy)

                # FACE OUTLINE ONLY
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None
                )

                # FACE BOX
                cv2.rectangle(
                    frame,
                    (x_min, y_min),
                    (x_max, y_max),
                    (0, 255, 255),
                    2
                )

                # CENTER DOT
                cv2.circle(
                    frame,
                    (cx, cy),
                    4,
                    (0, 0, 255),
                    -1
                )

                # ----------------------------------
                # EMOTION AI
                # ----------------------------------
                current_time = time.time()

                if face_id not in emotion_cache:

                    emotion_cache[face_id] = {
                        "emotion": "SCANNING",
                        "time": 0
                    }

                if current_time - emotion_cache[face_id]["time"] > 3:

                    try:

                        face_crop = frame[
                            y_min:y_max,
                            x_min:x_max
                        ]

                        if face_crop.size > 0:

                            result = DeepFace.analyze(
                                face_crop,
                                actions=["emotion"],
                                enforce_detection=False,
                                silent=True
                            )

                            if isinstance(result, list):
                                emotion = result[0]["dominant_emotion"]
                            else:
                                emotion = result["dominant_emotion"]

                            emotion_cache[face_id]["emotion"] = emotion.upper()
                            emotion_cache[face_id]["time"] = current_time

                    except Exception:
                        pass

                emotion = emotion_cache[face_id]["emotion"]

                # LABELS
                cv2.putText(
                    frame,
                    f"ID {face_id}",
                    (x_min, y_min - 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    emotion,
                    (x_min, y_min - 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (255, 255, 0),
                    2
                )

        # ----------------------------------
        # FPS
        # ----------------------------------
        current_time = time.time()

        fps = int(
            1 / max(current_time - prev_time, 0.001)
        )

        prev_time = current_time

        # ----------------------------------
        # NO HUD BACKGROUND
        # ----------------------------------

        cv2.putText(
            frame,
            "SMARTCAM V6",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            3
        )

        cv2.putText(
            frame,
            f"FPS: {fps}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"FACES: {face_count}",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            f"TRACKED: {len(face_memory)}",
            (20, 140),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "AI ONLINE",
            (20, 175),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 90]
        )

        if not ret:
            continue

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            + buffer.tobytes()
            + b'\r\n'
        )

# ----------------------------------
# ROUTES
# ----------------------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# ----------------------------------
# MAIN
# ----------------------------------
if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )