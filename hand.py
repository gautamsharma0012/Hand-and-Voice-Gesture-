# hand.py
import cv2
import mediapipe as mp
import pyautogui
import time

class HandController:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.click_cooldown = 1.0
        self.last_click_time = time.time()
        self.cursor_enabled = True

    def count_fingers(self, landmarks):
        fingers = []
        tips_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

        # Thumb
        if landmarks[tips_ids[0]].x < landmarks[tips_ids[0] - 1].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for id in range(1, 5):
            if landmarks[tips_ids[id]].y < landmarks[tips_ids[id] - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return sum(fingers)

    def process_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            landmarks = hand_landmarks.landmark

            # Count fingers
            finger_count = self.count_fingers(landmarks)

            # Index fingertip position
            index_finger = landmarks[8]
            x = int(index_finger.x * self.screen_width)
            y = int(index_finger.y * self.screen_height)

            now = time.time()

            # Left Click with 1 finger
            if finger_count == 1 and (now - self.last_click_time > self.click_cooldown):
                pyautogui.click(button='left')
                self.last_click_time = now
                print("👆 Left Click")

            # Right Click with 2 fingers
            elif finger_count == 2 and (now - self.last_click_time > self.click_cooldown):
                pyautogui.click(button='right')
                self.last_click_time = now
                print("✌️ Right Click")

            # Stop cursor on closed fist
            elif finger_count == 0:
                self.cursor_enabled = False
                print("✊ Hand closed - cursor frozen")

            # Move cursor with open hand (3 or more fingers)
            elif finger_count >= 3:
                self.cursor_enabled = True
                smooth_x = self.prev_x + (x - self.prev_x) // 5
                smooth_y = self.prev_y + (y - self.prev_y) // 5
                pyautogui.moveTo(smooth_x, smooth_y)
                self.prev_x, self.prev_y = smooth_x, smooth_y
                print("🖐️ Moving cursor")

        return frame

    def release(self):
        self.cap.release()
