# Blur Detection using Fourier Transform
This repo shows the use of Fast Fourier Transform (FFT) to perform blur detection in images.

## The Design Pipeline is as follows:
* Finding the center of image.
* Compute the FFT to find the frequency transform.
* shift the zero frequency component (DC component) located at the top-left corner to the center by using fftshift().
* Zero-out the all the pixels in the neighbourhood of the DC component by setting it to 0.
* Shifting the DC component back to top-left portion of spectrum by using inverse fft shift.
* Retransforming the spectrum from frequency domain to time domain by using inverse fourier transform.
* Compute the magnitude spectrum of the reconstructed image.
* Find the mean of the magnitude values.
* Set the blur condition by evaluating whether the mean value of the magnitude is less than the threshold value.
* Applying blur detector on the test image to detect whether it is blurry or not.

![Blurry Image](Output/Output_Blurry.png?raw=true)

![Blurry Image](Output/Output_Non_Blurry.png?raw=true)

