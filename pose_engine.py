import cv2
from mediapipe.tasks.python import vision
from mediapipe.tasks import python


UPPER_COLOR = (0, 255, 255)
LOWER_COLOR = (0, 200, 0)
CENTER_COLOR = (255, 0, 255)


POSE_CONNECTIONS = [

    (11,13),(13,15),
    (12,14),(14,16),

    (11,12),

    (11,23),(12,24),
    (23,24),

    (23,25),(25,27),
    (24,26),(26,28)
]


class PoseEngine:

    def __init__(self, model_path):

        base_options = python.BaseOptions(model_asset_path=model_path)

        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_poses=1,
            result_callback=self._callback
        )

        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.latest_result = None

    def _callback(self, result, image, timestamp):

        self.latest_result = result

    def detect_async(self, mp_image, timestamp):

        self.landmarker.detect_async(mp_image, timestamp)

    def draw_skeleton(self, frame):

        if self.latest_result is None:
            return frame

        if not self.latest_result.pose_landmarks:
            return frame

        height, width, _ = frame.shape
        landmarks = self.latest_result.pose_landmarks[0]

        points = []

        for lm in landmarks:

            x = int(lm.x * width)
            y = int(lm.y * height)

            points.append((x,y))

        for start,end in POSE_CONNECTIONS:

            p1 = points[start]
            p2 = points[end]

            color = LOWER_COLOR if start >= 23 else UPPER_COLOR

            cv2.line(frame,p1,p2,color,3)

        for p in points:

            cv2.circle(frame,p,5,(0,255,0),-1)

        return frame