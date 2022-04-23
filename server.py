#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import io
import time
import picamera
# Creating instance of Flask and passing
app = Flask(__name__, template_folder='template')
@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')
def gen():
    """Video streaming generator function."""
    with picamera.PiCamera() as camera:
        camera.vflip = True
        camera.resolution = (640, 480)
        yield b'--frame\r\n'
        # let camera warm up
        # time.sleep(2)
        stream = io.BytesIO()
        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            # return current frame
            stream.seek(0)
            frame = stream.read()
            yield b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n--frame\r\n'
            # reset stream for next frame
            stream.seek(0)
            stream.truncate()
@app.route("/stream.mjpg", methods=["GET"])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=3000,
        threaded=True
    )
