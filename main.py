import time
from flask import Flask, render_template, jsonify
from DetectUser import DetectUser

app = Flask(__name__)

detect_user = DetectUser()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/check_hand_status')
def check_hand_status():
    status = detect_user.detect_hand(0)
    print(status)
    #print(status)
    return jsonify({'hand_status': status})

if __name__ == '__main__':
    detect_user.start_detection_thread()
    time.sleep(1)
    app.run(debug=True)
