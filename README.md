
# 🔐 Hashcat Cracking Queue System

**Streamline your password cracking — queue, manage, and get notified effortlessly.**

A lightweight Flask web app for managing and queuing [Hashcat](https://hashcat.net/hashcat/) cracking jobs on your local machine.  
Supports multi-user login, real-time job tracking, and notifications via email or webhooks.

---

## 📦 Features

- ✅ Submit and queue hash cracking jobs with custom wordlists, rules, and hash types
- 🧠 Jobs executed sequentially in the background using Hashcat
- 📧 Email and webhook notifications when jobs complete
- 🔐 Secure login system with bcrypt-hashed passwords
- 🌐 Web-based dashboard for job status and management
- 💾 Queue persists across application restarts
- 📁 Drag & drop UI with file upload support

---

## 🛠️ Project Structure


hashcat-queue/
├── app.py # Flask web app
├── job_model.py # Job model
├── queue_manager.py # Queue persistence
├── job_runner.py # Background job execution with hashcat
├── notifier.py # Email and webhook notifications
├── templates/ # Flask HTML templates
│ ├── login.html
│ └── dashboard.html
├── wordlists/ # Custom wordlists (add yours here)
├── rules/ # Hashcat rule files (optional)
├── uploads/ # Uploaded hash files (auto-created)
├── users.json # User database with hashed passwords
├── .env # Environment variables (not committed)
├── .gitignore
└── requirements.txt





## 🚀 Quick Start

### 1. Clone the Repo

bash
git clone https://github.com/sendmetirries/hashcat-cracking-queue.git
cd hashcat-cracking-queue

Set Up Virtual Environment (Recommended)

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt


⚙️ Configuration
Create a .env File

This keeps your credentials and settings out of your source code.

SECRET_KEY=supersecretkey123
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your.email@gmail.com
SMTP_PASSWORD=your-app-password
WEBHOOK_URL=https://your-webhook-endpoint
🧪 Run the App

python app.py

Then open your browser at:
http://127.0.0.1:5000 



