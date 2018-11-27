# pylint: disable=E1101
import cv2
import numpy as np

class Efx:
    def __init__(self,path):
        self.imgSrc = cv2.imread(path)

    def gaussianBlur(self):
        return cv2.GaussianBlur(self.imgSrc,(5,5),0)

    def filter_brightnes_contrast(self,brightness,contrast):
        """g(x) = contrast*f(x) + brightness"""
        return cv2.addWeighted(self.imgSrc,contrast,np.zeros(self.imgSrc.shape,self.imgSrc.dtype),0,brightness)
