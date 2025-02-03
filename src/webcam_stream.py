import cv2
import time
from detect_plate import detect_license_plate

if __name__ == "__main__":
    try:
        detect_license_plate()
    except KeyboardInterrupt:
        print("Program dihentikan.")
