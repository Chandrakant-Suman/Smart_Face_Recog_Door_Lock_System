# Smart Face Recognition Door Lock System

A modern, secure, and fully automated door-locking system powered by facial recognition. This project combines embedded systems, computer vision, and IoT principles to deliver a reliable access-control mechanism designed for real-world deployment. It’s the kind of solution that politely tells traditional keys, “Your services are no longer required.”

# 📌 Project Overview

This system uses a camera module and a face recognition algorithm to identify authorized users and unlock the door automatically. Unauthorized attempts trigger a security response.

The whole architecture is engineered to be:
Accurate
Automated
Tamper-resistant
User-friendly
Scalable for home, office, or lab environments

# 🎯 Key Features

Real-time Face Detection & Recognition
Identifies pre-registered users with high accuracy.

Automatic Door Unlocking
Uses a relay/servo/motor-based locking mechanism.

Security Alerts
Unauthorized users trigger buzzer alerts or warning messages.

Local + Cloud Storage (optional)
Store face datasets locally or sync with cloud.

Low-power Embedded Hardware
Designed for efficient performance in embedded environments.

# 🛠️ Tech Stack
Layer	Technology
Hardware	ESP32 / Raspberry Pi / Camera Module, Relay/Servo Motor
Software	Python / OpenCV OR ESP-IDF/Arduino (depending on implementation)
Recognition	LBPH / Haar Cascade / CNN-based model
Storage	Local File System / SD Card / Cloud Integration

# 📂 Project Structure
Smart-Face-Recognition-Door-Lock/
│── /dataset                → Stored images for training
│── /training               → Model training scripts
│── /src                    → Main firmware/software code
│── /hardware               → Schematics, connections, parts list
│── /docs                   → Documentation and reports
│── README.md               → You’re reading it :)

# ⚙️ Working Principle

Camera scans the face of the person standing at the door.
The system extracts facial features and matches them with the trained model.
If the face is recognized → Lock opens automatically.
If the face is not recognized → System triggers alert mechanisms.
The entire flow runs autonomously with minimal user intervention.
Classic workflow, future-proof execution.

# 🚪 Hardware Requirements

ESP32-CAM / Raspberry Pi (depending on design)
OV2640 Camera Module
Relay Module / Servo Motor Lock
Buzzer (for alerts)
Power Supply (5V/2A)
Jumper Wires & Basic Hardware Tools

# 💻 Software Requirements

Python 3.x (if Raspberry Pi version)
OpenCV
Arduino IDE / ESP-IDF (for ESP32 version)
Serial Monitor Tools
Training Scripts (for dataset generation)

# 🧪 How to Run the Project

1. Prepare the Hardware
Connect camera module to ESP32/RPi
Connect relay/servo to control the lock
Power up and verify connections

2. Dataset Creation
Run:
python capture_images.py

Capture 50–100 images per authorized user.

3. Train the Model
python train_model.py

4. Deploy Firmware
Flash the microcontroller or run the Python script on Raspberry Pi.

5. Test the System
Stand in front of the camera → observe door lock response.
Straightforward. Mission-critical. No drama.

# 📈 Future Enhancements
Mobile App to manage user access
Cloud-based face dataset
Two-factor authentication (Face + OTP)
Integration with smart home systems
Night-vision support

# 👥 Team Members (Group 2)

Ayush Gupta 20233096(Group Leader)
Ayush Joshi 20233097
Ayush Pandey 20233331
Chandrakant Suman 20233106
Gopal Maheshwari 20233336
Harsh Agrawal 20233522
Harsh Chaurasiya 20233136
Jitendra Kumar 20233150
Kanishk Agrawal 20233526
Keshav Kumar 20233339
Keshav Kumar 20233158

# ✨ Acknowledgment
Embedded Systems Project
Subject Code Number: CSN15402

Course Coordinator: Saugata Roy
