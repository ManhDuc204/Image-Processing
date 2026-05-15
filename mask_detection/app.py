from flask import (
    Flask,
    render_template,
    Response,
    request,
    redirect,
    url_for,
    session,
    send_file
)

from ultralytics import YOLO

import cv2
import os
import time
import pandas as pd
import pygame


app = Flask(__name__)

app.secret_key = "mask_secret"


model = YOLO("best.pt")


cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


sound_ready = False

try:

    pygame.mixer.init()

    alert_sound = pygame.mixer.Sound(
        "sounds/Beep.mp3"
    )

    sound_ready = True

except:

    print("Không tìm thấy âm thanh")


os.makedirs(
    "static/violations",
    exist_ok=True
)


USERNAME = "admin"
PASSWORD = "123456"


logs = []

last_beep = 0
last_save = 0

total_mask = 0
total_nomask = 0


def generate_frames():

    global last_beep
    global last_save

    global total_mask
    global total_nomask

    while True:

        success, frame = cap.read()

        if not success:
            break

        results = model.predict(
            frame,
            conf=0.6,
            verbose=False
        )

        mask_count = 0
        nomask_count = 0

        violation = False

        for r in results:

            for box in r.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cls = int(box.cls[0])

                label = model.names[cls].lower()

                if "no" in label:

                    color = (0, 0, 255)

                    nomask_count += 1
                    total_nomask += 1

                    violation = True

                else:

                    color = (0, 255, 0)

                    mask_count += 1
                    total_mask += 1

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    color,
                    2
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

        status = (
            "WARNING: NO MASK"
            if violation
            else "STATUS: SAFE"
        )

        status_color = (
            (0, 0, 255)
            if violation
            else (0, 255, 0)
        )

        current_time = time.time()

        if violation:

            if (
                sound_ready and
                current_time - last_beep > 2
            ):

                alert_sound.play()

                last_beep = current_time

            if current_time - last_save > 5:

                timestamp = time.strftime(
                    "%Y%m%d_%H%M%S"
                )

                filename = f"{timestamp}.jpg"

                filepath = os.path.join(
                    "static/violations",
                    filename
                )

                cv2.imwrite(filepath, frame)

                logs.append({

                    "time": time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),

                    "status": "NO MASK",

                    "image": filename
                })

                last_save = current_time

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (640, 120),
            (40, 40, 40),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.6,
            frame,
            0.4,
            0,
            frame
        )

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            status_color,
            3
        )

        cv2.putText(
            frame,
            f"Mask: {mask_count}",
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"No Mask: {nomask_count}",
            (220, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        )

        ret, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame +
            b"\r\n"
        )


@app.route("/")

def home():

    return redirect(url_for("login"))


@app.route(
    "/login",
    methods=["GET", "POST"]
)

def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        if (
            username == USERNAME and
            password == PASSWORD
        ):

            session["user"] = username

            return redirect(
                url_for("dashboard")
            )

    return render_template("login.html")


@app.route("/dashboard")

def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(

        "dashboard.html",

        total_mask=total_mask,

        total_nomask=total_nomask,

        logs=logs
    )


@app.route("/video")

def video():

    return Response(

        generate_frames(),

        mimetype=
        "multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/download")

def download():

    df = pd.DataFrame(logs)

    file_name = "report.csv"

    df.to_csv(
        file_name,
        index=False,
        encoding="utf-8-sig"
    )

    return send_file(
        file_name,
        as_attachment=True
    )


if __name__ == "__main__":

    print("MASK DETECTION WEB SYSTEM")
    print("username: admin")
    print("password: 123456")

    app.run(debug=True)