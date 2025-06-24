from flask import Flask, request, render_template, flash, url_for, redirect, session
import csv
import sqlite3
import secrets
import io
import os
import pyqrcode
import png

app = Flask(__name__)
print(secrets.token_hex(16))
app.secret_key = 'a42afb59dab1808b4b116bc2d1b6aba3'

UPLOAD_FOLDER = 'static/qrcodes'
learner_data = []  # Store uploaded learners in memory for now

# Ensure folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def form():
    return render_template('upload.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/print')
def print():
    return render_template('print.html')


@app.route('/register_event')
def register_event():
    return render_template('register_event.html')


@app.route('/view_event')
def view_event():
    return render_template('view_event.html')


@app.route('/mark_attendance')
def mark_attendance():
    return render_template('mark_attendance.html')


@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['csvfile']
    if not file or file.filename == '':
        flash('❌ No file selected. Please upload a CSV.', 'danger')
        return redirect(url_for('form'))

    stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
    reader = csv.DictReader(stream)

    for row in reader:
        learner_id = row['learner_id']
        name = row['name']
        grade = row['grade']

        # 🧾 QR code data (Google search link with name)
        qr_data = f"https://www.google.com/search?q={name.replace(' ', '+')}"
        qr = pyqrcode.create(qr_data)
        qr_filename = f"{learner_id}.png"
        qr_path = os.path.join(UPLOAD_FOLDER, qr_filename)
        qr.png(qr_path, scale=6)

        # 📥 Insert into DB
        with sqlite3.connect("app.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO learners (learner_id, name, grade, qr_code) VALUES (?, ?, ?, ?)",
                (learner_id, name, grade, qr_filename))
            conn.commit()
    flash('✅ CSV uploaded and QR codes generated successfully!', 'success')
    return redirect(url_for('form'))


@app.route('/view')
def view_data():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row  # allows dictionary-style access
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM learners")
    rows = cursor.fetchall()
    conn.close()

    learners = [dict(row)
                for row in rows]  # convert sqlite rows to list of dicts

    return render_template('view.html', learners=learners)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
