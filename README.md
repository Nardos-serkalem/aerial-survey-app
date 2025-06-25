# 🛰 Aerial Survey Flight Report System

This is a web-based Flight Report Submission and Monitoring System for the **Space Science and Geospatial Institute (SSGI)**. It enables aerial survey teams to submit detailed flight reports and view past submissions in a well-structured dashboard.

---

## 🚀 Features

- 📝 **Flight Submission Form**  
  Record all essential aerial survey flight data including aircraft info, camera settings, flight timings, and operator details.

- 📊 **Dashboard Overview**  
  Browse all submitted flights with full details in a responsive layout. Displays time summary and flight entry breakdown per record.

- ⏱ **Flight Time Summary Calculations**  
  Automatically computes:
  - Start to Stop Movement
  - Takeoff to Landing
  - Engine Start to Shutdown

- 🔐 **Authentication**  
  Secure access using Flask-Login to ensure only registered users can submit/view data.

- 📡 **Real-time Updates**  
  Integrated with Socket.IO to support real-time broadcasting (optional enhancement).

---

## 🛠 Tech Stack

- **Backend**: Flask (Python), SQLAlchemy, SQLite  
- **Frontend**: HTML5, Bootstrap 5, JavaScript  
- **Authentication**: Flask-Login  
- **Live updates (Optional)**: Flask-SocketIO  
- **Database**: SQLite (default, can switch to PostgreSQL/MySQL)

## 📦 How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/aerial-survey-app.git
cd aerial-survey-app

# 2. Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the application
python app.py
```

The app will run on `http://127.0.0.1:5000/`.

## 🏢 Developed for

**Space Science and Geospatial Institute (SSGI)**  
Flight Data Management Division

![Screenshot (564)](https://github.com/user-attachments/assets/94eca511-04b1-450a-b01b-df2143cc8e45)
![Screenshot (595)](https://github.com/user-attachments/assets/d7ce8b5a-8528-4986-8a23-56134884c2dd)
![Screenshot (609)](https://github.com/user-attachments/assets/74dc974f-1df6-4c50-b952-182eed467581)
![Screenshot (608)](https://github.com/user-attachments/assets/08601411-699e-4776-9a05-0d3b9c70d0b5)

