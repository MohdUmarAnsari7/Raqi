import numpy as np
import cv2
import threading
from functions import *

label_text = ""
speaking_flag = False

speak("I cannot allow any unauthorized access.")
speak("Authentication is about to begin, Please look directly at the camera")

# isAuth = AuthenticateFace()
isAuth = 1

if isAuth == 1:
    speak("Authentication successfull, Access granted")  
    def show_rotating_sphere():
        global label_text

        num_points = 1300
        phi = np.arccos(2 * np.random.random(num_points) - 1)
        theta = np.random.uniform(0, 2 * np.pi, num_points)
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)

        frame_size = 1000
        scale = frame_size // 4
        center = frame_size // 2
        rotation_speed = 2
        perspective_factor = 300
        label_font = cv2.FONT_HERSHEY_SIMPLEX
        label_scale = 1
        label_color = (255, 255, 255)
        label_thickness = 1
        label_position = (center - 180, frame_size - 50)

        cv2.namedWindow('RAQI', cv2.WINDOW_NORMAL)
        frame_count = 0

        while True:
            frame = np.zeros((frame_size, frame_size, 3), dtype=np.uint8)
            angle = np.radians(frame_count * rotation_speed)
            cos_angle, sin_angle = np.cos(angle), np.sin(angle)
            x_rot = cos_angle * x - sin_angle * z
            z_rot = sin_angle * x + cos_angle * z

            for i in range(num_points):
                depth_scale = perspective_factor / (perspective_factor + z_rot[i])
                px = int(center + scale * x_rot[i] * depth_scale)
                py = int(center - scale * y[i] * depth_scale)
                color = (0, 255, 255)
                cv2.circle(frame, (px, py), 2, color, -1)

            cv2.putText(frame, label_text, label_position, label_font, label_scale, label_color, label_thickness, cv2.LINE_AA)
            cv2.imshow('RAQI', frame)

            if cv2.waitKey(30) & 0xFF == 27:
                break

            frame_count += 1

        cv2.destroyAllWindows()

    sphere_thread = threading.Thread(target=show_rotating_sphere)
    sphere_thread.daemon = True
    sphere_thread.start()

    wishMe()
    while True:
        label_text = "Listening for command..."
        command = takeCommand().lower()
        label_text = "USER : "+command

        if command.startswith("start"):
            openApp(command)

        elif 'close' in command:
            closeApplication(command)

        elif 'youtube' in command:
            searchYoutube()

        elif 'google' in command:
            searchGoogle()

        elif 'where is' in command or 'find' in command or 'locate' in command:
            locate(command)

        elif 'switch to' in command:
            switchToApp(command)

        elif 'our location' in command or 'my location' in command:
            myLocation()

        elif 'copy' in command:
            copy()

        elif 'copy all' in command:
            copyAll()

        elif 'paste' in command:
            paste()

        elif 'new tab' in command:
            newTab()

        elif 'this tab' in command:
            closeTab()

        elif 'run' in command or 'enter' in command or 'search' in command:
            pg.hotkey('enter')

        elif 'save' in command:
            save()

        elif 'write' in command or 'right' in command:
            write()

        elif 'what' in command or 'who' in command or 'when' in command or 'where' in command or 'tell me about' in command:
            database(command)

        elif 'quit' in command or 'bye' in command or 'shut up' in command or 'see you' in command or 'soon' in command:
            label_text = "Shutting down..."
            speak('Yes sir, you can call me anytime')
            break

        else:
            response = chatBot(command)
            label_text = response.text
            speak(response)

else:
    speak("Authentication failed. could not recognize you, access denied")