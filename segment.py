from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
from skimage import data
import numpy as np
import matplotlib.pyplot as plt


#GUI for the Image Segmentation

class Img_Proc_Gui(QWidget):
    def __init__(self, parent=None):
        super(Img_Proc_Gui, self).__init__(parent)
        self.img_processed = False
        btn_process_img = QPushButton("Process Image")
        #calling for INPUT

        btn_process_img.clicked.connect(self.getInput)

        #Quit Button Widget

        btn_quit = QPushButton("Quit")
        btn_quit.clicked.connect(self.quit_clicked)
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_process_img)
        hbox_btn.addWidget(btn_quit)

        #Image Address Box
        hbox_address = QHBoxLayout()
        self.address = QLineEdit()
        hbox_address.addWidget(self.address)
        btn_img_explorer = QPushButton('Open Image')
        hbox_address.addWidget(btn_img_explorer)

        btn_img_explorer.clicked.connect(self.open)

        #Threshold Input Box
        hbox_size = QHBoxLayout()
        label_threshold = QLabel('Threshold :')
        self.et_threshold = QLineEdit()
        hbox_size.addWidget(label_threshold)
        hbox_size.addWidget(self.et_threshold)
        
        #Combined all the Widgets
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_address)
        vbox.addLayout(hbox_size)
        vbox.addLayout(hbox_btn)


        self.setGeometry(400,300,400,200)
        self.setWindowTitle('Image Processing')
        self.setLayout(vbox)

  
    def quit_clicked(self):
        
        cv2.destroyAllWindows()
        self.close()

  
    def open(self):
        fileName = QFileDialog.getOpenFileName(self,'openFile')
        self.address.setText(fileName[0])
        
       

  
    def getInput(self):
        
        self.req_threshold = self.et_threshold.text()
        if self.req_threshold != '':
            self.ready = True
            self.img_processed = True
        else:
            self.ready =  False
        self.ready = True
        if self.ready is False :
            QMessageBox.about(self,'Error','Fill parameters to process')
        if self.address.text() == '':
            QMessageBox.about(self,'Error','Select Image to process')
        else:
            self.req_img = self.process_img(cv2.imread(self.address.text()))
            #cv2.imshow("req_img",self.req_img)

     

    def process_img(self,imgtoproc):


            imgtoproc = cv2.resize(imgtoproc, (512, 512))  
            
            #Region of Interest to segment out
            r = cv2.selectROI(imgtoproc)       
            imgtoproc = cv2.cvtColor(imgtoproc,cv2.COLOR_BGR2RGB)

            
            roi = imgtoproc[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            roi = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)

            #Conversion of data type for mathematical computation

            img_float=imgtoproc.astype('float64')
            roi_float = roi.astype('float64')
            
            #Red Channel Process
            red_channel=img_float[:,:,0]
            red_mean=roi_float[:,:,0].mean()

            #Green Channel Process
            green_channel=img_float[:,:,1]
            green_mean=roi_float[:,:,1].mean()

            #Blue Channel Process
            blue_channel=img_float[:,:,2]
            blue_mean=roi_float[:,:,2].mean()

            #Matrix of mean for easy computation
            val_r=np.ones((512,512),dtype=np.float64) *red_mean
            val_g=np.ones((512,512),dtype=np.float64)*green_mean
            val_b=np.ones((512,512),dtype=np.float64)*blue_mean

            #calculation of Euclidean Distance
            red=np.power((red_channel-val_r),2)
            green=np.power((green_channel-val_g),2)
            blue=np.power((blue_channel-val_b),2)
            D=np.sqrt(red+green+blue)
            
            D_new=(D).astype('uint8')   #Converting the datatype back to uint8
            
           
            #Threshold
            # print(np.unique(D_new))
           
            D_new[D_new<=int(self.req_threshold)]=1
            D_new[D_new>int(self.req_threshold)]=0
           
    
            #Image Plotting

            ax=[]
            fig=plt.figure(figsize=(10,5))
            ax.append(fig.add_subplot(1,2,1))
            ax[-1].set_title("Original Image:")
            plt.imshow(imgtoproc,cmap='gray')
            ax.append(fig.add_subplot(1,2,2))
            ax[-1].set_title("Segmented Image:")
            (plt.imshow(D_new,cmap='gray'))

            
                   
            return plt.show()

#Main Driver
if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Img_Proc_Gui()
    screen.show()
    sys.exit(app.exec_())