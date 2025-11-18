

import os
import io
import json
import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string, redirect, url_for
from PIL import Image
import face_recognition

#CONFIGURATION
ENROLLED_DIR = "enrolled"
ENCODINGS_FILE = "known_encodings.pkl"
TOLERANCE = 0.5
PORT = 5000

app = Flask(__name__)
os.makedirs(ENROLLED_DIR, exist_ok=True)

#html UI

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Smart Door Lock Enrollment</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f2f2f2; text-align: center; padding-top: 60px; }
    h2 { color: #333; }
    form { background: white; display: inline-block; padding: 30px; border-radius: 10px;
           box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    input[type=text] { padding: 10px; margin: 10px; width: 80%; border: 1px solid #ccc; border-radius: 5px; }
    input[type=file] { margin: 10px; }
    button { padding: 10px 20px; border: none; background: #007bff; color: white;
             border-radius: 5px; cursor: pointer; }
    button:hover { background: #0056b3; }
    .msg { margin-top: 20px; color: green; }
    img { width: 120px; height: auto; border-radius: 10px; margin: 5px; }
    .faces { margin-top: 20px; }
  </style>
</head>
<body>
  <h2>Enroll a New Family Member</h2>
  <form action="/enroll" method="POST" enctype="multipart/form-data">
    <input type="text" name="name" placeholder="Enter name" required><br>
    <input type="file" name="photo" accept="image/*" required><br>
    <button type="submit">Enroll</button>
  </form>
  {% if message %}
  <div class="msg">{{ message }}</div>
  {% endif %}

  <div class="faces">
    <h3>Currently Enrolled Members:</h3>
    {% for name, file in faces %}
      <div>
        <img src="/static/{{file}}" alt="{{name}}">
        <div>{{name}}</div>
      </div>
    {% endfor %}
  </div>
</body>
</html>
"""

#  FUNCTIONS 

def build_encodings():
    known_encodings = []
    known_names = []
    for fn in os.listdir(ENROLLED_DIR):
        path = os.path.join(ENROLLED_DIR, fn)
        if not fn.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        name = os.path.splitext(fn)[0]
        img = face_recognition.load_image_file(path)
        encs = face_recognition.face_encodings(img)
        if len(encs) == 0:
            print(f"[WARN] No face found in {fn}")
            continue
        known_encodings.append(encs[0])
        known_names.append(name)
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump((known_encodings, known_names), f)
    return known_encodings, known_names

def load_encodings():
    if os.path.exists(ENCODINGS_FILE):
        try:
            with open(ENCODINGS_FILE, "rb") as f:
                return pickle.load(f)
        except:
            pass
    return build_encodings()

known_encodings, known_names = load_encodings()

def save_image(file_storage, name):
    # Save uploaded photo to enrolled folder
    ext = os.path.splitext(file_storage.filename)[1]
    path = os.path.join(ENROLLED_DIR, f"{name}{ext}")
    file_storage.save(path)
    return path

#API endpoints

@app.route("/")
def home():
    return redirect("/enroll")

@app.route("/enroll", methods=["GET", "POST"])
def enroll():
    message = ""
    if request.method == "POST":
        name = request.form.get("name").strip()
        file = request.files.get("photo")
        if not name or not file:
            message = "Missing name or photo!"
        else:
            path = save_image(file, name)
            print(f"[INFO] Saved new enrollment photo for {name}: {path}")
            # rebuild encodings
            global known_encodings, known_names
            known_encodings, known_names = build_encodings()
            message = f"✅ Successfully enrolled {name}!"
    faces = [(os.path.splitext(f)[0], f) for f in os.listdir(ENROLLED_DIR)
             if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    return render_template_string(HTML_TEMPLATE, message=message, faces=faces)

@app.route("/recognize", methods=["POST"])
def recognize():
    img_bytes = request.get_data()
    if not img_bytes:
        return jsonify({"error":"no image data"}), 400
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.save("last_upload.jpg")
        print("[DEBUG] Saved test frame as last_upload.jpg")

    except Exception as e:
        return jsonify({"error":"bad image"}), 400
    img_np = np.array(img)
    face_locs = face_recognition.face_locations(img_np)
    face_encs = face_recognition.face_encodings(img_np, face_locs)
    if len(face_encs) == 0:
        print("[INFO] No face detected")
        return jsonify({"result":"no_face"})
    for enc in face_encs:
        distances = face_recognition.face_distance(known_encodings, enc) if known_encodings else []
        if len(distances) > 0:
            best_idx = int(np.argmin(distances))
            best_dist = float(distances[best_idx])
            if best_dist <= TOLERANCE:
                name = known_names[best_idx]
                print("Person identified\n")
                print("door unlocked") 
                return jsonify({"result":"known","name":name})
    print("[ALERT] Unknown person detected")
    return jsonify({"result":"unknown"})

# Serve static enrolled images
app.static_folder = ENROLLED_DIR

# ------------------- MAIN ----------------------
if __name__ == "__main__":
    print("[INFO] Starting Smart Door Lock Server")
    print(f"[INFO] Access the web interface at port: {PORT}/enroll")
    app.run(host="0.0.0.0", port=PORT, debug=False)
