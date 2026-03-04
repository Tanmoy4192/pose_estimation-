import cv2
import time
import mediapipe as mp

from pose_engine import PoseEngine
from correct_engine import PoseCorrectionEngine


class Camera:
    def __init__(self, index=1):
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            raise Exception("Camera could not be opened")

    def read(self):
        ret, frame = self.cap.read()

        if not ret:
            raise Exception("Frame capture failed")

        return frame

    def release(self):
        self.cap.release()


def main():
    #create objects
    camera = Camera(1)
    pose_detector = PoseEngine("pose_landmarker_heavy.task")
    pose_corrector = PoseCorrectionEngine()

    prev_time = time.time()

    while True:

        frame = camera.read()
        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #convert into mp image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        timestamp = int(time.time() * 1000) #for live streame
        pose_detector.detect_async(mp_image, timestamp)
        frame = pose_detector.draw_skeleton(frame)#draw skeleton of the person
        message = "No pose detected"

        if pose_detector.latest_result and pose_detector.latest_result.pose_landmarks:

            landmarks = pose_detector.latest_result.pose_landmarks[0]

            # print coordinates 
            for i, lm in enumerate(landmarks):
                print(f"Landmark {i}: ({lm.x:.3f}, {lm.y:.3f})")

            message = pose_corrector.evaluate_pose(
                landmarks,
                width,
                height
            )

        color = (0, 255, 0) if message == "Correct Pose" else (0, 0, 255)

        cv2.putText(
            frame,message,
            (40, 70),cv2.FONT_HERSHEY_SIMPLEX,
            1,color,2
        )

        cv2.putText(
            frame,
            f"Reps: {pose_corrector.reps}",
            (40,120),cv2.FONT_HERSHEY_SIMPLEX,
            1,(255,255,0),2
        )

        current_time = time.time()
        dt = current_time - prev_time
        fps = 1 / dt if dt > 0 else 0
        prev_time = current_time
        #show fps
        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()