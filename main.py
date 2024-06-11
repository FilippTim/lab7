import cv2
import sys
from window import ImageWindow
import numpy as np
from PyQt6.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QLineEdit, QLabel, QHBoxLayout, QWidget

save_process_path='stuff/saved/save_proc.jpg'
class Mywindow(ImageWindow):
    def __init__(self):
        super().__init__()
        self.initial_path=''
        self.centerx=50
        self.centery=50
        self.angle=-90
        self.original_image=None
    #Кнопки
    def on_button1_clicked(self):
        self.img_hide()
        self.download_img(1)
        self.slider_a.show()
    def on_button_findh_clicked(self):
        self.slider_a.hide()
        self.find_features()
    def on_button_track_clicked(self):
        self.slider_a.hide()
        self.track_features()
    def on_button_compare_clicked(self):
        self.slider_a.hide()
    def onChanged_a(self, value):
        self.angle=value
        self.labela.setText(str(value))
        self.rotate()


    def download_img(self, i):
        try:
            self.initial_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "", "Изображения (*.png *.jpg *.jpeg)")
            if not self.initial_path:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            if i==1:
                self.update_images1(self.initial_path)
            else:
                raise FileNotFoundError("Куда ты хочешь картинку?")
        except Exception as e:
            print("Ошибка при загрузке изображения", e)
            return None
        
    def loadcv2(self, ini):
        try:
            if not ini:
                raise FileNotFoundError("Путь к изображению не был выбран.")
            img = cv2.imread(ini)
            return img
        except Exception as e:
            print("Ошибка при выполнении операции: ", e)
            return None

    def saved_and_print_process(self, img):
        cv2.imwrite(save_process_path, img)
        self.update_images2(save_process_path)

    def rotate(self):
        try:
            img = self.loadcv2(self.initial_path)
            rows, cols = img.shape[:2]
            #M = cv2.getRotationMatrix2D((self.centery,self.centerx), self.angle, 1)
            M = cv2.getRotationMatrix2D((rows//2,cols//2), self.angle, 1)
            img = cv2.warpAffine(img, M, (cols, rows), flags=cv2.INTER_LINEAR)
            self.saved_and_print_process(img)
        except Exception as e:
            print("Ошибка при rotate: ", e)
            return None
    def find_features(self):
        self.original_image = self.loadcv2(save_process_path)
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.keypoints = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
        self.keypoints = [cv2.KeyPoint(x[0][0], x[0][1], 1) for x in self.keypoints]
        self.keypoints_image = cv2.drawKeypoints(self.original_image, self.keypoints, None, color=(0, 255, 0))
        cv2.imwrite(save_process_path, self.keypoints_image)
        self.update_images3(save_process_path)

    def track_features(self):
        if self.original_image is None:
            return
        if self.keypoints is None:
            self.find_features()
        
        old_gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        new_image = cv2.imread(self.initial_path)
        new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        p0 = np.array([point.pt for point in self.keypoints], dtype=np.float32)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, p0, None)

        # Добавляем отладочный вывод для проверки размерности st
        print("Размерность st:", st.shape)

        good_indices = np.where(st==1)[0]  # Находим индексы хороших точек
        good_new = p1[good_indices]  # Выбираем хорошие новые точки
        good_old = p0[good_indices]  # Выбираем соответствующие старые точки
            
        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel()
            c, d = old.ravel()
            cv2.circle(new_image, (int(a), int(b)), 5, (0, 255, 0), -1)
            cv2.line(new_image, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
            
        cv2.imwrite(save_process_path, new_image)
        self.update_images3(save_process_path)
    def match_features(self):
        if self.original_image is None:
            return

        new_image = cv2.imread(self.initial_path)
        gray1 = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(gray1, None)
        kp2, des2 = orb.detectAndCompute(gray2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        matching_result = cv2.drawMatches(self.original_image, kp1, new_image, kp2, matches[:10], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        self.display_image(matching_result, self.processed_label)
        cv2.imwrite(save_process_path, matching_result)
        self.update_images3(save_process_path)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mywindow()
    sys.exit(app.exec())
