import cv2
import mediapipe as mp
import math
import numpy as np
from collections import deque

from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

from ctypes import cast, POINTER


# -----------------------------
# Windows Volume Connection
# -----------------------------

devices = AudioUtilities.GetSpeakers()

interface = devices.EndpointVolume
7
volume = cast(
    interface,
    POINTER(IAudioEndpointVolume)
)


# -----------------------------
# MediaPipe Hands
# -----------------------------

mp_hands = mp.solutions.hands

mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1
)


# -----------------------------
# Camera
# -----------------------------

cap = cv2.VideoCapture(0)


# -----------------------------
# Fixed Calibration
# -----------------------------

min_distance = 20
max_distance = 220


# -----------------------------
# Smoothing
# -----------------------------

distance_history = deque(maxlen=5)

volume_history = deque(maxlen=5)


# -----------------------------
# Volume Safety System
# -----------------------------

previous_volume = 0


while True:

    success, img = cap.read()

    # Camera error check
    if not success:

        print("Camera Frame Error")

        continue

    # Mirror effect
    img = cv2.flip(img, 1)

    # BGR -> RGB
    rgb_img = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2RGB
    )

    # Hand tracking
    results = hands.process(rgb_img)

    # Image size
    h, w, c = img.shape

    # Finger coordinates
    thumb_x, thumb_y = 0, 0
    index_x, index_y = 0, 0

    # Hand detected
    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            # Draw hand skeleton
            mp_draw.draw_landmarks(
                img,
                handLms,
                mp_hands.HAND_CONNECTIONS
            )

            # Landmark loop
            for id, lm in enumerate(handLms.landmark):

                # Normalize -> Pixel
                cx = int(lm.x * w)
                cy = int(lm.y * h)

                # Thumb tip
                if id == 4:

                    thumb_x, thumb_y = cx, cy

                    cv2.circle(
                        img,
                        (thumb_x, thumb_y),
                        15,
                        (0,255,0),
                        -1
                    )

                # Index tip
                if id == 8:

                    index_x, index_y = cx, cy

                    cv2.circle(
                        img,
                        (index_x, index_y),
                        15,
                        (255,0,255),
                        -1
                    )

            # Distance calculation
            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )

            # Distance smoothing
            distance_history.append(distance)

            smooth_distance = np.mean(
                distance_history
            )

            # Distance -> Percentage
            volume_percent = np.interp(
                smooth_distance,
                [min_distance, max_distance],
                [0,100]
            )

            # Clipping
            volume_percent = np.clip(
                volume_percent,
                0,
                100
            )

            # Percentage smoothing
            volume_history.append(
                volume_percent
            )

            smooth_volume = np.mean(
                volume_history
            )

            # Percentage -> Scalar
            volume_scalar = smooth_volume / 100

            # Debug print
            print(
                f"Distance: {int(smooth_distance)} | "
                f"Volume: {int(smooth_volume)}% | "
                f"Scalar: {round(volume_scalar, 2)}"
            )

            # Volume threshold check
            if abs(volume_scalar - previous_volume) > 0.02:

                try:

                    volume.SetMasterVolumeLevelScalar(
                        volume_scalar,
                        None
                    )

                    previous_volume = volume_scalar

                except Exception as e:

                    print("Volume Error:", e)

            # Bar mapping
            bar_y = np.interp(
                smooth_volume,
                [0,100],
                [400,150]
            )

            # Gesture states
            if smooth_volume < 30:

                volume_status = "LOW"

                line_color = (0,0,255)

            elif smooth_volume < 70:

                volume_status = "MEDIUM"

                line_color = (0,255,255)

            else:

                volume_status = "HIGH"

                line_color = (0,255,0)

            # Finger line
            cv2.line(
                img,
                (thumb_x, thumb_y),
                (index_x, index_y),
                line_color,
                5
            )

            # Volume bar outline
            cv2.rectangle(
                img,
                (50,150),
                (85,400),
                (255,255,255),
                3
            )

            # Dynamic volume bar
            cv2.rectangle(
                img,
                (50, int(bar_y)),
                (85,400),
                line_color,
                -1
            )

            # Percentage text
            cv2.putText(
                img,
                f'{int(smooth_volume)} %',
                (30, 430),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                3
            )

            # Status text
            cv2.putText(
                img,
                volume_status,
                (15, 470),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                line_color,
                3
            )

    # No hand detected
    else:

        cv2.putText(
            img,
            "NO HAND DETECTED",
            (120, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255),
            3
        )

    cv2.imshow(
        "Real Gesture Volume Control",
        img
    )

    # Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()

cv2.destroyAllWindows()