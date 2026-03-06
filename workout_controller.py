from pose_similarity import pose_similarity
from utils import calculate_angle


class WorkoutController:

    def __init__(self):

        self.rep_count = 0

        self.threshold = 0.93   # stricter similarity

        self.phase = "DOWN"

    def evaluate(self, user_lm, ref_lm, width, height):

        if user_lm is None or ref_lm is None:
            return False, "Detecting pose..."

        similarity = pose_similarity(user_lm, ref_lm)

        if similarity < self.threshold:

            correction = self.detect_correction(user_lm, width, height)

            return False, correction

        self.detect_rep(user_lm, width, height)

        return True, "Good form"

    def detect_correction(self, lm, width, height):

        left_shoulder = (lm[11].x * width, lm[11].y * height)
        right_shoulder = (lm[12].x * width, lm[12].y * height)

        left_elbow = (lm[13].x * width, lm[13].y * height)
        right_elbow = (lm[14].x * width, lm[14].y * height)

        left_wrist = (lm[15].x * width, lm[15].y * height)
        right_wrist = (lm[16].x * width, lm[16].y * height)

        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        if left_angle < 160 or right_angle < 160:
            return "Straighten your arms"

        if left_wrist[1] > left_shoulder[1] or right_wrist[1] > right_shoulder[1]:
            return "Raise your arms higher"

        wrist_distance = abs(left_wrist[0] - right_wrist[0])

        if wrist_distance > width * 0.15:
            return "Join your palms"

        return "Adjust posture"

    def detect_rep(self, lm, width, height):

        left_wrist_y = lm[15].y * height
        left_shoulder_y = lm[11].y * height

        arms_up = left_wrist_y < left_shoulder_y

        if arms_up and self.phase == "DOWN":

            self.phase = "UP"

        if not arms_up and self.phase == "UP":

            self.phase = "DOWN"
            self.rep_count += 1