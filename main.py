import cv2
import mediapipe as mp
import pyautogui
import math


def hands_mouse_control():

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("It cant")
        return

 
    screen_width, screen_height = pyautogui.size()

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    drawing = mp.solutions.drawing_utils

  
    pinch_threshold = 0.05
    clicking = False

    while True:
        success, frame = cam.read()
        if not success:
            continue

     
        frame = cv2.flip(frame, 1)

    
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
            
                drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

              
                index_finger = hand_landmarks.landmark[8]

             
                screen_x = screen_width * index_finger.x
                screen_y = screen_height * index_finger.y
                pyautogui.moveTo(screen_x, screen_y)

                thumb = hand_landmarks.landmark[4]
                dx = thumb.x - index_finger.x
                dy = thumb.y - index_finger.y
                distance = math.hypot(dx, dy)

                if distance < pinch_threshold and not clicking:
                    pyautogui.click()
                    clicking = True
                elif distance >= pinch_threshold and clicking:
                    clicking = False

        cv2.imshow("heeey", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    hands_mouse_control()
