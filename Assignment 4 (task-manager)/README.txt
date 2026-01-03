🗂️ Task Manager Application

A full-stack Task Manager application built using FastAPI (Python) for the backend and React for the frontend.
The application allows users to take tasks from a queue, manage their own tasks, and track task start/stop time with live updates.

📌 Features
✅ Task Queue

Displays tasks that are not yet taken

Each task has:

Assign (assigns and starts task)

Keep (assigns without starting)

Once taken:

Task disappears immediately from the queue

Task never reappears in the queue

✅ My Tasks

Displays tasks kept by the current user

Each task shows:

Start Time

Stop Time

Buttons:

Start

Stop

Button Behavior
State	Start	Stop
Initial	Enabled	Disabled
After Start	Disabled	Enabled
After Stop	Disabled	Disabled
✅ Live Updates (Polling)

Task data automatically refreshes every 5 seconds

Queue updates in real-time when tasks are taken by any user

No manual refresh required

✅ Data Persistence

Task state persists after page refresh

Start and Stop times persist after refresh

Tasks never appear in incorrect sections

✅ Time Handling

Backend stores timestamps in UTC

Frontend converts and displays time in IST (Asia/Kolkata)

Supports 12-hour or 24-hour display

✅ UI Enhancements

Card-based layout

Clear task status badges (KEPT / RUNNING / COMPLETED)

Visually distinct action buttons

Responsive dashboard layout

🛠️ Tech Stack
Backend

Python

FastAPI

SQLAlchemy

SQLite

Frontend

React

Axios

CSS (no external UI libraries)

📂 Project Structure
task-manager/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   └── task_manager.db
│
└── frontend/
    ├── src/
    │   ├── App.js
    │   ├── Queue.js
    │   ├── MyTasks.js
    │   ├── api.js
    │   └── App.css
    └── package.json

🚀 How to Run the Application
🔹 Backend (FastAPI)

Navigate to backend directory

cd backend


Create virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows


Install dependencies

pip install fastapi uvicorn sqlalchemy


Run the server

uvicorn main:app --reload


Backend runs at:

http://127.0.0.1:8000

🔹 Frontend (React)

Navigate to frontend directory

cd frontend


Install dependencies

npm install


Start the React app

npm start


Frontend runs at:

http://localhost:3000

🧪 Usage Instructions

Enter a username to log in

View available tasks in Task Queue

Assign or Keep a task

Start and Stop tasks from My Tasks

Observe live updates without refreshing the page

🧠 Design Decisions

UTC storage ensures consistency across time zones

Frontend timezone conversion avoids backend coupling

Polling approach used for simplicity and reliability

Backend-driven task state ensures data integrity

No task duplication or invalid transitions

🏁 Conclusion

This project fulfills all requirements of the assessment:

Queue management

User-specific task tracking

Start/Stop tracking

Live updates

Data persistence

Clean and responsive UI

📎 Notes

Authentication is intentionally lightweight (username-based) as per assignment scope

Polling can be replaced with WebSockets in a production environment

A Python virtual environment is recommended for running the backend.