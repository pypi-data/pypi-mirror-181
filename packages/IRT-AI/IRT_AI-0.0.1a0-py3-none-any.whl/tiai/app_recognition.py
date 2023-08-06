import PyQt5
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from tiai.mediapip.hand import *
from tiai.mediapip.face_mesh import *
from tiai.mediapip.face import *
from tiai.mediapip.pose import *
from tiai.mediapip.selfie import *
from tiai.ui_infrared_recognition import Ui_MainWindow
import sys
import os
import ctypes
from tiai.image_viewer import ImageViewer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class DetectCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure( dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_xlim(1, width)
        self.axes.set_ylim(1,height)
        self.axes.invert_yaxis()
        # self.axes.set_box_aspect(1)
        super(DetectCanvas, self).__init__(fig)

myappid = 'health-infrared-mgs-gui'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class MyMainForm(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.btn_browse.clicked.connect(self.browse_report_path)
        self.btn_analyze.clicked.connect(self.analyze)
        self.btn_analyze_face.clicked.connect(self.analyze_face)
        self.btn_analyze_pose.clicked.connect(self.analyze_pose)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_analyze_shape.clicked.connect(self.analyze_shape)

        self.cb_analyze_file.stateChanged.connect(self.state_changed)

        self.cb_body_part.currentTextChanged.connect(self.body_part_changed)
        self.body_parts=['arm','ear','feet','hand','head','leg','neck']
        self.dict_faces={}
        self.dict_faces['arm']=['arm1','arm2']
        self.dict_faces['ear']=['ear1','ear2']
        self.dict_faces['feet']=['feet1','feet2']
        self.dict_faces['hand']=['hand1','hand2','hand3','hand4']
        self.dict_faces['head']=['head1','head2','head3']
        self.dict_faces['leg']=['leg1','leg2']
        self.dict_faces['neck']=['neck1','neck2','neck3','neck4']
        self.cb_body_part.clear()
        for bp in self.body_parts:
            self.cb_body_part.addItem(bp)

        self.canvas_original=None
        self.iv_hand=None
        self.iv_landmarks=None

        # add canvas for plot data
        '''
        self.detect_canvas = DetectCanvas(self, width=5, height=4, dpi=100)
        self.detect_canvas.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.layout_plot.addWidget(self.detect_canvas)
        '''
        self.detect_canvas=None
        # self.plot_detected_results(x=[],y=[],width=5,height=4)
        self.gb_report.setEnabled(True)
        self.gb_file.setEnabled(False)


    def state_changed(self):
        if self.cb_analyze_file.isChecked():
            self.gb_report.setEnabled(False)
            self.gb_file.setEnabled(True)
        else:
            self.gb_report.setEnabled(True)
            self.gb_file.setEnabled(False)

    def open_file(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Select a CSV file", "",
                                                  "All Files (*);;CSV Files (*.csv)")
        if fileName:
            print(fileName)
            self.edit_file_path.setText(fileName)

    def plot_detected_results(self,part,list_node,list_connection,width,height):
        if self.detect_canvas!=None:
            self.layout_plot.removeWidget(self.detect_canvas)
        list_x=[]
        list_y=[]
        list_temp=[]
        for node in list_node:
            if part=='face':
                for k in node:
                    if type(node[k])==tuple and k!="box":
                        x=node[k][0]
                        y=node[k][1]
                        list_x.append(x)
                        list_y.append(y)
                        list_temp.append(node[k][2])
            elif part=="shape":
                if node['temp']<self.sb_min_temp.value():
                    continue
                list_x.append(node['x'])
                list_y.append(node['y'])
                list_temp.append(node['temp'])
            else:
                if node['temp']==-1:
                    continue
                list_x.append(node['x'])
                list_y.append(node['y'])
                list_temp.append(node['temp'])
        if part=="shape":
            self.detect_canvas = DetectCanvas(self, width=width, height=height, dpi=100)
            self.detect_canvas.axes.scatter(x=list_x, y=list_y, c=list_temp, cmap='inferno',s=0.1)
            self.layout_plot.addWidget(self.detect_canvas)
        else:
            self.detect_canvas = DetectCanvas(self, width=width, height=height, dpi=100)
            self.detect_canvas.axes.scatter(x=list_x, y=list_y,s=list_temp,alpha=0.5,c=list_temp,cmap='inferno')
            self.layout_plot.addWidget(self.detect_canvas)

    def remove_plot_detected_reuslts(self):
        if self.detect_canvas!=None:
            self.layout_plot.removeWidget(self.detect_canvas)

    def show_original_image(self,csv_path):
        if self.canvas_original!=None:
            self.layout_original.removeWidget(self.canvas_original)
        figure = plt.figure(facecolor='#F5F5F5', )  # 可选参数,facecolor为背景颜色
        self.canvas_original = FigureCanvas(figure)
        self.layout_original.addWidget(self.canvas_original)
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
        sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题
        data = self.read_infrared_data(csv_path)
        ax = sns.heatmap(data,
                         xticklabels=False,  # remove the labels
                         yticklabels=False,
                         cbar=False
                         # cmap='rainbow',
                         # padding=0
                         )
        # cbar = ax.collections[0].colorbar
        # cbar.ax.tick_params(labelsize=5)
        plt.tight_layout()

        ## 坐标
        def on_move(event):
            # get the x and y pixel coords
            x, y = event.x, event.y
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                x1 = int(event.xdata)
                y1 = int(event.ydata)
                v = data[y1][x1]
                self.lb_xyv.setText(f"Temp:（{x1},{y1}） = {v}")
                # print('data coords %f %f' % (event.xdata, event.ydata))

        # define a click event
        def on_click(event):
            x, y = event.x, event.y
            if event.inaxes:
                ax = event.inaxes  # the axes instance
                # print('data coords %f %f' % (event.xdata, event.ydata))
                x1 = int(event.xdata)
                y1 = int(event.ydata)
                v = data[y1][x1]
                print(x1, y1, v)
                # self.edit_x.setText(str(x1))
                # self.edit_y.setText(str(y1))
                # self.edit_temperature.setText(str(v))

        binding_id = plt.connect('motion_notify_event', on_move)
        plt.connect('button_press_event', on_click)

        self.canvas_original.draw()

    def analyze_shape(self):
        self.remove_plot_detected_reuslts()
        if not self.cb_analyze_file.isChecked():
            csv_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".csv"
            img_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".png"
            save_hand_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".detected.png"
        else:
            csv_path = self.edit_file_path.text()
            file, ext = os.path.splitext(csv_path)
            img_path = file + ".png"
            save_hand_path = file + ".detected.png"
            # generate png image
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
            sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题
            data = self.read_infrared_data(csv_path)
            ax = sns.heatmap(data,
                             xticklabels=False,  # remove the labels
                             yticklabels=False,
                             cbar=False
                             )
            plt.tight_layout()
            plt.savefig(img_path, dpi=300, bbox_inches='tight', pad_inches=0)

        self.show_original_image(csv_path)

        img, list_nodes, list_connections = detect_shape(image_path=img_path, show=False,
                                                        save_detect_path=save_hand_path)
        img_matrix = read_infrared_data(csv_path)
        img_m_width = len(img_matrix[0])
        img_m_height = len(img_matrix)
        if self.iv_hand != None:
            self.layout_detection.removeWidget(self.iv_hand)
        if os.path.exists(save_hand_path) and list_nodes != None and len(list_nodes) != 0:
            self.iv_hand = ImageViewer(image_file=save_hand_path)
            self.layout_detection.addWidget(self.iv_hand)
            # show 21 points and temperature
            self.lw_landmarks.clear()
            self.lw_connections.clear()
            '''
            for model in list_nodes[:100]:
                if model['temp'] == -1:
                    continue
                self.lw_landmarks.addItem(f'({model["x"]},{model["y"]}) :{model["temp"]}')
            for c in list_connections:
                self.lw_connections.addItem(f"{c['id']}, {c['start']}, {c['end']}")
            
            if self.iv_landmarks != None:
                self.iv_landmarks.setImage("references/pose_tracking_full_body_landmarks.png")
            else:
                self.iv_landmarks = ImageViewer(image_file="references/pose_tracking_full_body_landmarks.png")
                self.layout_reference.addWidget(self.iv_landmarks)
            '''
            self.plot_detected_results('shape', list_nodes, list_connections, width=img_m_width, height=img_m_height)
        else:
            QMessageBox.information(self, "Tip", "Failed to detect!")
            if self.iv_hand != None:
                self.layout_detection.removeWidget(self.iv_hand)
            if self.iv_landmarks != None:
                self.iv_landmarks.setImage("")
            self.lw_landmarks.clear()
            self.lw_connections.clear()

    def analyze_pose(self):
        self.remove_plot_detected_reuslts()
        if not self.cb_analyze_file.isChecked():
            csv_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".csv"
            img_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".png"
            save_hand_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".detected.png"
        else:
            csv_path=self.edit_file_path.text()
            file,ext=os.path.splitext(csv_path)
            img_path=file+".png"
            save_hand_path=file+".detected.png"
            # generate png image
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
            sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题
            data = self.read_infrared_data(csv_path)
            ax = sns.heatmap(data,
                             xticklabels=False,  # remove the labels
                             yticklabels=False,
                             cbar=False
                             )
            plt.tight_layout()
            plt.savefig(img_path,dpi=300,bbox_inches='tight',   pad_inches = 0)

        self.show_original_image(csv_path)

        img, list_nodes, list_connections = detect_pose(image_path=img_path, show=False,
                                                        save_detect_path=save_hand_path)
        img_matrix=read_infrared_data(csv_path)
        img_m_width=len(img_matrix[0])
        img_m_height=len(img_matrix)
        if self.iv_hand != None:
            self.layout_detection.removeWidget(self.iv_hand)
        if os.path.exists(save_hand_path) and list_nodes != None and len(list_nodes) != 0:
            self.iv_hand = ImageViewer(image_file=save_hand_path)
            self.layout_detection.addWidget(self.iv_hand)
            # show 21 points and temperature
            self.lw_landmarks.clear()
            self.lw_connections.clear()
            for model in list_nodes:
                if model['temp'] == -1:
                    continue
                self.lw_landmarks.addItem(f'{model["id"]}: {model["part"]}: {model["temp"]}')
            for c in list_connections:
                self.lw_connections.addItem(f"{c['id']}, {c['start']}, {c['end']}")
            if self.iv_landmarks!=None:
                self.iv_landmarks.setImage("references/pose_tracking_full_body_landmarks.png")
            else:
                self.iv_landmarks = ImageViewer(image_file="references/pose_tracking_full_body_landmarks.png")
                self.layout_reference.addWidget(self.iv_landmarks)
            self.plot_detected_results('pose',list_nodes,list_connections,width=img_m_width,height=img_m_height)
        else:
            QMessageBox.information(self, "Tip", "Failed to detect!")
            if self.iv_hand != None:
                self.layout_detection.removeWidget(self.iv_hand)
            if self.iv_landmarks!=None:
                self.iv_landmarks.setImage("")
            self.lw_landmarks.clear()
            self.lw_connections.clear()

    def analyze_face(self):
        self.remove_plot_detected_reuslts()
        if not self.cb_analyze_file.isChecked():
            csv_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".csv"
            img_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".png"
            save_hand_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".detected.png"
        else:
            csv_path=self.edit_file_path.text()
            file,ext=os.path.splitext(csv_path)
            img_path=file+".png"
            save_hand_path=file+".detected.png"
            # generate png image
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
            sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题
            data = self.read_infrared_data(csv_path)
            ax = sns.heatmap(data,
                             xticklabels=False,  # remove the labels
                             yticklabels=False,
                             cbar=False
                             )
            plt.tight_layout()
            plt.savefig(img_path,dpi=300,bbox_inches='tight',   pad_inches = 0)

        self.show_original_image(csv_path)
        if self.iv_landmarks!=None:
            self.iv_landmarks.setImage("")
        # if self.cb_body_part.currentText() not in ['head']:
        #     QMessageBox.information(self,"Tip","NOT Select Head!")
        #    return
        img_matrix = read_infrared_data(csv_path)
        img_m_width = len(img_matrix[0])
        img_m_height = len(img_matrix)
        img, list_nodes, list_connections = detect_face(image_path=img_path, show=False,
                                                             save_detect_path=save_hand_path)
        if list_nodes == None or len(list_nodes) == 0:
            QMessageBox.information(self, "Tip", "Not Found!")
            return
        if self.iv_hand != None:
            self.layout_detection.removeWidget(self.iv_hand)
        if os.path.exists(save_hand_path):
            self.iv_hand = ImageViewer(image_file=save_hand_path)
            self.layout_detection.addWidget(self.iv_hand)
            # show 21 points and temperature
            self.lw_landmarks.clear()
            self.lw_connections.clear()
            for model in list_nodes:
                for k in model:
                    self.lw_landmarks.addItem(f'{k},{model[k]}')
            for c in list_connections:
                self.lw_connections.addItem(f"{c['id']}, {c['start']}, {c['end']}")
            # self.iv_landmarks = ImageViewer(image_file="references/hand_landmarks.png")
            # self.layout_reference.addWidget(self.iv_landmarks)
            self.plot_detected_results('face',list_nodes, list_connections, width=img_m_width, height=img_m_height)
        else:
            QMessageBox.information(self, "Tip", "Failed to detect!")
            if self.iv_hand != None:
                self.layout_detection.removeWidget(self.iv_hand)
            self.lw_landmarks.clear()
            self.lw_connections.clear()

    def body_part_changed(self):
        body_part=self.cb_body_part.currentText()
        list_faces=self.dict_faces[body_part]
        self.cb_face.clear()
        for f in list_faces:
            self.cb_face.addItem(f)

    def browse_report_path(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Pick a folder")  # 起始路径
        print(directory)
        if directory == "":
            return
        self.edit_report_path.setText(directory)

    def read_infrared_data(self,file):
        lines = open(file, "r", encoding='utf-8')
        data = []
        for line in lines:
            vs = line.strip().split(",")
            row = [float(v) for v in vs]
            data.append(row)
        return data

    def find_temp(self,csv_matrix, image_x, image_y, image_width, image_height):
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
        return csv_matrix[c_y][c_x]

    def analyze(self):
        self.remove_plot_detected_reuslts()
        if not self.cb_analyze_file.isChecked():
            csv_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".csv"
            img_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".png"
            save_hand_path = self.edit_report_path.text() + "/" + self.cb_body_part.currentText() + "/" + self.cb_face.currentText() + ".detected.png"
        else:
            csv_path=self.edit_file_path.text()
            file,ext=os.path.splitext(csv_path)
            img_path=file+".png"
            save_hand_path=file+".detected.png"
            # generate png image
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            plt.rcParams['axes.unicode_minus'] = False  # 解决无法显示符号的问题
            sns.set(font='SimHei', font_scale=0.8, style="ticks")  # 解决Seaborn中文显示问题
            data = self.read_infrared_data(csv_path)
            ax = sns.heatmap(data,
                             xticklabels=False,  # remove the labels
                             yticklabels=False,
                             cbar=False
                             )
            plt.tight_layout()
            plt.savefig(img_path,dpi=300,bbox_inches='tight',   pad_inches = 0)

        self.show_original_image(csv_path)
        if self.iv_landmarks!=None:
            self.iv_landmarks.setImage("")
        img_matrix = read_infrared_data(csv_path)
        img_m_width = len(img_matrix[0])
        img_m_height = len(img_matrix)
        if self.cb_body_part.currentText() in ["hand","arm"]:
            # ================================== Hand Detection ===========================

            detected_hand,list_hand_model,list_hand_connection=detect_hand(image_path=img_path,save_detected_path=save_hand_path)
            if self.iv_hand!=None:
                self.layout_detection.removeWidget(self.iv_hand)
            if os.path.exists(save_hand_path):
                self.iv_hand = ImageViewer(image_file=save_hand_path)
                self.layout_detection.addWidget(self.iv_hand)
                # show 21 points and temperature
                self.lw_landmarks.clear()
                for model in list_hand_model:
                    self.lw_landmarks.addItem(str(model['id'])+f": ({model['x']},{model['y']}): "+str(model['temp']))
                for model in list_hand_connection:
                    self.lw_connections.addItem(f"{(model['id'])},{model['start']},{model['end']}")
                if self.iv_landmarks!=None:
                    self.iv_landmarks.setImage("references/hand_landmarks.png")
                else:
                    self.iv_landmarks = ImageViewer(image_file="references/hand_landmarks.png")
                    self.layout_reference.addWidget(self.iv_landmarks)
                self.plot_detected_results('hand',list_hand_model, list_hand_connection, width=img_m_width, height=img_m_height)
            else:
                QMessageBox.information(self,"Tip","Failed to detect!")
                if self.iv_hand != None:
                    self.layout_detection.removeWidget(self.iv_hand)
                self.lw_landmarks.clear()
                self.lw_connections.clear()
        elif self.cb_body_part.currentText() in ['head']:
            img, list_nodes, list_connections = detect_face_mesh(image_path=img_path,show=False,save_detected_path=save_hand_path)
            if list_nodes==None or len(list_nodes)==0:
                QMessageBox.information(self, "Tip", "Not Found!")
                return
            if self.iv_hand!=None:
                self.layout_detection.removeWidget(self.iv_hand)
            if os.path.exists(save_hand_path):
                self.iv_hand = ImageViewer(image_file=save_hand_path)
                self.layout_detection.addWidget(self.iv_hand)
                # show 21 points and temperature
                self.lw_landmarks.clear()
                self.lw_connections.clear()
                for model in list_nodes:
                    self.lw_landmarks.addItem(str(model['id'])+f": ({model['x']},{model['y']}): "+str(model['temp']))
                for c in list_connections:
                    self.lw_connections.addItem(f"{c['id']}, {c['start']}, {c['end']}")
                # self.iv_landmarks = ImageViewer(image_file="references/hand_landmarks.png")
                # self.layout_reference.addWidget(self.iv_landmarks)
                self.plot_detected_results('facemesh',list_nodes, list_connections, width=img_m_width,
                                           height=img_m_height)
            else:
                QMessageBox.information(self,"Tip","Failed to detect!")
                if self.iv_hand != None:
                    self.layout_detection.removeWidget(self.iv_hand)
                self.lw_landmarks.clear()
                self.lw_connections.clear()

        else:
            if self.iv_hand != None:
                self.layout_detection.removeWidget(self.iv_hand)
            if self.iv_landmarks != None:
                self.iv_landmarks.setImage("")
            self.iv_hand=None
            self.layout_detection.update()

            self.lw_landmarks.clear()
            self.lw_connections.clear()
            QMessageBox.information(self, "Tip", "Not Implemented!")

def main():
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    r = app.exec_()
    print(r)

if __name__ == "__main__":
    main()

