import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from Lab2.Lab2_Window import Ui_Lab2_Window
from Lab2.models import SpatialFilterModel, CannyFilterModel, FrequencyFilterModel
from Lab2.events import event_manager



class Lab2Controller:
    def __init__(self) -> None:
        self.spatial_model = SpatialFilterModel()
        self.canny_model = CannyFilterModel()
        self.freq_model = FrequencyFilterModel()

        event_manager.register("on_load_image", self.load_image)

        # Partie1 events
        event_manager.register("on_filter_method_changed", self.spatial_model.update_filtering_method)
        event_manager.register("on_range_method_changed", self.spatial_model.update_filtering_method)
        event_manager.register("on_border_method_changed", self.spatial_model.update_handling_border_method)
        event_manager.register("on_kernel_size_changed", self.spatial_model.update_kernel_size)
        event_manager.register("on_apply_spatial_filter", self.apply_spatial_filter)

        # Partie2 events
        event_manager.register("on_gaussian_filter_size_changed", self.canny_model.update_gaussian_filter_size)
        event_manager.register("on_min_canny_threshold_changed", self.canny_model.update_min_threshold)
        event_manager.register("on_max_canny_threshold_changed", self.canny_model.update_max_threshold)
        event_manager.register("on_apply_canny_filter", self.apply_canny_filter)


        # Partie3 events
        event_manager.register("on_update_n_butterworth", self.freq_model.update_n_params_butter)
        event_manager.register("on_update_cutoff_frequency", self.freq_model.update_cutoff)

        event_manager.register("on_apply_ideal_lowpass_filter", lambda: self.apply_freq_filter("lowpass_ideal"))
        event_manager.register("on_apply_ideal_highpass_filter", lambda: self.apply_freq_filter("highpass_ideal"))
        event_manager.register("on_apply_butter_lowpass_filter", lambda: self.apply_freq_filter("lowpass_butter"))
        event_manager.register("on_apply_butter_highpass_filter", lambda: self.apply_freq_filter("highpass_butter"))


        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Lab2_Window()
        self.ui.setupUi(self.window)

        self.window.show()

    
    def apply_freq_filter(self, filter_mtd:str):
        methods = {
            'lowpass_ideal': self.freq_model.apply_ideal_lowpass_filter,
            'highpass_ideal': self.freq_model.apply_ideal_highpass_filter,
            'lowpass_butter': self.freq_model.apply_butterworth_lowpass_filter,
            'highpass_butter': self.freq_model.apply_butterworth_highpass_filter,
        }

        if filter_mtd not in methods:
            print(f"Erro {filter_mtd}")
            return
        
        results = methods[filter_mtd]()

        if results is None:
            return

        for key, image in results.items():
            event_manager.trigger("on_freq_image_result", key, image)     
        


    def apply_canny_filter(self):
        results = self.canny_model.apply_filter()
        if results is None:
            return
        
        for key, image in results.items():
            event_manager.trigger("on_canny_image_result", key, image)
        

    def apply_spatial_filter(self):
        result_image = self.spatial_model.apply_filter()
        if result_image is not None:
            event_manager.trigger("on_spatial_filter_result", result_image)


    def load_image(self, filename:str):
        image = cv2.imread(filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        self.spatial_model.source_image = image
        self.canny_model.source_image = image
        self.freq_model.source_image = image


    