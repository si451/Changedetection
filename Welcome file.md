
# Project Documentation: Image Change Detection
## 1. Project Overview
This project is designed to automatically detect significant changes between pairs of "before" and "after" images. It identifies regions where objects present in the first image are missing or altered in the second. The script then generates a side-by-side comparison image, highlighting the detected differences with red bounding boxes on the "after" image.

## 2. Project Structure
The project is organized into the following directories and files:

```
/Task2
|-- input-images/         # Contains all input image pairs
|   |-- 1.jpg
|   |-- 1~2.jpg
|   |-- 2.jpg
|   |-- 2~2.jpg
|   |-- ... (and so on)
|-- output/               # Generated output images are 
saved here
|   |-- 1_differences.jpg
|   |-- 2_differences.jpg
|   |-- ...
|-- change_detection.py   # The main Python script for 
processing
```
## 3. Requirements
- Python 3.x
- The following Python libraries:
  - opencv-python : For image processing tasks like reading, writing, and drawing.
  - scikit-image : Used for calculating the Structural Similarity Index (SSIM).
  - numpy : For numerical operations and array manipulation.
## 4. Setup and Execution
1. Install Dependencies: If you haven't already, open your terminal and run the following command to install the required libraries:
   
   ```
   pip install opencv-python scikit-image numpy
   ```
2. Run the Script: Execute the main script from the terminal:
   
   ```
   python "c:\Users\siddi\Desktop\Assessment 
   Folder\Task2\change_detection.py"
   ```
   The script will automatically find image pairs in the input-images folder and save the results in the output folder.
## 5. Code Walkthrough (change_detection.py)
The script operates in the following sequence:

1. Initialization : It defines the input and output folder paths and creates the output directory if it doesn't exist.
2. Image Pairing : It scans the input-images directory and intelligently pairs the 'before' images (e.g., 1.jpg ) with their corresponding 'after' images (e.g., 1~2.jpg ).
3. Processing Loop : The script iterates through each identified pair.
   a. Load Images : It loads both the 'before' and 'after' images in grayscale.
   b. Compute Difference : It uses the Structural Similarity Index (SSIM) to compute a difference map between the two images. This method is effective at highlighting structural changes while ignoring minor variations in lighting or texture.
   c. Thresholding : The difference map is converted into a binary image (black and white) using a threshold. This isolates the areas with the most significant changes.
   d. Clean Noise : Morphological operations (closing and opening) are applied to remove small, irrelevant spots or noise from the thresholded image, ensuring that only substantial changes are considered.
   e. Find Contours : The script identifies the boundaries (contours) of the cleaned, changed areas.
   f. Draw Bounding Boxes : For each contour with an area greater than a set minimum (to filter out tiny changes), a red bounding box is drawn on a copy of the 'after' image.
   g. Save Output : A final comparison image is created by placing the original 'before' image and the annotated 'after' image side-by-side. This composite image is saved to the output folder.
