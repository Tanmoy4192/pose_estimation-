import numpy as np

# joints that actually matter for this exercise
KEYPOINTS = [
    11, 12,   # shoulders
    13, 14,   # elbows
    15, 16    # wrists
]


def normalize_landmarks(landmarks):
    pts = []

    for idx in KEYPOINTS:
        lm = landmarks[idx]
        pts.append([lm.x, lm.y])

    pts = np.array(pts)

    # center at shoulder midpoint
    center = (pts[0] + pts[1]) / 2
    pts = pts - center

    # scale by shoulder width
    shoulder_width = np.linalg.norm(pts[1] - pts[0])

    if shoulder_width == 0:
        shoulder_width = 1

    pts = pts / shoulder_width
    return pts.flatten()


def pose_similarity(user_lm, ref_lm):
    u = normalize_landmarks(user_lm)
    r = normalize_landmarks(ref_lm)

    dot = np.dot(u, r)
    mag = np.linalg.norm(u) * np.linalg.norm(r)

    if mag == 0:
        return 0
    similarity = dot / mag
    return similarity