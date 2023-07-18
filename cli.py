import sys
import cv2
import numpy as np
import requests
from DiabloOcr.DiabloItemParser import DiabloItemParser
from DiabloOcr.DiabloImageReader import DiabloImageReader

def main():
    if len(sys.argv) < 2:
        print("Please provide a picture URL as an argument.")
        return

    picture_url = sys.argv[1]

    response = requests.get(picture_url, stream=True).raw
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    item = DiabloItemParser().parse(DiabloImageReader.perform_ocr(image))

    print(item.to_json())

if __name__ == "__main__":
    main()
