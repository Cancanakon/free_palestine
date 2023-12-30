import time
from flask import Flask, render_template, jsonify
import cv2
import mediapipe as mp
import math
import threading
from multiprocessing import Value

class DetectUser:

    def __init__(self):
        self.circle_center = (320, 240)
        self.circle_radius = 100
        self.cap = cv2.VideoCapture(0)
        self.inside_circle = Value('i', 0)
       #self.hand_status = Value('i', 0)
        self.lock = threading.Lock()
        self.is_running = threading.Event()
    def is_point_inside_circle(self, point):
        distance = math.sqrt((point[0] - self.circle_center[0]) ** 2 + (point[1] - self.circle_center[1]) ** 2)
        return distance <= self.circle_radius

    def detect_hand(self,f_hand_status):
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(max_num_hands=1)

        while not self.is_running.is_set():
            ret, frame = self.cap.read()
            cv2.circle(frame, self.circle_center, self.circle_radius, (0, 255, 0), 2)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                h, w, _ = frame.shape
                hand_landmark_top = results.multi_hand_landmarks[0].landmark[9]
                hand_landmark_bot = results.multi_hand_landmarks[0].landmark[0]
                hand_x_top, hand_y_top = int(hand_landmark_top.x * w), int(hand_landmark_top.y * h)
                hand_x_bot, hand_y_bot = int(hand_landmark_bot.x * w), int(hand_landmark_bot.y * h)
                cv2.circle(frame, ((hand_x_top + hand_x_bot) // 2, (hand_y_top + hand_y_bot) // 2), 10, (255, 0, 0), -1)
                inside_circle = self.is_point_inside_circle(((hand_x_top + hand_x_bot) // 2, (hand_y_top + hand_y_bot) // 2))

                if self.inside_circle.value != inside_circle:
                    print("/////", inside_circle)
                    with self.lock:
                        self.inside_circle.value = inside_circle

                with self.lock:
                    #self.hand_status.value = 1
                    return 1

            else:
                with self.lock:
                    #self.hand_status.value = 0
                    return 0
            #print("Hand_detect FUNC: ", self.hand_status.value)
            cv2.imshow("GencTDV", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        with self.lock:
            self.cap.release()
            cv2.destroyAllWindows()

    def start_detection_thread(self):
        self.is_running.clear()
        detection_thread = threading.Thread(target=self.detect_hand)
        detection_thread.start()

    def stop_detection_thread(self):
        self.is_running.set()
        detection_thread.join()