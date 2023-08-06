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

def detect_face_mesh(image_path,save_detected_path=None,show=True,ext=".png",refine_landmarks=False, min_detection_confidence=0.5,min_tracking_confidence=0.5):

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    # For static images:
    IMAGE_FILES = [image_path]
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    list_node=[]
    list_connection=[]
    annotated_image=None
    with mp_face_mesh.FaceMesh(
        static_image_mode=True,
        max_num_faces=1,
        refine_landmarks=refine_landmarks,
        min_detection_confidence=min_detection_confidence,min_tracking_confidence=min_tracking_confidence) as face_mesh:
      for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        image_height, image_width, _ = image.shape
        # Print and draw face mesh landmarks on the image.
        if not results.multi_face_landmarks:
          print("Not found!")
          continue
        annotated_image = image.copy()
        count=0
        for face_landmarks in results.multi_face_landmarks:
          img_matrix = read_infrared_data(file.replace(ext, ".csv"))
          print("matrix: ", len(img_matrix[0]), len(img_matrix))
          print('face_landmarks:', face_landmarks)
          for idx1,hand_lanmark in enumerate(face_landmarks.landmark):
                print(idx1)
                x=hand_lanmark.x * image_width
                y=hand_lanmark.y * image_height
                z=hand_lanmark.z
                temp,c_x,c_y=find_temp(img_matrix,x,y,image_width,image_height)
                print(c_x,c_y,z)
                print("temp = "+str(temp))
                print()
                list_node.append({
                    "id": f"facemesh-{count}",
                    "x":c_x,
                    "y":c_y,
                    "z":z,
                    "temp":temp
                })
          # connection of tesselation
          for c in mp_face_mesh.FACEMESH_TESSELATION:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"tesselation",
                  "start":c[0],
                  "end":c[1]
              })
          for c in mp_face_mesh.FACEMESH_IRISES:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"irises",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_CONTOURS:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"contours",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_LEFT_EYE:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"left_eye",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_RIGHT_EYE:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"right_eye",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_LIPS:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"lips",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_LEFT_EYEBROW:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"left_eyebow",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_RIGHT_EYEBROW:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"right_eyebow",
                  "start": c[0],
                  "end": c[1]
              })
          for c in mp_face_mesh.FACEMESH_FACE_OVAL:
              # print(c[0],c[1])
              list_connection.append({
                  "id": f"facemesh-{count}",
                  "type":"face_oval",
                  "start": c[0],
                  "end": c[1]
              })

          mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_tesselation_style())
          mp_drawing.draw_landmarks(
              image=annotated_image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_CONTOURS,
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_contours_style())
          if refine_landmarks:
              mp_drawing.draw_landmarks(
                  image=annotated_image,
                  landmark_list=face_landmarks,
                  connections=mp_face_mesh.FACEMESH_IRISES,
                  landmark_drawing_spec=None,
                  connection_drawing_spec=mp_drawing_styles
                  .get_default_face_mesh_iris_connections_style())

        if save_detected_path!=None:
            cv2.imwrite(save_detected_path, annotated_image)
        if show:
            cv2.imshow("annotated",annotated_image)
            cv2.waitKey()
        count+=1
    return annotated_image,list_node,list_connection

