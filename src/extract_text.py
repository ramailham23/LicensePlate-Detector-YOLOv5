import cv2
import pytesseract

def preprocess_plate(plate_image):
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2))  
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return gray

def extract_text(plate_image):
    cleaned_image = preprocess_plate(plate_image)
    text = pytesseract.image_to_string(cleaned_image, config="--psm 7")
    return text.strip()
