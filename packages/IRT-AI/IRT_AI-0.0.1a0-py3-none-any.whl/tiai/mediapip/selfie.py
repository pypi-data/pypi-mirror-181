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
    c_x=int(image_x*rate1)
    c_y=int(image_y*rate2)
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

def detect_shape(image_path,save_detect_path=None,show=True,ext=".png"):
    mp_drawing = mp.solutions.drawing_utils
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    # For static images:
    IMAGE_FILES = [image_path]
    BG_COLOR = (192, 192, 192) # gray
    MASK_COLOR = (255, 255, 255) # white
    list_nodes=[]
    list_connections=[]
    output_image=None
    with mp_selfie_segmentation.SelfieSegmentation(
        model_selection=0) as selfie_segmentation:
      for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        img_matrix = read_infrared_data(file.replace(ext, ".csv"))
        image=cv2.resize(image,(len(img_matrix[0]),len(img_matrix)))
        image_height, image_width, _ = image.shape
        print(image_width,image_height)

        # Convert the BGR image to RGB before processing.
        results = selfie_segmentation.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw selfie segmentation on the background image.
        # To improve segmentation around boundaries, consider applying a joint
        # bilateral filter to "results.segmentation_mask" with "image".
        # print(results.segmentation_mask)

        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
        print(condition.shape)
        print(len(condition[0]))
        num_true=0
        num_false=0

        for i in range(len(condition[0])):
          for j in range(len(condition)):
            flag=condition[j][i]
            if flag[0] and flag[1] and flag[2]:
                num_true+=1
                temp, c_x, c_y = find_temp(img_matrix, i, j, image_width, image_height)
                list_nodes.append({
                    "id":"selfie",
                    "x": c_x,
                    "y": c_y,
                    "temp":temp
                }
                )
            else:
              num_false+=1

        print("len of true: ",num_true)
        print("len of false: ",num_false)

        # Generate solid color images for showing the output selfie segmentation mask.
        fg_image = np.zeros(image.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR
        output_image = np.where(condition, image, bg_image)
        if save_detect_path!=None:
            cv2.imwrite(save_detect_path, output_image)
        if show:
            cv2.imshow("Annotated",cv2.resize(output_image,(int(image_height/2),int(image_width/2))))
            cv2.waitKey()
    return output_image,list_nodes,list_connections

if __name__=="__main__":
    image_path='../data/human/1.1/head/head1.png'
    img,nodes,connections=detect_shape(image_path=image_path)
    for node in nodes[:10]:
        print(node)

