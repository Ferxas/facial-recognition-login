import cv2
import os
import sqlite3
import face_recognition
import numpy as np

haarcascade_path = "haarcascade/haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(haarcascade_path)
dataset_path = "dataset"
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)

db_path = "users.db"

def initialize_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            encoding BLOB NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def register_user(username):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("[INFO] Capturando imágenes para el usuario:", username)
    cap = cv2.VideoCapture(0)
    encodings = []
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] No se pudo acceder a la cámara.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")

        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            encodings.extend(face_encodings)  # Add all codifications

            # Drawing vectors (squares or triangles)
            for (top, right, bottom, left) in face_locations:
                count += 1
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.putText(frame, f"Imagen {count}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

        cv2.imshow("Capturando Rostros", frame)
        if count >= 20 or cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if encodings:
        average_encoding = np.mean(encodings, axis=0)
        cursor.execute("INSERT INTO users (username, encoding) VALUES (?, ?)",
                       (username, sqlite3.Binary(average_encoding.tobytes())))
        conn.commit()
        print("[INFO] Usuario registrado exitosamente:", username)
    else:
        print("[ERROR] No se capturaron rostros válidos.")
    conn.close()

def login_user():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT username, encoding FROM users")
    users = cursor.fetchall()
    conn.close()

    known_encodings = [np.frombuffer(user[1], dtype=np.float64) for user in users]
    known_usernames = [user[0] for user in users]

    print("[INFO] Iniciando sesión...")
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] No se pudo acceder a la cámara.")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")  # detect locations

        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                distances = face_recognition.face_distance(known_encodings, face_encoding)

                if True in matches:
                    best_match_index = np.argmin(distances)
                    username = known_usernames[best_match_index]
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f"Bienvenido: {username}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                else:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.putText(frame, "Desconocido", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Reconocimiento Facial", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

initialize_db()

while True:
    print("1. Registrar Usuario")
    print("2. Iniciar Sesión")
    print("3. Salir")
    choice = input("Selecciona una opción: ")

    if choice == "1":
        username = input("Introduce un nombre de usuario: ")
        register_user(username)
    elif choice == "2":
        login_user()
    elif choice == "3":
        break
    else:
        print("[ERROR] Opción inválida. Intenta de nuevo.")
