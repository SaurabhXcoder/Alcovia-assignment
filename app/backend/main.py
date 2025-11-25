from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# -------------------------
# DATABASE CONNECTION
# -------------------------
conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME", "railway"),
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", ""),
    host=os.environ.get("DB_HOST", "localhost"),
    port=os.environ.get("DB_PORT", "5432"),
    cursor_factory=RealDictCursor
)

# -------------------------
# N8N WEBHOOK
# -------------------------
N8N_WEBHOOK = os.environ.get("N8N_WEBHOOK", "https://example.com")

# -------------------------
# ROUTES
# -------------------------
@app.route("/daily-checkin", methods=["POST"])
def daily_checkin():
    data = request.get_json()
    student_id = data.get("student_id")
    quiz_score = data.get("quiz_score")
    focus_minutes = data.get("focus_minutes")

    if not all([student_id, quiz_score, focus_minutes]):
        return jsonify({"error": "Missing required fields"}), 400

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO daily_logs (student_id, quiz_score, focus_minutes, log_date) VALUES (%s, %s, %s, %s)",
            (student_id, quiz_score, focus_minutes, datetime.utcnow())
        )

        if quiz_score > 7 and focus_minutes > 60:
            cur.execute("UPDATE students SET status=%s WHERE id=%s", ('On Track', student_id))
            status = "On Track"
        else:
            cur.execute("UPDATE students SET status=%s WHERE id=%s", ('Needs Intervention', student_id))
            status = "Pending Mentor Review"

        conn.commit()

    # Send to n8n webhook, but don't crash if it fails
    try:
        requests.post(N8N_WEBHOOK, json=data, timeout=5)
    except requests.RequestException:
        print("⚠ Could not reach n8n webhook")

    return jsonify({"status": status})


@app.route("/assign-intervention", methods=["POST"])
def assign_intervention():
    data = request.get_json()
    student_id = data.get("student_id")
    task = data.get("task")

    if not all([student_id, task]):
        return jsonify({"error": "Missing required fields"}), 400

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO interventions (student_id, task, assigned_at, completed) VALUES (%s, %s, %s, %s)",
            (student_id, task, datetime.utcnow(), False)
        )
        cur.execute("UPDATE students SET status=%s WHERE id=%s", ('Under Intervention', student_id))
        conn.commit()

    return jsonify({"msg": "Intervention assigned"})


@app.route("/student-status/<int:student_id>", methods=["GET"])
def student_status(student_id):
    with conn.cursor() as cur:
        cur.execute("SELECT status FROM students WHERE id=%s", (student_id,))
        row = cur.fetchone()
        return jsonify({"status": row['status'] if row else "Unknown"})


@app.route("/intervention/<int:student_id>", methods=["GET"])
def get_intervention(student_id):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT task FROM interventions WHERE student_id=%s AND completed=FALSE ORDER BY assigned_at DESC LIMIT 1",
            (student_id,)
        )
        row = cur.fetchone()
        return jsonify({"task": row['task'] if row else ""})


@app.route("/intervention-complete", methods=["POST"])
def complete_intervention():
    data = request.get_json()
    student_id = data.get("student_id")

    if not student_id:
        return jsonify({"error": "Missing student_id"}), 400

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE interventions SET completed=TRUE WHERE student_id=%s AND completed=FALSE",
            (student_id,)
        )
        cur.execute("UPDATE students SET status=%s WHERE id=%s", ("On Track", student_id))
        conn.commit()

    return jsonify({"msg": "Student unlocked"})


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
