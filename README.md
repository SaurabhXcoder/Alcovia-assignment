# Alcovia Assignment

This project is a **Student Progress Monitoring & Intervention System** built using **Flask** for the backend and **React** for the frontend. It also integrates with **n8n** for workflow automation.

---

## Project Structure

alcovia-assignment/
│
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ ├── Procfile
│ └── .env (ignored in Git)
│
├── frontend/
│ ├── package.json
│ ├── package-lock.json
│ ├── src/
│ │ ├── App.js
│ │ ├── index.js
│ │ └── other React files
│ └── public/
│
├── n8n_Workflow/ (if exists)
│ └── workflow.json
│
├── database/
   └── appdb.sql

---

## Features

### Backend (Flask)
- **Daily Check-in:** Students log their quiz score and focus minutes.
- **Status Update:** Automatically updates student status based on performance.
- **Intervention Management:** Assign tasks to students who need help.
- **Integration:** Sends data to an n8n webhook for workflow automation.
- **APIs Provided:**
  - `POST /daily-checkin`
  - `POST /assign-intervention`
  - `GET /student-status/<student_id>`
  - `GET /intervention/<student_id>`
  - `POST /intervention-complete`

### Frontend (React)
- React web application to interact with backend APIs.
- Displays student status and intervention tasks.
- Responsive UI to monitor daily logs and interventions.

---

## Environment Variables

Backend `.env` example:

Author

Saurabh Rajput
Email: saurabh.rajput8284@gmail.com

GitHub: https://github.com/SaurabhXcoder

