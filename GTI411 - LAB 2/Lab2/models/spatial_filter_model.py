import cv2
import numpy as np


class SpatialFilterModel:
    def __init__(self) -> None:
        self.source_image = None
        self.range_method = "Clamp 0 ... 255"
        self.filtering_method = "Mean"
        self.handling_border_method = "0"
        self.kernel_size = 0

    def update_kernel_size(self, value: int):
        try:
            k_size = int(value)
            if k_size % 2 == 1 and k_size > 0:
                self.kernel_size = k_size
            else:
                raise ValueError("Invalid kernel value, 3 assigned")
        except ValueError:
            self.kernel_size = 3

    def update_range_method(self, mtd: str):
        self.range_method = mtd

    def update_filtering_method(self, mtd: str):
        self.filtering_method = mtd

    def update_handling_border_method(self, mtd: str):
        self.handling_border_method = mtd

    def apply_filter(self):
        try:
            if self.source_image is None:
                return None

            img = self.source_image.copy()
            k_size = self.kernel_size
            if k_size % 2 == 0:
                k_size += 1

            if self.handling_border_method == "0":
                border_type = cv2.BORDER_CONSTANT
            elif self.handling_border_method == "none":
                border_type = cv2.BORDER_ISOLATED
            elif self.handling_border_method == "copy":
                border_type = cv2.BORDER_REPLICATE
            elif self.handling_border_method == "mirror":
                border_type = cv2.BORDER_REFLECT
            elif self.handling_border_method == "circular":
                border_type = cv2.BORDER_WRAP
            else:
                border_type = cv2.BORDER_DEFAULT

            if self.filtering_method == "Mean":
                img = cv2.blur(img, (k_size, k_size), borderType=border_type)
            elif self.filtering_method == "Gaussian":
                img = cv2.GaussianBlur(img, (k_size, k_size), 0, borderType=border_type)
            elif self.filtering_method.strip() == "Median":
                img = cv2.medianBlur(img, k_size)
            elif self.filtering_method == "Sobel x-axis":
                grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0)
                img = cv2.convertScaleAbs(grad_x)
            elif self.filtering_method == "Sobel y-axis":
                grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1)
                img = cv2.convertScaleAbs(grad_y)
            elif self.filtering_method == "Sobel":
                grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, borderType=border_type)
                grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, borderType=border_type)
                grad_xy = cv2.magnitude(grad_x, grad_y)
                img = cv2.convertScaleAbs(grad_xy)

            print(f"Applying with {self.filtering_method}")
            print(f"Applying with {self.kernel_size}")
            print(f"Applying with {self.range_method}")
            print(f"Applying with {self.handling_border_method}")

            img = img.astype(np.uint8)
            return img
        except Exception:
            return None

