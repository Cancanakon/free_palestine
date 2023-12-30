import time
from flask import Flask, render_template, jsonify
from DetectUser import DetectUser
import sqlite3
import os

app = Flask(__name__)

detect_user = DetectUser()

def get_db_connection():
    conn = sqlite3.connect('user_count.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    if not os.path.exists('user_count.db'):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE user_count (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                count INTEGER
            )
        ''')
        cursor.execute('INSERT INTO user_count (count) VALUES (0)')
        conn.commit()
        conn.close()

init_database()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE user_count SET count = count + 1')
    conn.commit()
    conn.close()
    return render_template('success.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/check_hand_status')
def check_hand_status():
    status = detect_user.detect_hand(0)
    print(status)
    return jsonify({'hand_status': status})

if __name__ == '__main__':
    detect_user.start_detection_thread()
    time.sleep(1)
    app.run(debug=True)
