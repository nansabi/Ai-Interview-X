# camera_analysis.py
import cv2
from deepface import DeepFace
import threading
import time
import traceback

# -------------------------
# Global variables for live feedback
# -------------------------
live_camera_score = 0        # Score 0-10
live_camera_feedback = ""    # Text feedback
camera_running = False       # Flag to control camera thread
latest_frame = None          # Latest frame for UI preview
_lock = threading.Lock()     # Thread-safe lock for shared variables


# -------------------------
# Internal camera loop
# -------------------------
def _camera_loop():
    """Runs in background thread and updates live feedback"""
    global live_camera_score, live_camera_feedback, camera_running, latest_frame

    # ✅ FIX: Force DirectShow backend (Windows stable)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Optional but safe stability settings (NO logic change)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        with _lock:
            live_camera_score = 0
            live_camera_feedback = "Cannot access camera"
        camera_running = False
        print("[Camera] ERROR: Cannot access camera")
        return

    camera_running = True
    print("[Camera] Camera started successfully")

    frame_fail_count = 0  # prevent console spam

    while camera_running:
        try:
            ret, frame = cap.read()

            if not ret:
                frame_fail_count += 1
                if frame_fail_count % 30 == 0:
                    print("[Camera] WARNING: Frame not received")
                time.sleep(0.05)
                continue

            frame_fail_count = 0
            frame = cv2.flip(frame, 1)  # Mirror effect

            # -------------------------
            # Emotion detection
            # -------------------------
            score = 0
            feedback = "No face detected. Please sit in front of the camera."
            dominant_emotion = "neutral"

            try:
                analysis = DeepFace.analyze(
                    frame,
                    actions=['emotion'],
                    enforce_detection=False
                )

                # Handle list vs dict from DeepFace
                if isinstance(analysis, list):
                    analysis = analysis[0]

                dominant_emotion = analysis.get("dominant_emotion", "neutral")
                print(f"[Camera] Detected emotion: {dominant_emotion}")

                # -------------------------
                # Realistic scoring & feedback (UNCHANGED)
                # -------------------------
                if dominant_emotion == "happy":
                    score = 10
                    feedback = "You look confident and engaged!"
                elif dominant_emotion == "neutral":
                    score = 6
                    feedback = "You look calm. Try to smile more for confidence."
                elif dominant_emotion == "surprise":
                    score = 8
                    feedback = "You seem alert and attentive!"
                elif dominant_emotion in ["sad", "angry", "fear", "disgust"]:
                    score = 3
                    feedback = f"Your emotion seems {dominant_emotion}. Try to smile more."
                else:
                    score = 5
                    feedback = "Keep your focus and confidence high."

            except Exception as e:
                dominant_emotion = "neutral"
                score = 0
                feedback = "Face not detected or unclear."
                print("[Camera] DeepFace analysis error:", e)
                traceback.print_exc()

            # -------------------------
            # Update shared variables thread-safely
            # -------------------------
            with _lock:
                live_camera_score = min(score, 10)
                live_camera_feedback = feedback
                latest_frame = frame.copy()

        except Exception as e:
            print("[Camera] Camera loop error:", e)
            traceback.print_exc()

        # Reduce CPU usage
        time.sleep(0.03)

    # -------------------------
    # Cleanup
    # -------------------------
    cap.release()
    camera_running = False
    print("[Camera] Camera stopped")


# -------------------------
# Public functions
# -------------------------
def start_camera():
    """Start camera thread"""
    global camera_running
    if not camera_running:
        threading.Thread(target=_camera_loop, daemon=True).start()
        print("[Camera] Starting camera thread...")


def stop_camera():
    """Stop camera thread"""
    global camera_running
    camera_running = False
    print("[Camera] Stopping camera thread...")


def get_live_camera_feedback():
    """Return latest live feedback and score"""
    with _lock:
        return {
            "score": live_camera_score,
            "feedback": live_camera_feedback
        }


def get_camera_frame():
    """Return latest camera frame for UI preview"""
    with _lock:
        if latest_frame is not None:
            return latest_frame.copy()
        return None
