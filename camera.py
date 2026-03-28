import math, cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1, # Light model for Raspberry Pi usage
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize the camera once
cap = cv2.VideoCapture(0) 

smooth_forearm = None
smooth_hand = None
alpha = 0.2 

def arm_detection(WIDTH, HEIGHT):

    global smooth_forearm, smooth_hand
    
    # Leemos el fotograma
    ret, frame = cap.read()
    if not ret:
        print("Error detecting the camera.")
        #  If there's no detection, we'll move the servos to 90º
        return ["F90H90", None] 
    
    frame_resized = cv2.resize(frame, (WIDTH, HEIGHT))
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    
    resultados = pose.process(frame_rgb)
    
    # If there's no detection, we'll move the servos to 90º
    message = "F90H90" 
    
    if resultados.pose_landmarks:
        alto, ancho, _ = frame_rgb.shape
        lm = resultados.pose_landmarks.landmark

        try:
            elbow = lm[mp_pose.PoseLandmark.RIGHT_ELBOW]
            wrist = lm[mp_pose.PoseLandmark.RIGHT_WRIST]
            finger = lm[mp_pose.PoseLandmark.RIGHT_INDEX]

            # Convert the AI normalized coordinates to pixels
            cx_e, cy_e = int(elbow.x * ancho), int(elbow.y * alto)
            cx_w, cy_w = int(wrist.x * ancho), int(wrist.y * alto)
            cx_f, cy_f = int(finger.x * ancho), int(finger.y * alto)

            if elbow.visibility > 0.5 and wrist.visibility > 0.5:
                # Visualization on the detections
                cv2.line(frame_rgb, (cx_e, cy_e), (cx_w, cy_w), (255, 0, 0), 3) 
                cv2.line(frame_rgb, (cx_w, cy_w), (cx_f, cy_f), (255, 0, 0), 3) 
                cv2.circle(frame_rgb, (cx_e, cy_e), 5, (0, 255, 0), cv2.FILLED) 
                cv2.circle(frame_rgb, (cx_w, cy_w), 5, (0, 255, 0), cv2.FILLED) 
                cv2.circle(frame_rgb, (cx_f, cy_f), 5, (0, 255, 0), cv2.FILLED) 
                
                forearm_inclination = math.degrees(math.atan2(cy_e - cy_w, cx_w - cx_e))
                hand_inclination = math.degrees(math.atan2(cy_w - cy_f, cx_f - cx_w))
                hand_offset = -30
                
                # Defines the hand angle's sensitivity
                hand_multiplier = 1.0
                adjusted_hand_inclination = (hand_inclination * hand_multiplier) + hand_offset

                # We invert the adjusted reading 90º to match the arm movement
                objective_forearm = forearm_inclination + 90.0
                objective_hand = adjusted_hand_inclination + 90.0
                
                # Smooth the lecture so the robot movement isn't erratic
                if smooth_forearm is None:
                    smooth_forearm = objective_forearm
                    smooth_hand = objective_hand
                else:
                    smooth_forearm = (alpha * objective_forearm) + ((1.0 - alpha) * smooth_forearm)
                    smooth_hand = (alpha * objective_hand) + ((1.0 - alpha) * smooth_hand)

                forearm_servo = int(smooth_forearm)
                hand_servo = int(smooth_hand)
            
                # Limit the servos' movement
                forearm_servo = max(0, min(180, forearm_servo))
                hand_servo = max(0, min(180, hand_servo))

                # Actualizamos el mensaje solo si hemos detectado el brazo bien
                message = f"F{forearm_servo}H{hand_servo}"

        except Exception as e:
            print(f"Calculus error: {e}")
            
    # Always returns a message
    return [message, frame_rgb]