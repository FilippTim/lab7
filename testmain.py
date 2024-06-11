import cv2
import numpy as np

class ImageProcessor:
    def __init__(self, initial_path):
        self.initial_path = initial_path
        self.points = []
        self.dest_points = []
        self.image = None
        self.clone = None

    def load_image(self):
        self.image = cv2.imread(self.initial_path)
        self.clone = self.image.copy()

    def select_points(self):
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", self.click_event)
        
        while True:
            cv2.imshow("image", self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or len(self.points) == 4:  # Esc key to stop or 4 points selected
                break

        cv2.destroyAllWindows()

    def click_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(self.points) < 4:
                cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)
                self.points.append((x, y))
                print(f"Point selected: {x}, {y}")

    def set_dest_points(self, dest_points):
        if len(dest_points) != 4:
            raise ValueError("Four destination points are required.")
        self.dest_points = dest_points

    def project_fragment(self):
        if len(self.points) != 4 or len(self.dest_points) != 4:
            raise ValueError("Four source and destination points are required.")

        pts_src = np.array(self.points, dtype='float32')
        pts_dst = np.array(self.dest_points, dtype='float32')

        # Compute the homography matrix
        h_matrix, status = cv2.findHomography(pts_src, pts_dst)

        # Warp the source image to the destination based on the homography
        height, width = self.clone.shape[:2]
        warped_image = cv2.warpPerspective(self.clone, h_matrix, (width, height))

        # Display the result
        cv2.imshow("Warped Image", warped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save_image(self, path):
        cv2.imwrite(path, self.clone)

# Пример использования
processor = ImageProcessor("path/to/image.jpg")
processor.load_image()
print("Select 4 points on the image")
processor.select_points()
print("Points selected:", processor.points)

# Укажите 4 точки на произвольной плоскости (пример)
dest_points = [(100, 100), (400, 100), (400, 400), (100, 400)]
processor.set_dest_points(dest_points)

processor.project_fragment()
processor.save_image("C:\opencv\lab3\stuff\images\kot1.jpg")