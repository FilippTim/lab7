from PyQt6.QtWidgets import QComboBox, QSlider, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Изображения")
        self.setGeometry(50, 50, 400, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        
        self.image_layout = QVBoxLayout()
        self.layout.addLayout(self.image_layout)

     
        self.image_label1 = QLabel()
        self.label1_title = QLabel('До обработки')
        self.image_label2 = QLabel()
        self.label2_title = QLabel('Повернутое изображение')
        self.image_label3 = QLabel()
        self.label3_title = QLabel('Обработанное изображение')


        
        self.image_layout.addWidget(self.label1_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label1, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.label2_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.label3_title, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label3, alignment=Qt.AlignmentFlag.AlignCenter)

       
        self.button_layout = QVBoxLayout()
        self.layout.addLayout(self.button_layout)
        self.update_button()

        self.label1_title.hide()
        self.image_label1.hide()
        self.label2_title.hide()
        self.image_label2.hide()
        self.label3_title.hide()
        self.image_label3.hide()
        self.show() 

    def update_images1(self, image_path1):
        self.label1_title.show()
        pixmap1 = QPixmap(image_path1)

        
        scaled_pixmap1 = pixmap1.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)

        
        self.image_label1.setPixmap(scaled_pixmap1)
        self.image_label1.show()
        
        self.update()
    def img_hide(self):
        self.label1_title.hide()
        self.image_label1.hide()
        
    def update_images2(self, image_path2):
        self.label2_title.show()
        
        pixmap2 = QPixmap(image_path2)

        
        scaled_pixmap2 = pixmap2.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio)

        
        self.image_label2.setPixmap(scaled_pixmap2)
        self.image_label2.show()
        
        self.update()
    def update_images3(self, image_path3):
        self.label3_title.show()
        
        pixmap3 = QPixmap(image_path3)

        
        scaled_pixmap3 = pixmap3.scaled(200,200, Qt.AspectRatioMode.KeepAspectRatio)

        
        self.image_label3.setPixmap(scaled_pixmap3)
        self.image_label3.show()
        
        self.update()

    
    def update_button(self):
        self.button1 = QPushButton("Выбрать изображение")
        self.button1.clicked.connect(self.on_button1_clicked)
        self.button_layout.addWidget(self.button1)

        
        self.button_findh= QPushButton("Найти особенности")
        self.button_findh.clicked.connect(self.on_button_findh_clicked)
        self.button_layout.addWidget(self.button_findh)

        self.button_track= QPushButton("Отследить особенности")
        self.button_track.clicked.connect(self.on_button_track_clicked)
        self.button_layout.addWidget(self.button_track)

        self.button_compare= QPushButton("Сопоставить особенности")
        self.button_compare.clicked.connect(self.on_button_compare_clicked)
        self.button_layout.addWidget(self.button_compare)

        #Ползунок на angle
        self.labela_title = QLabel('Угол')
        self.button_layout.addWidget(self.labela_title)
        self.labela_title.hide()

        self.labela = QLabel('0', self)
        self.labela.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_layout.addWidget(self.labela)
        self.labela.hide()

        self.slider_a = QSlider(Qt.Orientation.Horizontal, self)
        self.slider_a.setMinimum(-180)
        self.slider_a.setMaximum(180)
        self.slider_a.setValue(0)
        self.slider_a.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider_a.setTickInterval(1)
        self.slider_a.valueChanged.connect(self.onChanged_a)
        self.button_layout.addWidget(self.slider_a)
        self.slider_a.hide()
    





        
 

 




