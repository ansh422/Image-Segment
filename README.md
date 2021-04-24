# Image-Segment
A PyQt5 based python GUI which can segment an image using Euclidean Distance method in the RGB vector space. 

This implementation of segmentation in RGB vector space is based from **Section 6.7.2** of **Chapter 6** of the book **Digital Image Processing**, by *Rafael C. Gonzales* and *Richard E. Woods*. (ISBN number: 9780070702622)

## Python Libraries Required
* PyQt5- for GUI purposes.
* cv2- to read image.
* numpy- for  calculations purposes
* matplotlib- to plot the images.

## How to run?
* Install the dependencies using ``` pip install -r requirements.txt ``` command.
* Run the python file ```segment.py```.
* A box will be opened, upload the image and then enter the threshold value required.
* Mark your region of Interest in the image and you'll get the segmented image. 


## Output
**Our test Image-** Lena.png

![Test Image Lena](https://github.com/ansh422/Image-Segment/blob/main/Lena.png?raw=true)

**Output after Segmenting-** lena_segment.png

![Segmented Image Lena](https://github.com/ansh422/Image-Segment/blob/main/lena_segment.PNG?raw=true)
