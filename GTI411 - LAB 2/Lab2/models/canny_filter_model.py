import cv2
import numpy as np


def create_fake_image(image, text:str):
    fake_image = np.zeros_like(image, dtype=np.uint8)
    height = image.shape[0]

    font_size = 1
    color = (0, 255, 0)
    font_weight = 2

    fake_image = cv2.putText(fake_image, text, (20, round(height//2)), cv2.FONT_HERSHEY_SIMPLEX, font_size, color, font_weight)

    return fake_image


class CannyFilterModel:
    def __init__(self) -> None:
        self.source_image = None
        self.gaussian_filter_size = 3
        self.min_threshold = 130
        self.max_threshold = 130

    def update_min_threshold(self, value: int):
        try:
            self.min_threshold = max(0, min(int(value), 255))
        except ValueError:
            self.min_threshold = 130

    def update_max_threshold(self, value: int):
        try:
            self.max_threshold = max(0, min(int(value), 255))
        except ValueError:
            self.max_threshold = 150

    def update_gaussian_filter_size(self, value: int):
        try:
            k_size = int(value)
            if k_size % 2 == 1 and k_size > 0:
                self.gaussian_filter_size = k_size
            else:
                raise ValueError("Invalid kernel value, 3 assigned")
        except ValueError:
            self.gaussian_filter_size = 3

    def grey_to_rgb(self, image):
        if len(image.shape) == 2:
            display_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            display_image = image
        return display_image

    def apply_filter(self):
        if self.source_image is None:
            raise ValueError("No source image provided.")

        if len(self.source_image.shape) == 3:
            gray_image = cv2.cvtColor(self.source_image, cv2.COLOR_BGR2GRAY)
        else:
            gray_image = self.source_image

        smoothed_image = cv2.GaussianBlur(
            gray_image,
            (self.gaussian_filter_size, self.gaussian_filter_size),
            0
        )

        grad_x = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=3)
        grad_y = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=3)

        magnitude = np.sqrt(grad_x ** 2 + grad_y ** 2)
        direction = np.arctan2(grad_y, grad_x) * (180.0 / np.pi)
        direction = np.where(direction < 0, direction + 180, direction)
        locmax_image = np.zeros_like(magnitude, dtype=np.uint8)

        for i in range(1, magnitude.shape[0] - 1):
            for j in range(1, magnitude.shape[1] - 1):
                angle = direction[i, j]
                if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                    q = magnitude[i, j + 1]
                    r = magnitude[i, j - 1]
                elif 22.5 <= angle < 67.5:
                    q = magnitude[i + 1, j - 1]
                    r = magnitude[i - 1, j + 1]
                elif 67.5 <= angle < 112.5:
                    q = magnitude[i + 1, j]
                    r = magnitude[i - 1, j]
                else:
                    q = magnitude[i - 1, j - 1]
                    r = magnitude[i + 1, j + 1]
                if magnitude[i, j] >= q and magnitude[i, j] >= r:
                    locmax_image[i, j] = magnitude[i, j]
                else:
                    locmax_image[i, j] = 0

        threshold_mask = np.zeros_like(magnitude, dtype=np.uint8)
        threshold_mask[magnitude >= self.max_threshold] = 255
        threshold_mask[
            (magnitude >= self.min_threshold) & (magnitude < self.max_threshold)
            ] = 128
        final_image = np.zeros_like(threshold_mask)

        for i in range(1, threshold_mask.shape[0] - 1):
            for j in range(1, threshold_mask.shape[1] - 1):
                val = threshold_mask[i, j]
                if val == 128:
                    if (
                            threshold_mask[i - 1, j] == 255
                            or threshold_mask[i + 1, j] == 255
                            or threshold_mask[i, j - 1] == 255
                            or threshold_mask[i, j + 1] == 255
                            or threshold_mask[i - 1, j - 1] == 255
                            or threshold_mask[i + 1, j - 1] == 255
                            or threshold_mask[i - 1, j + 1] == 255
                            or threshold_mask[i + 1, j + 1] == 255
                    ):
                        final_image[i, j] = 255
                elif val == 255:
                    final_image[i, j] = 255

        final_image = final_image.astype(np.uint8)
        smoothed_image = self.grey_to_rgb(smoothed_image)
        grad_x = self.grey_to_rgb(np.uint8(np.absolute(grad_x)))
        grad_y = self.grey_to_rgb(np.uint8(np.absolute(grad_y)))
        locmax_image = self.grey_to_rgb(locmax_image)
        final_image = self.grey_to_rgb(final_image)

        images = {
            'smoothed': smoothed_image,
            'gradient_x': grad_x,
            'gradient_y': grad_y,
            'local_maxima': locmax_image,
            'final': final_image,
        }
        return images