import sys
import os
import cv2
import torch
import pytesseract
import yaml
import requests
import time
from datetime import datetime
from pathlib import Path

sys.path.append("Folder pengguna: {user_folder}/yolov")

from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from utils.plots import Annotator, colors

with open("Folder pengguna: {user_folder}/config.yaml", "r") as f:
    config = yaml.safe_load(f)

TELEGRAM_TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]
MODEL_PATH = "Folder pengguna: {user_folder}/weights/" + config["model_path"]
CAMERA_INDEX = config["camera_index"]

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DetectMultiBackend(MODEL_PATH, device=device)
stride, names = model.stride, model.names

def send_to_telegram(image_path, plate_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caption = f"🚗 Plat Terdeteksi: {plate_text}\n📅 Waktu: {timestamp}"
    with open(image_path, "rb") as img:
        requests.post(url, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": img})

def preprocess_plate(plate_image):
    gray = cv2.cvtColor(plate_image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (gray.shape[1] * 2, gray.shape[0] * 2)) 
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return gray

def extract_text(plate_image):
    cleaned_image = preprocess_plate(plate_image)
    text = pytesseract.image_to_string(cleaned_image, config="--psm 7")
    return text.strip()

def detect_license_plate():
    cap = cv2.VideoCapture(CAMERA_INDEX)
    prev_time = time.time()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time
        
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).to(device).float() / 255.0
        img = img.permute(2, 0, 1).contiguous().unsqueeze(0)

        results = model(img)
        preds = non_max_suppression(results, conf_thres=0.25, iou_thres=0.45)
        
        for det in preds:
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()
                
                for *xyxy, conf, cls in det:
                    x1, y1, x2, y2 = map(int, xyxy)
                    plate_crop = frame[y1:y2, x1:x2]
                    plate_text = extract_text(plate_crop)
                    
                    if plate_text:
                        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        image_path = f"Folder pengguna: {user_folder}/runs/{timestamp}.jpg"
                        cv2.imwrite(image_path, plate_crop)
                        send_to_telegram(image_path, plate_text)
                        
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, plate_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        cv2.imshow("License Plate Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_license_plate()
