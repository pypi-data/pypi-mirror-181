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


def find_temp(csv_matrix, image_x, image_y, image_width, image_height):
  m_width = len(csv_matrix[0])
  m_height = len(csv_matrix)
  rate1 = m_width * 1.0 / image_width
  rate2 = m_height * 1.0 / image_height
  c_x = int(image_x * rate1) - 1
  c_y = int(image_y * rate2) - 1
  if c_x < 0:
    c_x = 0
  if c_y < 0:
    c_y = 0
  if c_x > m_width - 1:
    c_x = m_width - 1
  if c_y > m_height - 1:
    c_y = m_height - 1
  print(f"cx={c_x},cy={c_y}")
  return csv_matrix[c_y][c_x], c_x, c_y

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def detect_face(image_path,save_detect_path=None,show=True,ext=".png",model_selection=0, min_detection_confidence=0.5):
  # For static images:
  IMAGE_FILES = [image_path]
  list_node=[]
  list_connection=[]
  annotated_image=None

  with mp_face_detection.FaceDetection(
      model_selection=model_selection, min_detection_confidence=min_detection_confidence) as face_detection:
    count=0
    for idx, file in enumerate(IMAGE_FILES):
      image = cv2.imread(file)
      img_matrix = read_infrared_data(file.replace(ext, ".csv"))
      print("matrix: ", len(img_matrix[0]), len(img_matrix))
      # print("shape: ",image.shape)
      image_height, image_width, _ = image.shape
      print("shape: ", image_width, image_height)
      # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
      results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

      # Draw face detections of each face.
      if not results.detections:
        print("Not found!")
        continue
      annotated_image = image.copy()
      for detection in results.detections:
        # print(detection)
        # ('Nose tip:')
        # print(mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
        nose_tip=mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.NOSE_TIP)
        left_eye=mp_face_detection.get_key_point(detection,mp_face_detection.FaceKeyPoint.LEFT_EYE)
        right_eye = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE)
        left_ear_tragion = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.LEFT_EAR_TRAGION)
        right_ear_tragion = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.RIGHT_EAR_TRAGION)
        mouth_center = mp_face_detection.get_key_point(detection, mp_face_detection.FaceKeyPoint.MOUTH_CENTER)
        # bounding_box=detection.relative_bounding_box
        box=detection.location_data.relative_bounding_box
        score=detection.score
        print("box: ",box)
        print("noise tip: ",nose_tip.x, nose_tip.y)
        print("score: ",score)
        def convert_m_xy(d):
          x = d.x * image_width
          y = d.y * image_height
          temp, c_x, c_y = find_temp(img_matrix, x, y, image_width, image_height)
          return (c_x,c_y,temp)
        model={
          "id":f"face-{count}",
          "score":score,
          "box": (int(box.xmin * image_width),int(box.ymin*image_height),int(box.width*image_width),int(box.height*image_height)),
          "nose_tip":convert_m_xy(nose_tip),
          "left_eye": convert_m_xy(left_eye),
          "right_eye": convert_m_xy(right_eye),
          "left_ear_tragion": convert_m_xy(left_ear_tragion),
          "right_ear_tragion": convert_m_xy(right_ear_tragion),
          "mouth_center":convert_m_xy(mouth_center)
        }
        list_node.append(model)
        count+=1

        mp_drawing.draw_detection(annotated_image, detection)
      if save_detect_path!=None:
        cv2.imwrite(save_detect_path, annotated_image)
      if show:
        cv2.imshow('annotated',annotated_image)
        cv2.waitKey()
  return annotated_image,list_node,list_connection


