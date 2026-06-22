# 🌿 ForestGuard AI - Wildlife Surveillance System

## Overview

ForestGuard AI is an AI-powered wildlife monitoring and surveillance system developed using Flask, OpenCV, and Groq AI. The system helps identify animals, plants, humans, and potential threats from images, videos, and live camera feeds.

It is designed to support wildlife conservation, forest monitoring, tourist safety, and threat detection by providing real-time analysis and intelligent alerts.

---

## ✨ Features

### 📷 Image Detection

Upload wildlife images and identify animals, plants, or possible threats.

### 🎥 Video Detection

Analyze uploaded videos and detect wildlife using extracted frames.

### 📹 Live Camera Detection

Use a webcam for real-time monitoring and instant wildlife identification.

### 🌱 Species Information

Get AI-generated information about animals, plants, and trees including:

* Scientific Name
* Habitat
* Diet
* Behavior
* Conservation Status

### 🚨 Threat Detection

Detect:

* Poaching activities
* Dangerous animals
* Human intrusions
* Deforestation activities

### 🖼️ Gallery

Store and view detected wildlife images.

### 📋 Activity Logs

Maintain records of detections including:

* Time
* Location
* User
* Detection Result

### 📊 Export Reports

Export detection logs in:

* CSV Format
* PDF Format

### ⚙️ Admin Controls

Manage:

* User accounts
* Notifications
* Alerts
* Reports

---

## 🛠️ Technologies Used

* Python
* Flask
* Groq AI
* OpenCV
* HTML
* CSS
* JavaScript
* ReportLab

---

## 📂 Project Structure

```text
wildlife_surveillance/
│
├── app.py
│
├── static/
│   ├── style.css
│   └── script.js
│
├── uploads/
│
├── index.html
│
├── requirements.txt
│
└── README.md
```

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/sujithamary-2607/wildlife_surveillance.git
cd wildlife_surveillance
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Add Your Groq API Key

Open `app.py`

Find:

```python
client = Groq(api_key="YOUR_GROQ_API_KEY")
```

Replace with your Groq API key:

```python
client = Groq(api_key="gsk_xxxxxxxxxxxxxxxxx")
```

You can get a free API key from Groq.

### Step 4: Run the Application

```bash
python app.py
```

### Step 5: Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🔐 Admin Login

Use the following credentials:

**Username**

```text
admin
```

**Password**

```text
admin.1234
```

---

## 👥 User Modes

### Tourist Mode

* Wildlife identification
* Species information
* Image and video detection

### Admin Mode

* Threat monitoring
* Alert management
* User management
* Log export
* Notification settings

---

## 🚨 Safety Levels

| Level   | Meaning                               |
| ------- | ------------------------------------- |
| SAFE    | Normal wildlife detected              |
| WARNING | Human activity detected               |
| DANGER  | Threat or dangerous wildlife detected |

---

## 🎯 Project Objective

The main objective of this project is to assist wildlife conservation and forest monitoring by using Artificial Intelligence to identify species, detect threats, and provide useful insights for researchers, forest officers, and tourists.

---

## 🔮 Future Enhancements

* GPS map integration
* SMS and Email alerts
* Wildlife database storage
* Deep learning object detection models
* Mobile application support
* Cloud deployment

---

## 👩‍💻 Author

**T. Sujitha Mary**

Department of Artificial Intelligence and Data Science

St. Joseph's College of Engineering

---


