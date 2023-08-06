import cv2
import mediapipe as mp
import numpy as np


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
        c_x=-1
    if c_y > m_height-1:
        c_y=-1
    # print(f"cx={c_x},cy={c_y}")
    if c_x==-1 or c_y==-1:
        return -1,-1,-1
    return csv_matrix[c_y][c_x],c_x,c_y

def detect_pose(image_path,save_detect_path=None,show=True,ext=".png",   model_complexity=2,  enable_segmentation=True,):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic
    # For static images:
    IMAGE_FILES = [image_path]
    BG_COLOR=[0,0,0]
    annotated_image=None
    list_node=[]
    list_connection=[]
    count=0
    with mp_holistic.Holistic(
        static_image_mode=True,
        model_complexity=model_complexity,
        enable_segmentation=enable_segmentation,
        refine_face_landmarks=True) as holistic:
      for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        image_height, image_width, _ = image.shape
        img_matrix = read_infrared_data(file.replace(ext, ".csv"))
        # Convert the BGR image to RGB before processing.
        results = holistic.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            return None,None,None

        for part in mp_holistic.PoseLandmark:
            print("part: ",part)
            x=results.pose_landmarks.landmark[part].x * image_width
            y = results.pose_landmarks.landmark[part].y * image_height
            temp,c_x,c_y=find_temp(img_matrix,x,y,image_width,image_height)
            list_node.append({
                "id":f"pose-{count}",
                "part":str(part).replace("PoseLandmark.",""),
                "x":c_x,
                "y":c_y,
                "temp":temp
            })
            print(list_node[len(list_node)-1])
            print()
        # for hand_part in mp_holistic.HandLandmark:
        #    print("hand part: ",hand_part)
        for idx1,model in enumerate(mp_holistic.POSE_CONNECTIONS):
            list_connection.append({
                "id": f"hand-{count}-" + str(idx1),
                "start": model[0],
                "end": model[1]
            })

        annotated_image = image.copy()
        # Draw segmentation on the image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        annotated_image = np.where(condition, annotated_image, bg_image)
        # Draw pose, left and right hands, and face landmarks on the image.
        '''
        mp_drawing.draw_landmarks(
            annotated_image,
            results.face_landmarks,
            mp_holistic.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_tesselation_style())
        '''
        mp_drawing.draw_landmarks(
            annotated_image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.
            get_default_pose_landmarks_style())
        if save_detect_path!=None:
            cv2.imwrite(save_detect_path, annotated_image)
        if show:
            cv2.imshow("annotated",annotated_image)
            cv2.waitKey()
        # Plot pose world landmarks.
        # mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_holistic.POSE_CONNECTIONS)
    return annotated_image,list_node,list_connection
