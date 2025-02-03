import requests
import yaml
from datetime import datetime

CONFIG_PATH = "Folder pengguna: {user_folder}/config.yaml"
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

TOKEN = config["telegram_token"]
CHAT_ID = config["chat_id"]
TELEGRAM_URL = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

def send_to_telegram(image_path, plate_text):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    caption = f"🚗 Plat Terdeteksi: {plate_text}\n📅 Waktu: {timestamp}"
    with open(image_path, "rb") as img:
        requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "caption": caption}, files={"photo": img})
