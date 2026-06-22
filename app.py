from flask import Flask, request, render_template_string, Response, redirect, session, send_from_directory, make_response
from groq import Groq
import base64, cv2, os, datetime, uuid
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = "secret123"

# =============================
# GROQ API
# =============================
client = Groq(api_key="YOUR GROQ API KEY")

# =============================
# ADMIN USERS
# =============================
admins = {"admin": "1234"}

# =============================
# STORAGE
# =============================
gallery = []
logs = []
notifications_enabled = True
os.makedirs("uploads", exist_ok=True)

# =============================
# LIVE CAMERA STREAM
# =============================
camera = cv2.VideoCapture(0)

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' +
                   frame_bytes + b'\r\n')

def capture_frame():
    success, frame = camera.read()
    if success:
        filename = f"{uuid.uuid4().hex}.jpg"
        path = os.path.join("uploads", filename)
        cv2.imwrite(path, frame)
        return path
    return None

# =============================
# HELPER FUNCTIONS
# =============================
def classify_detection(result):
    text = result.lower()
    if any(x in text for x in ["poaching","gun","deforestation","cutting"]):
        return "Threat"
    elif any(x in text for x in ["human","person","man","intruder"]):
        return "Human"
    else:
        return "Animal"

def get_safety_level(result):
    text = result.lower()
    if any(x in text for x in ["attack","danger","tiger","lion","snake","poaching","gun"]):
        return "DANGER"
    elif "human" in text:
        return "WARNING"
    else:
        return "SAFE"

def is_alert(result):
    return get_safety_level(result) == "DANGER"

# =============================
# AI FUNCTIONS
# =============================
def detect_image(path, mode):
    with open(path, "rb") as img:
        base64_image = base64.b64encode(img.read()).decode("utf-8")

    if mode == "tourist":
        prompt = "Identify the animal, plant, or tree. Reply with only its NAME, no sentences."
    else:
        prompt = "Identify species, humans, or threats. Reply with NAME only if it's animal/plant/tree. Include ALERT if danger."

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role":"user",
            "content":[
                {"type":"text","text":prompt},
                {"type":"image_url", "image_url":{"url":f"data:image/jpeg;base64,{base64_image}"}}
            ]
        }]
    )
    return response.choices[0].message.content.strip().split("\n")[0]

def get_species_info_ai(species):
    prompt = f"""
Provide details about {species}.

Format EXACTLY like:

Here are the details about {species}:

SCIENTIFIC NAME:
HABITAT:
DIET:
BEHAVIOR:
CONSERVATION STATUS:

Each heading must start on a new line.
"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role":"user","content":prompt}]
    )

    text = response.choices[0].message.content
    headings = ["SCIENTIFIC NAME:", "HABITAT:", "DIET:", "BEHAVIOR:", "CONSERVATION STATUS:"]
    for h in headings:
        text = text.replace(h, "\n" + h)
    return text

# =============================
# HTML CONTENT
# =============================
with open("index.html", "r", encoding="utf-8") as f:
    FRONTEND_HTML = f.read()

# =============================
# ROUTES
# =============================
@app.route("/", methods=["GET","POST"])
def login():
    error = ""
    if request.method=="POST":
        mode = request.form["mode"]
        user = request.form.get("username")
        if mode=="admin":
            if user in admins and admins[user]==request.form["password"]:
                session["user"] = user
                session["mode"] = mode
                return redirect("/dashboard")
            else:
                error="Invalid credentials"
        else:
            session["user"]=user
            session["mode"]=mode
            return redirect("/dashboard")
    return render_template_string(FRONTEND_HTML, error=error, page="login")

@app.route("/dashboard")
def dashboard():
    return render_template_string(FRONTEND_HTML, user=session.get("user"), mode=session.get("mode"), page="dashboard")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/detect_image_page", methods=["GET","POST"])
def detect_image_page():
    result = ""
    safety = ""
    filename = None
    if request.method=="POST":
        file = request.files.get("file")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        location = f"{lat}, {lon}" if lat and lon else "Unknown"
        if file:
            filename = f"{uuid.uuid4().hex}.jpg"
            path = os.path.join("uploads", filename)
            file.save(path)
            result = detect_image(path, session.get("mode"))
            safety = get_safety_level(result)
            gallery.append({"file": filename})
            logs.append({
                "user": session.get("user") if session.get("mode")=="admin" else "",
                "time": str(datetime.datetime.now()),
                "image": filename,
                "result": result,
                "location": location
            })
    return render_template_string(FRONTEND_HTML, result=result, safety=safety, filename=filename, page="detect_image")

@app.route("/detect_video_page", methods=["GET","POST"])
def detect_video_page():
    result = ""
    safety = ""
    video_filename = None
    if request.method=="POST":
        file = request.files.get("file")
        lat = request.form.get("lat")
        lon = request.form.get("lon")
        location = f"{lat}, {lon}" if lat and lon else "Unknown"
        if file:
            video_filename = f"{uuid.uuid4().hex}.mp4"
            path = os.path.join("uploads", video_filename)
            file.save(path)
            cap = cv2.VideoCapture(path)
            ret, frame = cap.read()
            cap.release()
            if ret:
                frame_file = f"{uuid.uuid4().hex}.jpg"
                frame_path = os.path.join("uploads", frame_file)
                cv2.imwrite(frame_path, frame)
                result = detect_image(frame_path, session.get("mode"))
                safety = get_safety_level(result)
                logs.append({
                    "user": session.get("user") if session.get("mode")=="admin" else "",
                    "time": str(datetime.datetime.now()),
                    "image": frame_file,
                    "result": result,
                    "location": location
                })
    return render_template_string(FRONTEND_HTML, video_filename=video_filename, result=result, safety=safety, page="detect_video")

@app.route("/detect_live_page", methods=["GET","POST"])
def detect_live_page():
    global camera
    result = None
    safety = None
    filename = None

    if not camera.isOpened():
        camera = cv2.VideoCapture(0)

    if request.method == "POST":
        if "capture" in request.form:
            path = capture_frame()
            if path:
                result = detect_image(path, session.get("mode"))
                safety = get_safety_level(result)
                filename = os.path.basename(path)
                logs.append({
                    "user": session.get("user") if session.get("mode")=="admin" else "",
                    "time": str(datetime.datetime.now()),
                    "image": filename,
                    "result": result,
                    "location": "Live Camera"
                })
        if "exit" in request.form:
            camera.release()
            return redirect("/dashboard")
    return render_template_string(FRONTEND_HTML, result=result, safety=safety, filename=filename, page="detect_live")

@app.route("/species_info_page", methods=["GET","POST"])
def species_info_page():
    info=""
    if request.method=="POST":
        species=request.form["species"]
        info=get_species_info_ai(species)
    return render_template_string(FRONTEND_HTML, info=info, page="species_info")

@app.route("/gallery")
def gallery_page():
    return render_template_string(FRONTEND_HTML, gallery=gallery, page="gallery")

@app.route("/logs")
def logs_page():
    return render_template_string(FRONTEND_HTML, logs=logs, page="logs")

@app.route("/alerts")
def alerts_page():
    if session.get("mode") != "admin": return "Access Denied"
    danger_logs = [log for log in logs if get_safety_level(log["result"])=="DANGER"]
    return render_template_string(FRONTEND_HTML, danger_logs=danger_logs, page="alerts")

@app.route("/export_option", methods=["GET","POST"])
def export_logs():
    if session.get("mode") != "admin": return "Access Denied"

    if request.method == "POST":
        format_type = request.form.get("format")
        if format_type == "CSV":
            from io import StringIO
            import csv
            si = StringIO()
            cw = csv.writer(si)
            cw.writerow(["Time","User","Location","Result","Image"])
            for log in logs:
                cw.writerow([log["time"], log.get("user",""), log["location"], log["result"], log["image"]])
            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=logs.csv"
            output.headers["Content-type"] = "text/csv"
            return output
        elif format_type == "PDF":
            from io import BytesIO
            from flask import send_file

            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            y = height - 50
            c.setFont("Helvetica", 12)
            for log in logs:
                c.drawString(30, y, f"Time: {log['time']}, User: {log.get('user','')}, Location: {log['location']}, Result: {log['result']}, Image: {log['image']}")
                y -= 20
                if y < 50:
                    c.showPage()
                    y = height - 50
            c.save()
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name="logs.pdf",
                mimetype="application/pdf"
            )

    return render_template_string(FRONTEND_HTML, page="export_option")

@app.route("/settings", methods=["GET","POST"])
def settings_page():
    global notifications_enabled
    if session.get("mode") != "admin": return "Access Denied"
    if request.method=="POST":
        notifications_enabled = "notify" in request.form
    return render_template_string(FRONTEND_HTML, notifications_enabled=notifications_enabled, page="settings")

@app.route("/users", methods=["GET","POST"])
def user_management_page():
    if session.get("mode") != "admin": return "Access Denied"
    message = ""
    if request.method=="POST":
        if "remove_user" in request.form:
            user_to_remove = request.form["remove_user"]
            admins.pop(user_to_remove, None)
            message = f"Removed user: {user_to_remove}"
        elif "new_user" in request.form and "new_pass" in request.form:
            new_user = request.form["new_user"].strip()
            new_pass = request.form["new_pass"].strip()
            if new_user in admins:
                message = f"User {new_user} already exists!"
            elif new_user and new_pass:
                admins[new_user] = new_pass
                message = f"Added user: {new_user}"
    return render_template_string(FRONTEND_HTML, admins=admins, message=message, page="users")

@app.route("/help")
def help_page():
    return render_template_string(FRONTEND_HTML, page="help")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory("uploads", filename)

# =============================
# RUN APP
# =============================
if __name__=="__main__":
    app.run(debug=True)
