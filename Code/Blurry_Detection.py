# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:13:05 2021

@author: Sonu
"""

import matplotlib.pyplot as plt
import numpy as np
import cv2

#Function to detect whether image is blurry or not using fourier transorm
def detect_blur_fft(image, radius=60, thresh=20, vis=False):
    print(image.shape)
    (h, w) = image.shape
    
    #Finding the center of image
    (cX, cY) = (int(w / 2.0), int(h / 2.0))
    
    #Finding the fast fourier transform of the image & shifting the DC component from top-left to center of spectrum
    fft = np.fft.fft2(image)
    fftShift = np.fft.fftshift(fft)
    
    #Check to see if we are visualizing our output
    if vis:
        #Computing the magnitude spectrum of the transform
        magnitude = 20 * np.log(np.abs(fftShift))
        
        #Displaying the original input image
        (fig, ax) = plt.subplots(1, 2, )
        ax[0].imshow(image, cmap="gray")
        ax[0].set_title("Input")
        ax[0].set_xticks([])
        ax[0].set_yticks([])
        
        #Displaying the magnitude image
        ax[1].imshow(magnitude, cmap="gray")
        ax[1].set_title("Magnitude Spectrum")
        ax[1].set_xticks([])
        ax[1].set_yticks([])
        
        plt.show()
    #Zero-out the all the pixels in the neighbourhood of the DC component by setting it to 0.
    #Neighbourhood size is given by radius.
    fftShift[cY - radius:cY + radius, cX - radius:cX + radius] = 0
    
    #Shifting the DC component back to top-left portion of spectrum and retransforming the spectrum from frequency domain to time domain
    fftShift = np.fft.ifftshift(fftShift)
    recon = np.fft.ifft2(fftShift)
    
    #Computing the magnitude spectrum of the reconstructed image,then compute the mean of the magnitude values
    magnitude = 20 * np.log(np.abs(recon))
    mean = np.mean(magnitude)
    #
    #Image will be considered "blurry" if the mean value of the magnitudes is less than the threshold value
    flag = mean<=thresh 
    return (mean, flag)

orig1 = cv2.imread('non_blurred.jpg',0)
orig2 = cv2.imread('blurred.jpg',0) 
img = [orig1, orig2]

for gray in img:
    #Applying blur detector using the FFT. Detecting whether the image is blurry or not.
    (mean, blurry) = detect_blur_fft(gray)

    image = np.dstack([gray] * 3)
    color = (0, 0, 255) if blurry else (0, 255, 0)
    text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
    text = text.format(mean)
    cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    print("[INFO] {}".format(text))
    
    #Showing the output image
    cv2.imshow("Output", image)
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

