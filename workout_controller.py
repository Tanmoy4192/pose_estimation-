from pose_similarity import pose_similarity
from utils import calculate_angle
import math

class WorkoutController:
    def __init__(self):
        self.rep_count = 0
        self.phase = "DOWN"

        self.similarity_threshold = 0.84

        self.error_frames = 0
        self.good_frames = 0

        self.error_threshold = 4
        self.good_threshold = 4

    def evaluate(self, user_lm, ref_lm, width, height):
        if user_lm is None or ref_lm is None:
            return False, "Detecting pose..."
        message = None

        # 1. FEET RULE 

        feet_issue = self.check_feet(user_lm, width, height)

        if feet_issue:
            message = feet_issue

        # 2. PHASE DETECTION 

        if message is None:
            if self.is_hold_phase(ref_lm, width, height):
                correction = self.check_hold_pose(user_lm, width, height)
                if correction:
                    message = correction
            elif self.is_rest_phase(ref_lm, width, height):
                correction = self.check_rest_pose(user_lm, width, height)
                if correction:
                    message = correction

        # 3. FOLLOW MENTOR (SIMILARITY CHECK)

        if message is None:
            similarity = pose_similarity(user_lm, ref_lm)
            if similarity < self.similarity_threshold:
                message = "Follow the mentor pose"

        # 4. TEMPORAL STABILITY
        if message:
            self.error_frames += 1
            self.good_frames = 0

            if self.error_frames >= self.error_threshold:
                return False, message
            return True, "Good form"
        else:
            self.good_frames += 1
            self.error_frames = 0

            if self.good_frames >= self.good_threshold:

                self.detect_rep(user_lm, width, height)
                return True, "Good form"
            return False, "Hold steady"

    # FEET RULE

    def check_feet(self, lm, width, height):

        left_ankle = (lm[27].x * width, lm[27].y * height)
        right_ankle = (lm[28].x * width, lm[28].y * height)

        left_shoulder = (lm[11].x * width, lm[11].y * height)
        right_shoulder = (lm[12].x * width, lm[12].y * height)

        feet_distance = math.dist(left_ankle, right_ankle)
        shoulder_width = math.dist(left_shoulder, right_shoulder)

        if shoulder_width == 0:
            shoulder_width = 1

        ratio = feet_distance / shoulder_width

        if ratio < 0.20:
            return "Move feet slightly apart"

        if ratio > 0.60:
            return "Feet too wide"
        return None

    # HOLD PHASE DETECTION

    def is_hold_phase(self, ref_lm, width, height):

        left_shoulder = (ref_lm[11].x * width, ref_lm[11].y * height)
        right_shoulder = (ref_lm[12].x * width, ref_lm[12].y * height)

        left_elbow = (ref_lm[13].x * width, ref_lm[13].y * height)
        right_elbow = (ref_lm[14].x * width, ref_lm[14].y * height)

        left_wrist = (ref_lm[15].x * width, ref_lm[15].y * height)
        right_wrist = (ref_lm[16].x * width, ref_lm[16].y * height)

        left_ear = (ref_lm[7].x * width, ref_lm[7].y * height)
        right_ear = (ref_lm[8].x * width, ref_lm[8].y * height)

        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        arms_straight = left_angle > 165 and right_angle > 165
        wrists_above = (
            left_wrist[1] < left_shoulder[1] and
            right_wrist[1] < right_shoulder[1]
        )
        near_ears = (
            abs(left_wrist[0] - left_ear[0]) < width * 0.10 and
            abs(right_wrist[0] - right_ear[0]) < width * 0.10
        )
        return arms_straight and wrists_above and near_ears


    # REST PHASE    

    def is_rest_phase(self, ref_lm, width, height):
        wrist_y = ref_lm[15].y * height
        hip_y = ref_lm[23].y * height
        return wrist_y > hip_y - 40

    # STRICT HOLD RULES

    def check_hold_pose(self, lm, width, height):
        left_shoulder = (lm[11].x * width, lm[11].y * height)
        right_shoulder = (lm[12].x * width, lm[12].y * height)

        left_elbow = (lm[13].x * width, lm[13].y * height)
        right_elbow = (lm[14].x * width, lm[14].y * height)

        left_wrist = (lm[15].x * width, lm[15].y * height)
        right_wrist = (lm[16].x * width, lm[16].y * height)

        left_hip = (lm[23].x * width, lm[23].y * height)
        right_hip = (lm[24].x * width, lm[24].y * height)

        left_ear = (lm[7].x * width, lm[7].y * height)
        right_ear = (lm[8].x * width, lm[8].y * height)

        # ARM STRAIGHT
        left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
        right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

        if left_angle < 175 or right_angle < 175:
            return "Straighten your arms fully"

        # ARMS VERTICAL
        left_vertical = calculate_angle(left_hip, left_shoulder, left_wrist)
        right_vertical = calculate_angle(right_hip, right_shoulder, right_wrist)

        if left_vertical < 150 or right_vertical < 150:
            return "Raise arms straight above head"

        # PALMS JOINED
        wrist_dist = math.dist(left_wrist, right_wrist)

        if wrist_dist > width * 0.02:
            return "Join your palms"

        # ELBOWS CLOSE
        elbow_dist = math.dist(left_elbow, right_elbow)

        if elbow_dist > width * 0.16:
            return "Bring elbows closer"

        # CENTERED ABOVE HEAD
        shoulder_mid = (left_shoulder[0] + right_shoulder[0]) / 2
        wrist_mid = (left_wrist[0] + right_wrist[0]) / 2

        if abs(wrist_mid - shoulder_mid) > width * 0.07:
            return "Keep palms centered above head"

        # HANDS NEAR EARS
        ear_gap_left = abs(left_wrist[0] - left_ear[0])
        ear_gap_right = abs(right_wrist[0] - right_ear[0])

        if ear_gap_left > width * 0.045 or ear_gap_right > width * 0.045:
            return "Keep arms close to ears"
        return None

    # REST RULE

    def check_rest_pose(self, lm, width, height):
        wrist_y = lm[15].y * height
        hip_y = lm[23].y * height

        if wrist_y < hip_y - 40:
            return "Rest arms near thighs"
        return None

    # REP COUNT

    def detect_rep(self, lm, width, height):
        left_wrist_y = lm[15].y * height
        left_shoulder_y = lm[11].y * height

        arms_up = left_wrist_y < left_shoulder_y

        if arms_up and self.phase == "DOWN":
            self.phase = "UP"

        if not arms_up and self.phase == "UP":
            self.phase = "DOWN"
            self.rep_count += 1