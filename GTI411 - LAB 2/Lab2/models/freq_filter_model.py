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


class FrequencyFilterModel:
    def __init__(self) -> None:
        self.source_image = None
        self.cutoff_freq:int = 0
        self.n_params_butter:int = 0


    def update_cutoff(self, value:int):
        self.cutoff_freq = value
        

    def update_n_params_butter(self, value:int):
        self.n_params_butter = value

    
    def apply_ideal_lowpass_filter(self):
        if self.source_image is None:
            return None
        image = self.source_image.copy()

        print(f"Applying with ideal lowpass with:  {self.cutoff_freq}")

        original_image_spectrum = create_fake_image(image, "Orig spectrum")
        ideal_filter_spectrum = create_fake_image(image, "Ideal spectrum") 
        ideal_filter_recons = create_fake_image(image, "Ideal recons") 

        images = {
            'original_spectrum': original_image_spectrum,
            'ideal_spectrum': ideal_filter_spectrum,
            'ideal_recons': ideal_filter_recons,
        }
        return images
    

    def apply_ideal_highpass_filter(self):
        if self.source_image is None:
            return None
        image = self.source_image.copy()

        print(f"Applying with ideal highpass with: {self.cutoff_freq}")

        original_image_spectrum = create_fake_image(image, "Orig spectrum")
        ideal_filter_spectrum = create_fake_image(image, "Ideal spectrum") 
        ideal_filter_recons = create_fake_image(image, "Ideal recons") 

        images = {
            'original_spectrum': original_image_spectrum,
            'ideal_spectrum': ideal_filter_spectrum,
            'ideal_recons': ideal_filter_recons,
        }
        return images

        
    def apply_butterworth_lowpass_filter(self):
        if self.source_image is None:
            return None
        image = self.source_image.copy()

        print(f"Applying with Butter lowpass with: {self.n_params_butter}")

        original_image_spectrum = create_fake_image(image, "Orig spectrum")
        butter_filter_spectrum = create_fake_image(image, "Butter spectrum") 
        butter_filter_recons = create_fake_image(image, "Butter recons") 

        images = {
            'original_spectrum': original_image_spectrum,
            'butter_spectrum': butter_filter_spectrum,
            'butter_recons': butter_filter_recons,
        }
        return images
    

    def apply_butterworth_highpass_filter(self):
        if self.source_image is None:
            return None
        image = self.source_image.copy()

        print(f"Applying with Butter highpass with: {self.n_params_butter}")

        original_image_spectrum = create_fake_image(image, "Orig spectrum")
        butter_filter_spectrum = create_fake_image(image, "Butter spectrum") 
        butter_filter_recons = create_fake_image(image, "Butter recons") 

        images = {
            'original_spectrum': original_image_spectrum,
            'butter_spectrum': butter_filter_spectrum,
            'butter_recons': butter_filter_recons,
        }
        return images