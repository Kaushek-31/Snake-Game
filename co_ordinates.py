import cv2
import mediapipe as mp
import csv
import time

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# For webcam input:
    
holistic = mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4)
cap = cv2.VideoCapture(0)

#initializing time
time.sleep(3)
initial_time = time.time()

path = '/home/kaushek/activity_detection/test_output/output.csv'

with open(path, 'a+', newline="") as f:
    myFields = ['TIME', 'L_WRIST', 'L_THUMB_CMC', 'L_THUMB_MCP', 'L_THUMB_IP', 'L_THUMB_TIP', 'L_INDEX_FINGER_MCP', 'L_INDEX_FINGER_PIP',
              'L_INDEX_FINGER_DIP', 'L_INDEX_FINGER_TIP', 'L_MIDDLE_FINGER_MCP', 'L_MIDDLE_FINGER_PIP', 'L_MIDDLE_FINGER_DIP',
              'L_MIDDLE_FINGER_TIP', 'L_RING_FINGER_MCP', 'L_RING_FINGER_PIP', 'L_RING_FINGER_DIP', 'L_RING_FINGER_TIP', 'L_PINKY_MCP',
              'L_PINKY_PIP', 'L_PINKY_DIP', 'L_PINKY_TIP', 'R_WRIST', 'R_THUMB_CMC', 'R_THUMB_MCP', 'R_THUMB_IP', 'R_THUMB_TIP',
              'R_INDEX_FINGER_MCP', 'R_INDEX_FINGER_PIP', 'R_INDEX_FINGER_DIP', 'R_INDEX_FINGER_TIP', 'R_MIDDLE_FINGER_MCP', 
              'R_MIDDLE_FINGER_PIP', 'R_MIDDLE_FINGER_DIP', 'R_MIDDLE_FINGER_TIP', 'R_RING_FINGER_MCP', 'R_RING_FINGER_PIP', 
              'R_RING_FINGER_DIP', 'R_RING_FINGER_TIP', 'R_PINKY_MCP', 'R_PINKY_PIP', 'R_PINKY_DIP', 'R_PINKY_TIP','NOSE',
              'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR',
              'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 
              'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 
              'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE','RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']
    writer = csv.DictWriter(f, fieldnames=myFields)    
    writer.writeheader()

while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Empty frame. Proceeding further...")
    # If loading a video, use 'break' instead of 'continue'.
    continue

  # Flip the image horizontally for a later selfie-view display, and convert
  # the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  image_height, image_width, _ = image.shape
  #print(image_height, image_width)
  # To improve performance, optionally mark the image as not writeable to
  # pass by reference.
  image.flags.writeable = False
  results = holistic.process(image)

  # We can extract whatever co-ordinates we want to with the following command.
  #if results.pose_landmarks:
  #  print(f'Mouth coordinates: ('
  #        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].x * image_width}, '
  #        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_LEFT].y * image_height})'
  #        '('
  #        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].x * image_width}, '
  #        f'{results.pose_landmarks.landmark[mp_holistic.PoseLandmark.MOUTH_RIGHT].y * image_height})'
  #        )
  
  #if results.right_hand_landmarks:
  #  print(f'Right wrist coordinates: ('
  #        f'{results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].x * image_width}, '
  #        f'{results.right_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y * image_height})'
  #        )

  #if results.left_hand_landmarks:
  #  print(f'Left wrist coordinates: ('
  #        f'{results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].x * image_width}, '
  #        f'{results.left_hand_landmarks.landmark[mp_holistic.HandLandmark.WRIST].y * image_height})'
  #        )

  # Draw landmark annotation on the image.
  image.flags.writeable = True
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
  
  mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
  mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
  mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
  mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
  
  cv2.imshow('MediaPipe Holistic', image)
  
  
  #having landmarks as a list => contains x,y coordinates of each position of landmark in order as listed in website
  left_hand = []
  for i in range(0, 21, 1):
    if results.left_hand_landmarks:
      a = [results.left_hand_landmarks.landmark[i].x * image_width, results.left_hand_landmarks.landmark[i].y * image_height]
      left_hand.append(a)
    else:
      #left_hand.append(None)
      left_hand.append('n/d')
      
  right_hand = []
  for i in range(0, 21, 1):
    if results.right_hand_landmarks:
      b = [results.right_hand_landmarks.landmark[i].x * image_width, results.right_hand_landmarks.landmark[i].y * image_height]
      right_hand.append(b)
    else:
      #right_hand.append(None)
      right_hand.append('n/d')
    
  pose = []
  for i in range(0, 33, 1):
    if results.pose_landmarks:
      c = [results.pose_landmarks.landmark[i].x * image_width, results.pose_landmarks.landmark[i].y * image_height]
      pose.append(c)
    else:
      #pose.append(None)
      pose.append('n/d')
     
  
  print(left_hand)
  print("******************************************************************************")
  print(right_hand)
  print("******************************************************************************")
  print(pose)
  print("******************************************************************************")
  
  #combining all the coordinates
  total = left_hand + right_hand + pose
  print(total)
  print("******************************************************************************")
  print(len(total))
  print("******************************************************************************")
  
#  myFields = ['TIME', 'L_WRIST', 'L_THUMB_CMC', 'L_THUMB_MCP', 'L_THUMB_IP', 'L_THUMB_TIP', 'L_INDEX_FINGER_MCP', 'L_INDEX_FINGER_PIP',
#              'L_INDEX_FINGER_DIP', 'L_INDEX_FINGER_TIP', 'L_MIDDLE_FINGER_MCP', 'L_MIDDLE_FINGER_PIP', 'L_MIDDLE_FINGER_DIP',
#              'L_MIDDLE_FINGER_TIP', 'L_RING_FINGER_MCP', 'L_RING_FINGER_PIP', 'L_RING_FINGER_DIP', 'L_RING_FINGER_TIP', 'L_PINKY_MCP',
#              'L_PINKY_PIP', 'L_PINKY_DIP', 'L_PINKY_TIP', 'R_WRIST', 'R_THUMB_CMC', 'R_THUMB_MCP', 'R_THUMB_IP', 'R_THUMB_TIP',
#              'R_INDEX_FINGER_MCP', 'R_INDEX_FINGER_PIP', 'R_INDEX_FINGER_DIP', 'R_INDEX_FINGER_TIP', 'R_MIDDLE_FINGER_MCP', 
#              'R_MIDDLE_FINGER_PIP', 'R_MIDDLE_FINGER_DIP', 'R_MIDDLE_FINGER_TIP', 'R_RING_FINGER_MCP', 'R_RING_FINGER_PIP', 
#              'R_RING_FINGER_DIP', 'R_RING_FINGER_TIP', 'R_PINKY_MCP', 'R_PINKY_PIP', 'R_PINKY_DIP', 'R_PINKY_TIP','NOSE',
#              'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR',
#              'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 
#              'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 
#              'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE','RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']

  #writing the final data in a csv file
  current_time = time.time() - initial_time
  with open(path, 'a+', newline="") as f:
    myFields = ['TIME', 'L_WRIST', 'L_THUMB_CMC', 'L_THUMB_MCP', 'L_THUMB_IP', 'L_THUMB_TIP', 'L_INDEX_FINGER_MCP', 'L_INDEX_FINGER_PIP',
              'L_INDEX_FINGER_DIP', 'L_INDEX_FINGER_TIP', 'L_MIDDLE_FINGER_MCP', 'L_MIDDLE_FINGER_PIP', 'L_MIDDLE_FINGER_DIP',
              'L_MIDDLE_FINGER_TIP', 'L_RING_FINGER_MCP', 'L_RING_FINGER_PIP', 'L_RING_FINGER_DIP', 'L_RING_FINGER_TIP', 'L_PINKY_MCP',
              'L_PINKY_PIP', 'L_PINKY_DIP', 'L_PINKY_TIP', 'R_WRIST', 'R_THUMB_CMC', 'R_THUMB_MCP', 'R_THUMB_IP', 'R_THUMB_TIP',
              'R_INDEX_FINGER_MCP', 'R_INDEX_FINGER_PIP', 'R_INDEX_FINGER_DIP', 'R_INDEX_FINGER_TIP', 'R_MIDDLE_FINGER_MCP', 
              'R_MIDDLE_FINGER_PIP', 'R_MIDDLE_FINGER_DIP', 'R_MIDDLE_FINGER_TIP', 'R_RING_FINGER_MCP', 'R_RING_FINGER_PIP', 
              'R_RING_FINGER_DIP', 'R_RING_FINGER_TIP', 'R_PINKY_MCP', 'R_PINKY_PIP', 'R_PINKY_DIP', 'R_PINKY_TIP','NOSE',
              'LEFT_EYE_INNER', 'LEFT_EYE', 'LEFT_EYE_OUTER', 'RIGHT_EYE_INNER', 'RIGHT_EYE', 'RIGHT_EYE_OUTER', 'LEFT_EAR', 'RIGHT_EAR',
              'MOUTH_LEFT', 'MOUTH_RIGHT', 'LEFT_SHOULDER', 'RIGHT_SHOULDER', 'LEFT_ELBOW', 'RIGHT_ELBOW', 'LEFT_WRIST', 'RIGHT_WRIST', 
              'LEFT_PINKY', 'RIGHT_PINKY', 'LEFT_INDEX', 'RIGHT_INDEX', 'LEFT_THUMB', 'RIGHT_THUMB', 'LEFT_HIP', 'RIGHT_HIP', 
              'LEFT_KNEE', 'RIGHT_KNEE', 'LEFT_ANKLE','RIGHT_ANKLE', 'LEFT_HEEL', 'RIGHT_HEEL', 'LEFT_FOOT_INDEX', 'RIGHT_FOOT_INDEX']
    writer = csv.DictWriter(f, fieldnames=myFields)
    writer.writerow({'TIME': current_time, 'L_WRIST': total[0], 'L_THUMB_CMC': total[1], 'L_THUMB_MCP': total[2], 'L_THUMB_IP': total[3], 
                     'L_THUMB_TIP': total[4], 'L_INDEX_FINGER_MCP': total[5], 'L_INDEX_FINGER_PIP': total[6],
                     'L_INDEX_FINGER_DIP': total[7], 'L_INDEX_FINGER_TIP': total[8], 'L_MIDDLE_FINGER_MCP': total[9],
                     'L_MIDDLE_FINGER_PIP': total[10], 'L_MIDDLE_FINGER_DIP': total[11],
                     'L_MIDDLE_FINGER_TIP': total[12], 'L_RING_FINGER_MCP': total[13], 'L_RING_FINGER_PIP': total[14], 
                     'L_RING_FINGER_DIP': total[15], 'L_RING_FINGER_TIP': total[16], 'L_PINKY_MCP': total[17],
                     'L_PINKY_PIP': total[18], 'L_PINKY_DIP': total[19], 'L_PINKY_TIP': total[20], 'R_WRIST': total[21], 
                     'R_THUMB_CMC': total[22], 'R_THUMB_MCP': total[23], 'R_THUMB_IP': total[24], 'R_THUMB_TIP': total[25],
                     'R_INDEX_FINGER_MCP': total[26], 'R_INDEX_FINGER_PIP': total[27], 'R_INDEX_FINGER_DIP': total[28],
                     'R_INDEX_FINGER_TIP': total[29], 'R_MIDDLE_FINGER_MCP': total[30], 
                     'R_MIDDLE_FINGER_PIP': total[31], 'R_MIDDLE_FINGER_DIP': total[32], 'R_MIDDLE_FINGER_TIP': total[33],
                     'R_RING_FINGER_MCP': total[34], 'R_RING_FINGER_PIP': total[35], 
                     'R_RING_FINGER_DIP': total[36], 'R_RING_FINGER_TIP': total[37], 'R_PINKY_MCP': total[38], 'R_PINKY_PIP': total[39], 
                     'R_PINKY_DIP': total[40], 'R_PINKY_TIP': total[41],
                     'NOSE': total[42], 'LEFT_EYE_INNER': total[43], 'LEFT_EYE': total[44], 'LEFT_EYE_OUTER': total[45], 
                     'RIGHT_EYE_INNER': total[46], 'RIGHT_EYE': total[47], 'RIGHT_EYE_OUTER': total[48], 'LEFT_EAR': total[49], 
                     'RIGHT_EAR': total[50], 'MOUTH_LEFT': total[51], 'MOUTH_RIGHT': total[52], 'LEFT_SHOULDER': total[53], 
                     'RIGHT_SHOULDER': total[54], 'LEFT_ELBOW': total[55], 'RIGHT_ELBOW': total[56], 'LEFT_WRIST': total[57], 
                     'RIGHT_WRIST': total[58], 'LEFT_PINKY': total[59], 'RIGHT_PINKY': total[60], 'LEFT_INDEX': total[61], 
                     'RIGHT_INDEX': total[62], 'LEFT_THUMB': total[63], 'RIGHT_THUMB': total[64], 'LEFT_HIP': total[65], 'RIGHT_HIP': total[66], 
                     'LEFT_KNEE': total[67], 'RIGHT_KNEE': total[68], 'LEFT_ANKLE': total[69], 'RIGHT_ANKLE': total[70], 
                     'LEFT_HEEL': total[71], 'RIGHT_HEEL': total[72], 'LEFT_FOOT_INDEX': total[73], 'RIGHT_FOOT_INDEX': total[74]})
  
  if cv2.waitKey(10) & 0xFF == ord('q'):
    break

holistic.close()
cap.release()
