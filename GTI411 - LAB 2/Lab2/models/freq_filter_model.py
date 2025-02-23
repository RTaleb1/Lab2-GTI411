import cv2
import numpy as np


def create_fake_image(image, text: str):
    fake_image = np.zeros_like(image, dtype=np.uint8)
    height = image.shape[0]

    font_size = 1
    color = (0, 255, 0)
    font_weight = 2
    fake_image = cv2.putText(fake_image, text, (20, round(height // 2)), cv2.FONT_HERSHEY_SIMPLEX, font_size, color,
                             font_weight)

    return fake_image


class FrequencyFilterModel:
    def __init__(self) -> None:
        self.source_image = None
        self.cutoff_freq: int = 0
        self.n_params_butter: int = 0

    def update_cutoff(self, value: int):
        try:
            self.cutoff_freq = int(value)
        except ValueError:
            self.cutoff_freq = 25

    def update_n_params_butter(self, value: int):
        try:
            self.butter_params = int(value)
        except ValueError:
            self.butter_params = 25

    def initialiser_image(self):
        try:
            if self.source_image is None:
                return None
            else:
                return cv2.split(self.source_image)
        except Exception:
            return None

    def transformer_fourier(self, channel):
        f = np.fft.fft2(channel)
        F = np.fft.fftshift(f)
        original_spectrum = np.log1p(np.abs(F))
        normalized_spectrum = np.uint8(255 * original_spectrum / np.max(original_spectrum))
        return F, normalized_spectrum

    def fourier_inverse(self, G_shift):
        G = np.fft.ifftshift(G_shift)
        img_back = np.abs(np.fft.ifft2(G))
        normalized_image = np.uint8(cv2.normalize(img_back, None, 0, 255, cv2.NORM_MINMAX))
        return normalized_image

    def apply_ideal_lowpass_filter(self):
        try:
            channels = self.initialiser_image()
            if channels is None:
                return None
            filtered_channels = []
            original_spectra = []
            filter_spectra = []
            M, N = channels[0].shape
            M_center, N_center = M // 2, N // 2
            H = np.zeros((M, N), np.float32)
            for u in range(M):
                for v in range(N):
                    D = np.sqrt((u - M_center) ** 2 + (v - N_center) ** 2)
                    if D <= self.cutoff_freq:
                        H[u, v] = 1
                    else:
                        H[u, v] = 0

            for c in channels:
                F, og_spectrum = self.transformer_fourier(c)
                original_spectra.append(og_spectrum)
                G_shift = F * H
                ideal_spectrum = np.log1p(np.abs(G_shift))
                filter_spectra.append(np.uint8(255 * ideal_spectrum / np.max(ideal_spectrum)))
                filtered_channel = self.fourier_inverse(G_shift)
                filtered_channels.append(filtered_channel)

            merged_filtered = cv2.merge(filtered_channels)
            merged_original_spectrum = cv2.merge(original_spectra)
            merged_filter_spectrum = cv2.merge(filter_spectra)

            return {
                'original_spectrum': merged_original_spectrum,
                'ideal_spectrum': merged_filter_spectrum,
                'ideal_recons': merged_filtered,
            }
        except Exception:
            return None

    def apply_ideal_highpass_filter(self):
        try:
            channels = self.initialiser_image()
            if channels is None:
                return None
            filtered_channels = []
            original_spectra = []
            filter_spectra = []
            M, N = channels[0].shape
            M_center, N_center = M // 2, N // 2
            H = np.ones((M, N), np.float32)
            for u in range(M):
                for v in range(N):
                    D = np.sqrt((u - M_center) ** 2 + (v - N_center) ** 2)
                    if D <= self.cutoff_freq:
                        H[u, v] = 0
                    else:
                        H[u, v] = 1

            for c in channels:
                F, og_spectrum = self.transformer_fourier(c)
                original_spectra.append(og_spectrum)
                G_shift = F * H
                filtered_spectrum = np.log1p(np.abs(G_shift))
                filter_spectra.append(np.uint8(255 * filtered_spectrum / np.max(filtered_spectrum)))
                filtered_channel = self.fourier_inverse(G_shift)
                filtered_channels.append(filtered_channel)

            merged_filtered = cv2.merge(filtered_channels)
            merged_original_spectrum = cv2.merge(original_spectra)
            merged_filter_spectrum = cv2.merge(filter_spectra)

            return {
                'original_spectrum': merged_original_spectrum,
                'ideal_spectrum': merged_filter_spectrum,
                'ideal_recons': merged_filtered,
            }
        except Exception:
            return None

    def apply_butterworth_lowpass_filter(self):
        try:
            channels = self.initialiser_image()
            if channels is None:
                return None
            filtered_channels = []
            original_spectra = []
            filter_spectra = []
            M, N = channels[0].shape
            M_center, N_center = M // 2, N // 2
            H = np.zeros((M, N), dtype=np.float32)
            for u in range(M):
                for v in range(N):
                    D = np.sqrt((u - M_center) ** 2 + (v - N_center) ** 2)
                    H[u, v] = 1 / (1 + (D / self.cutoff_freq) ** (2 * self.butter_params))

            for c in channels:
                F, og_spectrum = self.transformer_fourier(c)
                original_spectra.append(og_spectrum)
                G_shift = F * H
                filtered_spectrum = np.log1p(np.abs(G_shift))
                filter_spectra.append(np.uint8(255 * filtered_spectrum / np.max(filtered_spectrum)))
                filtered_channel = self.fourier_inverse(G_shift)
                filtered_channels.append(filtered_channel)

            merged_filtered = cv2.merge(filtered_channels)
            merged_original_spectrum = cv2.merge(original_spectra)
            merged_filter_spectrum = cv2.merge(filter_spectra)

            return {
                'original_spectrum': merged_original_spectrum,
                'butter_spectrum': merged_filter_spectrum,
                'butter_recons': merged_filtered,
            }
        except Exception:
            return None

    def apply_butterworth_highpass_filter(self):
        try:
            channels = self.initialiser_image()
            if channels is None:
                return None
            filtered_channels = []
            original_spectra = []
            filter_spectra = []
            M, N = channels[0].shape
            M_center, N_center = M // 2, N // 2
            H = np.zeros((M, N), dtype=np.float32)
            for u in range(M):
                for v in range(N):
                    D = np.sqrt((u - M_center) ** 2 + (v - N_center) ** 2)
                    if D != 0:
                        H[u, v] = 1 / (1 + (self.cutoff_freq / D) ** (2 * self.butter_params))
                    else:
                        H[u, v] = 0

            for c in channels:
                F, og_spectrum = self.transformer_fourier(c)
                original_spectra.append(og_spectrum)
                G_shift = F * H
                filtered_spectrum = np.log1p(np.abs(G_shift))
                filter_spectra.append(np.uint8(255 * filtered_spectrum / np.max(filtered_spectrum)))
                filtered_channel = self.fourier_inverse(G_shift)
                filtered_channels.append(filtered_channel)

            merged_filtered = cv2.merge(filtered_channels)
            merged_original_spectrum = cv2.merge(original_spectra)
            merged_filter_spectrum = cv2.merge(filter_spectra)

            return {
                'original_spectrum': merged_original_spectrum,
                'butter_spectrum': merged_filter_spectrum,
                'butter_recons': merged_filtered,
            }
        except Exception:
            return None