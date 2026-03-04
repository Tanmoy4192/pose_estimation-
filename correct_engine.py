import time
from utils import distance, calculate_angle


class PoseCorrectionEngine:
    def __init__(self):
        self.state = "IDLE"
        self.hold_start = None
        self.rest_start = None
        self.reps = 0
        self.reference_shoulder_width = None

    def evaluate_pose(self, lm, width, height):
        if not lm:
            return "No Pose"

        # -------- LANDMARKS --------
        left_shoulder = (lm[11].x * width, lm[11].y * height)
        right_shoulder = (lm[12].x * width, lm[12].y * height)

        left_elbow = (lm[13].x * width, lm[13].y * height)
        right_elbow = (lm[14].x * width, lm[14].y * height)

        left_wrist = (lm[15].x * width, lm[15].y * height)
        right_wrist = (lm[16].x * width, lm[16].y * height)

        left_ear = (lm[7].x * width, lm[7].y * height)
        right_ear = (lm[8].x * width, lm[8].y * height)

        left_hip = (lm[23].x * width, lm[23].y * height)
        right_hip = (lm[24].x * width, lm[24].y * height)

        left_ankle = (lm[27].x * width, lm[27].y * height)
        right_ankle = (lm[28].x * width, lm[28].y * height)

        # -------- BODY SCALE --------
        shoulder_width = distance(left_shoulder, right_shoulder)
        if self.reference_shoulder_width is None:
            self.reference_shoulder_width = shoulder_width

        # -------- FEET CHECK --------
        feet_distance = distance(left_ankle, right_ankle)
        ratio = feet_distance / self.reference_shoulder_width
        #print("Feet ratio:", round(ratio, 2))
        feet_ok = 0.40 <= ratio <= 0.55

        # -------- REST POSE CHECK --------
        left_down = left_wrist[1] > left_hip[1]
        right_down = right_wrist[1] > right_hip[1]
        rest_pose = left_down and right_down

        current_time = time.time()

        # HOLDING STATE
        if self.state == "HOLDING":
            hold_time = current_time - self.hold_start
            if hold_time >= 12:
                self.state = "RESTING"
                self.rest_start = None
                return f"Lower arms for rest | Reps: {self.reps}"
            return f"Holding {round(hold_time,1)} sec | Reps: {self.reps}"
        # RESTING STATE
        if self.state == "RESTING":
            if rest_pose:
                if self.rest_start is None:
                    self.rest_start = current_time
                rest_time = current_time - self.rest_start

                if rest_time >= 6:
                    self.reps += 1
                    self.state = "IDLE"
                    self.rest_start = None
                    return f"Rep Completed: {self.reps}"
                return f"Rest {round(rest_time,1)} sec | Reps: {self.reps}"
            else:
                return "Lower arms to thighs"

        # IDLE STATE
        if not feet_ok:
            return "Adjust feet spacing"
        
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        arms_straight = left_angle > 165 and right_angle > 165
        if not arms_straight:
            return "Straighten arms"

        arms_up = (
            left_wrist[1] < left_shoulder[1] and
            right_wrist[1] < right_shoulder[1]
        )

        if not arms_up:
            return "Raise arms up"

        left_ear_dist = abs(left_wrist[0] - left_ear[0])
        right_ear_dist = abs(right_wrist[0] - right_ear[0])

        arms_near_ears = (
            left_ear_dist < self.reference_shoulder_width * 0.3 and
            right_ear_dist < self.reference_shoulder_width * 0.3
        )

        if not arms_near_ears:
            return "Keep arms near ears"

        wrist_distance = distance(left_wrist, right_wrist)

        palms_joined = wrist_distance < self.reference_shoulder_width * 0.2

        if not palms_joined:
            return "Join palms"
        
        # Pose correct -> start hold
        self.state = "HOLDING"
        self.hold_start = current_time

        return f"Correct Pose | Reps: {self.reps}"