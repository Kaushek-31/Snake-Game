import cv2
import mediapipe as mp
import csv
import time

import socket

listen_socket = socket.socket()
port = 8000
maxconn = 10
IP = socket.gethostname()

listen_socket.bind(('', port))
listen_socket.listen(maxconn)

print("Server started! " + IP + ".... port: " + str(port))
(clientsocket, address) = listen_socket.accept()
print("Connection established")
          

def most_frequent(List): 
    return max(set(List), key = List.count) 

def direction(key_pos):
    full = []
    for i in range(0, len(key_pos)-1, 1):
      key_diff_x = key_pos[i+1][0] - key_pos[i][0]
      key_diff_y = key_pos[i+1][1] - key_pos[i][1]
      
      if key_diff_x > 150 or key_diff_x < -150:
          if key_diff_x > 0:
              full.append("right")
          else:
              full.append("left")
              
#      if key_diff_y > 50 or key_diff_y < -50:
      elif key_diff_y > 60 or key_diff_y < -60:
          if key_diff_y > 0:
              full.append("up")
          else:
              full.append("down")
              
      else:
          full.append("no_change")
          
      print(full)
      #return most_frequent(full)

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# For webcam input:
    
holistic = mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4)
cap = cv2.VideoCapture(0)

key_point = "L_INDEX_FINGER_TIP"

#initializing time
time.sleep(3)
initial_time = time.time()

save = 0
key_positions = []
key_length = 3

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

settin = True
while settin:
    if cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Empty frame. Proceeding further...")
        # If loading a video, use 'break' instead of 'continue'.
        continue
    
      # Flip the image horizontally for a later selfie-view display, and convert
      # the BGR image to RGB.

      image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
      image_height, image_width, _ = image.shape
      image.flags.writeable = False
      results = holistic.process(image)

      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      
      mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
      mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
      mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
      
      cv2.imshow('MediaPipe Holistic', image)
      
      i = 0
      for content in myFields:
          if content == key_point:
              content_ind = i
              break
          i+=1
    
      #writing the final data in a csv file
      current_time = time.time() - initial_time
    
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
         
      #combining all the coordinates
      total = left_hand + right_hand + pose
      content = total[content_ind]
      
      if content != 'n/d':
          if len(key_positions) <= key_length:
              key_positions.append(content)
          else:
              key_positions.pop(0)
              key_positions.append(content)
          key_diff_x = key_positions[len(key_positions) - 1][0] - key_positions[0][0]
          key_diff_y = key_positions[len(key_positions) - 1][1] - key_positions[0][1]
          
          if key_diff_x > 150 or key_diff_x < -150:
              if key_diff_x > 0:
                  position = "d"
              else:
                  position = "a" 
    #      if key_diff_y > 50 or key_diff_y < -50:
          elif key_diff_y > 60 or key_diff_y < -60:
              if key_diff_y < 0:
                  position = "w"
              else:
                  position = "s" 
          else:
              position = "q"
          #result = direction(key_positions)
          #print(result)
          
          clientsocket.send(position.encode())
          print("Message_sent")
          
      else:
          #print("Place your index finger in front of the camera")
          position = 'r'
          clientsocket.send(position.encode())
          print("Message_sent")
          if (len(key_positions) > 0):
              key_positions.pop(0)
    
      if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
    else:
        position = 'q'
        clientsocket.send(position.encode())
        print("Message_sent")

holistic.close()
cap.release()
