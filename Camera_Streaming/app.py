from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

# Open the webcam (use 1 if 0 doesn't show your Logitech camera)
camera = cv2.VideoCapture(0)

def generate_frames():
    """
    Continuously capture frames from the webcam and yield them as JPEG for streaming.
    """
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Encode the frame to JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # Yield frame with proper multipart formatting
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """
    Render the homepage with the video stream embedded.
    """
    return render_template("index.html")

@app.route('/video')
def video():
    """
    Route to stream the video feed.
    """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
