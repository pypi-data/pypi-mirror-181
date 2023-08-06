import cv2
import mediapipe as mp

def read_infrared_data(file):
    lines = open(file, "r", encoding='utf-8')
    data = []
    for line in lines:
        vs = line.strip().split(",")
        row = [float(v) for v in vs]
        data.append(row)
    return data

def find_temp(csv_matrix,image_x,image_y,image_width,image_height):
    m_width=len(csv_matrix[0])
    m_height=len(csv_matrix)
    rate1=m_width*1.0/image_width
    rate2=m_height*1.0/image_height
    c_x=int(image_x*rate1)-1
    c_y=int(image_y*rate2)-1
    if c_x<0:
        c_x=0
    if c_y<0:
        c_y=0
    if c_x>m_width-1:
        c_x=m_width-1
    if c_y > m_height-1:
        c_y=m_height-1
    print(f"cx={c_x},cy={c_y}")
    return csv_matrix[c_y][c_x],c_x,c_y

def props_with_(obj):
    pr={}
    for name in dir(obj):
        value=getattr(obj,name)
        if not name.startswith('__') and not callable(value):
            pr[name]=value
    return pr

def detect_hand(image_path,save_detected_path=None,show=False,ext=".png",min_detection_confidence=0.5):

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # For static images:
    IMAGE_FILES = [image_path]
    annotated_image=None
    list_model=[]
    list_connections=[]
    count=0
    with mp_hands.Hands(
        static_image_mode=True,
        max_num_hands=2,
        min_detection_confidence=min_detection_confidence) as hands:
      for idx, file in enumerate(IMAGE_FILES):
        img_matrix = read_infrared_data(file.replace(ext,".csv"))
        print("matrix: ",len(img_matrix[0]),len(img_matrix))
        # Read an image, flip it around y-axis for correct handedness output (see
        # above).
        image = cv2.flip(cv2.imread(file), 1)
        #print("shape: ",image.shape)
        image_height,image_width,_=image.shape
        print("shape: ", image_width,image_height)
        # Convert the BGR image to RGB before processing.
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print handedness and draw hand landmarks on the image.
        print('Handedness:', results.multi_handedness)
        cls=results.multi_handedness[0]
        import re
        xx=re.findall(r'score: ([\d\.]+) ', str(cls).replace("\n"," "))

        score=float(xx[0].strip())
        print("score: ",xx[0])
        if not results.multi_hand_landmarks:
          continue
        image_height, image_width, _ = image.shape
        annotated_image = image.copy()
        for hand_landmarks in results.multi_hand_landmarks:
          # print(f'hand_landmarks:', hand_landmarks)
          print("hand_landmarks: ")

          for idx1,hand_lanmark in enumerate(hand_landmarks.landmark):
                print(idx1)
                x=hand_lanmark.x * image_width
                y=hand_lanmark.y * image_height
                z=hand_lanmark.z
                temp,c_x,c_y=find_temp(img_matrix,x,y,image_width,image_height)
                print(x,y,z)
                print("temp = "+str(temp))
                print()
                list_model.append({
                    "id":f"hand-{count}-"+str(idx1),
                    "x":c_x,
                    "y":c_y,
                    "z":z,
                    "temp":temp
                })
          print(
              f'Index finger tip coordinates: (',
              f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
              f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
          )

          for model in mp_hands.HAND_CONNECTIONS:
              list_connections.append({
                  "id": f"hand-{count}-" + str(idx1),
                  "start":model[0],
                  "end":model[1]
              })

          mp_drawing.draw_landmarks(
              annotated_image,
              hand_landmarks,
              mp_hands.HAND_CONNECTIONS,
              mp_drawing_styles.get_default_hand_landmarks_style(),
              mp_drawing_styles.get_default_hand_connections_style())
          count += 1
        if save_detected_path!=None:
            cv2.imwrite(save_detected_path, cv2.flip(annotated_image, 1))

        if show:
            cv2.imshow("annotated image",annotated_image)
            cv2.waitKey()


        '''
        # Draw hand world landmarks.
        if not results.multi_hand_world_landmarks:
          continue
        for hand_world_landmarks in results.multi_hand_world_landmarks:
          mp_drawing.plot_landmarks(
            hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
        '''

    return annotated_image,list_model,list_connections,score