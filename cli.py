import sys
import requests
from PIL import Image
from io import BytesIO
from OCR import DiabloImageReader, DiabloItem, DiabloItemParser

def main():
    if len(sys.argv) < 2:
        print("Please provide a picture URL as an argument.")
        return

    picture_url = sys.argv[1]

    response = requests.get(picture_url)
    image = Image.open(BytesIO(response.content))
    item = DiabloItemParser().parse(DiabloImageReader.perform_ocr(image))

    print(item.to_json())

if __name__ == "__main__":
    main()
