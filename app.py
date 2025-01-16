from flask import Flask, request, jsonify, render_template
import cv2
import face_recognition
import numpy as np
import mysql.connector
import base64

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "face_recognition_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    image_data = request.form.get("image")

    if not username or not image_data:
        return jsonify({"error": "Nombre de usuario e imagen son obligatorios"}), 400

    img_data = base64.b64decode(image_data.split(",")[1])
    np_image = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        return jsonify({"error": "No se detectaron rostros válidos"}), 400

    encoding = face_encodings[0]
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, encoding) VALUES (%s, %s)",
            (username, encoding.tobytes())
        )
        conn.commit()
        conn.close()
        return jsonify({"message": f"Usuario {username} registrado exitosamente", "vector": encoding.tolist()}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    image_data = request.form.get("image")

    if not image_data:
        return jsonify({"error": "La imagen es obligatoria"}), 400

    img_data = base64.b64decode(image_data.split(",")[1])
    np_image = np.frombuffer(img_data, np.uint8)
    frame = cv2.imdecode(np_image, cv2.IMREAD_COLOR)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, encoding FROM users")
    users = cursor.fetchall()
    conn.close()

    known_encodings = [np.frombuffer(user[1], dtype=np.float64) for user in users]
    known_usernames = [user[0] for user in users]

    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    if not face_encodings:
        return jsonify({"error": "No se detectaron rostros válidos"}), 400

    face_encoding = face_encodings[0]
    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
    distances = face_recognition.face_distance(known_encodings, face_encoding)

    if True in matches:
        best_match_index = np.argmin(distances)
        username = known_usernames[best_match_index]
        return jsonify({"message": f"Bienvenido, {username}", "vector": face_encoding.tolist()}), 200

    return jsonify({"error": "Usuario no reconocido"}), 401

if __name__ == "__main__":
    app.run(debug=True)