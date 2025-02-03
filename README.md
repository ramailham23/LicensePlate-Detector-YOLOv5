# 🚗 License Plate Detection System (YOLOv5)

This system uses **YOLOv5** to detect vehicle license plates in real-time via a camera.  
When a license plate is detected, the system will:
1. **Capture a screenshot of the detected license plate**
2. **Run OCR (Optical Character Recognition) to read the plate number**
3. **Send the captured image and recognized text to a Telegram bot**

---

## 📂 **1. Project Structure**
LicensePlate-Detector-YOLOv5/

│── yolov5/                        # YOLOv5 (make sure it is cloned from GitHub)

│── weights/

│   └── plate.pt                   # Your YOLOv5 model

│── src/

│   ├── detect_plate.py

│   ├── webcam_stream.py

│   ├── send_telegram.py

│   ├── extract_text.py

│── config.yaml

│── requirements.txt

│── run.sh


---

## 🔧 **2. Installation Guide**
1. Clone The Repository:
git clone https://github.com/ramailham23/LicensePlate-Detector-YOLOv5.git
cd LicensePlate-Detector-YOLOv5

2. Create & Activate Virtual Environment:
python3 -m venv venv
source venv/bin/activate  # For Linux/Mac

3. Install Dependencies:
pip install --upgrade pip
pip install -r requirements.txt

4. Clone YOLOv5 & Install:
git clone https://github.com/ultralytics/yolov5.git
cd yolov5
pip install -r requirements.txt
cd ..

5. Configure the Telegram Bot:
open the config.yaml file and fill in:
telegram_token: "YOUR_BOT_TOKEN"
chat_id: "YOUR_CHAT_ID"
model_path: "your train model.pt"
camera_index: 0  # Default webcam (change if using another source)

**📌 How to Get Your Telegram Chat ID & Token:**
1. Create a bot on Telegram using @BotFather
2. Get the bot token
3. Use @userinfobot to get your chat ID

---

## ▶️ **3. Running the System**
Once everything is set up, start the system with:

./run.sh

📌 If run.sh is not executable, give it permission:

chmod +x run.sh

---

## 🔍 **4. How It Works**
1. The system detects license plates via the camera.
2. If a plate is detected, OCR will read the plate text.
3. The screenshot and detected plate text will be sent to your Telegram bot.
   
**📌 To exit the program, press Q on the camera window.**

---

## 📌 **5. License**
This project is licensed under the **MIT License.**

---

## 📞 **6. Contact**
For any questions or issues, feel free to reach out:

**📩 Email:** mohilhamramadana721@gmail.com

**💬 Telegram:** @Ambatronus
