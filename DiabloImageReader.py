import pytesseract
import re
from PIL import ImageOps
from PIL import ImageEnhance

class DiabloImageReader:
    @staticmethod
    def optimize_image_for_tesseract(image):
        # Resize the image if needed (optional)
        max_size = 3000
        if max(image.size) > max_size:
            image.thumbnail((max_size, max_size))

        # Convert to grayscale
        image = image.convert('L')
        
        # Apply image enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)


        image = ImageOps.invert(image)
        image = image.point(lambda pixel: 0 if pixel < 128 else 255 if pixel > 200 else 0)
       
        return image

    @staticmethod
    def perform_ocr(image):
        image = DiabloImageReader.optimize_image_for_tesseract(image)
        ocr_text = pytesseract.image_to_string(image)
        return DiabloImageReader.replace_special_characters(ocr_text)

    @staticmethod
    def replace_special_characters(text):
        pattern = r'[^0-9a-zA-Z\+\[\]\(\)%\. \n-]+'
        return re.sub(pattern, '', text.replace('®', 'O').replace('@', 'O').replace('£', 'E').replace('(', '[').replace(')', ']'))