import cv2


def draw_alert(frame, text):

    overlay = frame.copy()

    h, w, _ = frame.shape

    cv2.rectangle(
        overlay,
        (30, h - 120),
        (w - 30, h - 40),
        (0, 0, 0),
        -1
    )

    cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

    cv2.putText(
        frame,
        text,
        (60, h - 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )


def draw_rep_counter(frame, reps):

    cv2.putText(
        frame,
        f"Reps: {reps}",
        (40, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 255),
        3
    )


def draw_start_overlay(frame, seconds):

    overlay = frame.copy()

    h, w, _ = frame.shape

    cv2.rectangle(
        overlay,
        (0, 0),
        (w, h),
        (0, 0, 0),
        -1
    )

    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    cv2.putText(
        frame,
        "Let's Begin",
        (w // 2 - 150, h // 2 - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (255, 255, 255),
        4
    )

    cv2.putText(
        frame,
        str(seconds),
        (w // 2 - 20, h // 2 + 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 255),
        4
    )