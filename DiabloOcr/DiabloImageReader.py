import time
import cv2
import numpy as np
import pytesseract
import re

class DiabloImageReader:
    def __init__():
        pass
        
    @staticmethod
    def optimize_image_for_tesseract(image):
        #return image
        # Get the current width of the image
        current_width = image.shape[1]

        # Set the target width
        target_width = 1000

        # Calculate the scaling factor based on the target width
        scaling_factor = target_width / current_width

        # Calculate the new size in pixels
        new_width = int(current_width * scaling_factor)
        new_height = int(image.shape[0] * scaling_factor)
        new_size = (new_width, new_height)

        # Resize the image using the calculated size
        image = cv2.resize(image, new_size)

        # norm_image = np.zeros((image.shape[0], image.shape[1]))
        # image = cv2.normalize(image, norm_image, 180, 255, cv2.NORM_MINMAX)
        
   
        # cv2.imwrite('debug3.png', image)
        # 
        # image = np.clip(image, 0, 256).astype(np.uint8)

        # Convert the image to float32 for calculations
    

        # Convert the image to grayscale
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate the histogram of the grayscale image
        hist, bins = np.histogram(image_gray.flatten(), bins=256, range=[0, 256])

        # Find the index of the maximum histogram value
        max_index = np.argmax(hist)

        # Set the black level to the right of the maximum histogram value
        black_level = max_index + 30

        # Define the white level and clamp value
        white_level = 255
        clamp_value = 1

        # Create a lookup table (LUT) for color adjustment
        lut = np.arange(256, dtype=np.uint8)
        lut[:black_level] = 0
        lut[black_level:white_level] = np.clip((lut[black_level:white_level] - black_level) * (255 / (white_level - black_level)), clamp_value, white_level)
        lut[white_level:] = white_level

        # Apply the LUT transformation to the image
        image = cv2.LUT(image, lut)
 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

 
        # cv2.imwrite('debug2.png', image)
 
        _, image = cv2.threshold(image, 25, 255, cv2.THRESH_BINARY_INV)

        # image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

        # border_color = (255, 255, 255)  # Black color
        # border_size = 30
        # image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)
        # border_color = (0, 0, 0)  # Black color
        # border_size = 3
        # image = cv2.copyMakeBorder(image, border_size, border_size, border_size, border_size, cv2.BORDER_CONSTANT, value=border_color)
                
        # cv2.imwrite('debug.png', image)
       
        return image

    @staticmethod
    def perform_ocr(image):
        image = DiabloImageReader.optimize_image_for_tesseract(image)
        ocr_text = pytesseract.image_to_string(image, config='--psm 4 -c preserve_interword_spaces=0')
        return DiabloImageReader.replace_special_characters(ocr_text)

    @staticmethod
    def replace_special_characters(text):
        pattern = r'[^0-9a-zA-Z\+\[\]\(\)%\. \n-]+'
        return re.sub(pattern, '', text.replace('®', 'O').replace('@', 'O').replace('£', 'E').replace('(', '[').replace(')', ']'))