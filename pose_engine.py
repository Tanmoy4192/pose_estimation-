import cv2
from mediapipe.tasks.python import vision
from mediapipe.tasks import python


POSE_CONNECTIONS = [

    (11, 13), (13, 15), 
    (12, 14), (14, 16),

    (11, 12),

    (11, 23), (12, 24),
    (23, 24),

    (23, 25), (25, 27),
    (24, 26), (26, 28)

]


class PoseEngine:

    def __init__(self, model_path, visibility_threshold=0.6):

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_poses=1,
            result_callback=self._callback
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.latest_result = None
        self.visibility_threshold = visibility_threshold

    def _callback(self, result, output_image, timestamp_ms):
        self.latest_result = result

    def detect_async(self, mp_image, timestamp_ms):
        self.landmarker.detect_async(mp_image, timestamp_ms)

    def draw_skeleton(self, frame):
        if self.latest_result is None:
            return frame

        if not self.latest_result.pose_landmarks:
            return frame

        height, width, _ = frame.shape
        landmarks = self.latest_result.pose_landmarks[0]
        points = []

        for lm in landmarks:

            if lm.visibility < self.visibility_threshold:
                points.append(None)
                continue

            x = int(lm.x * width)
            y = int(lm.y * height)

            points.append((x, y))
            cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        for start, end in POSE_CONNECTIONS:
            if points[start] and points[end]:
                cv2.line(
                    frame,
                    points[start],
                    points[end],
                    (255, 0, 0),
                    2
                )

        return frame