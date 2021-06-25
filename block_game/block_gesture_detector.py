import cv2
import mediapipe as mp
import csv
import time
import socket

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
maxconn = 10
hostname = 'kaushek-VivoBook-Flip-14-TP410UF'
port = 12345
IP = '127.0.0.1'

listen_socket.bind((IP, port))
listen_socket.listen(maxconn)

print("Server started! " + IP + ".... port: " + str(port))
(clientsocket, address) = listen_socket.accept()
print("Connection established")

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# For webcam input:
    
holistic = mp_holistic.Holistic(min_detection_confidence=0.4, min_tracking_confidence=0.4)
cap = cv2.VideoCapture(0)

key_point = "L_INDEX_FINGER_TIP"

#initializing time
time.sleep(3)
filename = "movement_data.csv"
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

fields = ['Time', 'Co-ordinate']
with open(filename, 'a+', newline="") as f:
          fields = ['Time', 'Co-ordinate']
          writer = csv.DictWriter(f, fieldnames=fields)
          writer.writerow({'Time': 'Time', 'Co-ordinate': 'Co-ordinate'})
settin = True
initial_time = time.time()
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
      print(image.shape)
      image.flags.writeable = False

      image.flags.writeable = True
      
      results = holistic.process(image)
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
      
      cv2.imshow('MediaPipe Holistic', image)
      
      i = 0
      for content in myFields:
          if content == key_point:
              content_ind = i
              break
          i+=1
    
      #writing the final data in a csv file
      
    
      #having landmarks as a list => contains x,y coordinates of each position of landmark in order as listed in website
      left_hand = []
      for i in range(0, 21, 1):
        if results.left_hand_landmarks:
          a = [results.left_hand_landmarks.landmark[i].x * image_width, results.left_hand_landmarks.landmark[i].y * image_height]
          left_hand.append(a)
        else:
          #left_hand.append(None)
          left_hand.append('n/d')
          
      '''right_hand = []
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
          pose.append('n/d')'''
         
      #combining all the coordinates
      #total = left_hand + right_hand + pose
      total = left_hand
      content = total[content_ind]
      current_time = time.time() - initial_time
      
      with open(filename, 'a+', newline="") as f:
          fields = ['Time', 'Co-ordinate']
          writer = csv.DictWriter(f, fieldnames=fields)
          writer.writerow({'Time': current_time, 'Co-ordinate': content})
            
      if content != 'n/d':
          cont = [float(i) for i in content]
          position = str(cont)[1:-1]
          print(position)
          position = position.encode('utf-8')
          clientsocket.send(position)
          
      else:
          #print("Place your index finger in front of the camera")
          position = 'n/d, n/d'
          position = position.encode('utf-8')
          clientsocket.send(position)
    
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    else:
        position = 'n/d, n/d'
        position = position.encode('utf-8')
        clientsocket.send(position)

holistic.close()
cap.release()
