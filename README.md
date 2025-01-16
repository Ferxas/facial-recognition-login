# Facial Recognition with Flask and MySQL

This project implements *too simple basic* facial recognition system using Flask for the backend and MySQL as the database. Users can register and log in using their faces, with support for webcam integration and frontend interactions via HTML, CSS, and JavaScript.

## Features

- **User Registration**: Capture a user's face via webcam, encode it, and store it in the database.
- **Login Authentication**: Authenticate users by matching their facial encoding with the stored data.
- **Frontend Integration**: Interact with the system through a web interface using HTML, CSS, and JavaScript.
- **Database**: Store user information and facial encodings in MySQL.
- **Face Recognition**: Use the `face_recognition` library for detecting and encoding faces.

## Requirements

- Python 3.7+
- MySQL Server
- Node.js (for serving frontend, optional)
- Web browser with webcam access

### Python Dependencies

Install the required Python libraries:

```bash
pip install flask face_recognition opencv-python numpy mysql-connector-python 
```

or 

```
pip install -r requirements.txt
```

### Database Setup

1. Start your MySQL server.
2. Create the database and table:

```sql
CREATE DATABASE face_recognition_db;

USE face_recognition_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    encoding BLOB NOT NULL
);
```

## Project Structure

```
project/
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
├── templates/
│   └── index.html
├── app.py
├── desktop_local.py
├── requirements.txt
└── README.md
```

## Running the Project

1. Clone this repository:

```bash
git clone https://github.com/ferxas/facial-recognition-login.git
cd facial-recognition-flask
```

2. Start the Flask server:

```bash
python app.py
```

3. Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

## Endpoints

### 1. `POST /register`

**Description**: Register a new user by capturing their face and storing their facial encoding in the database.

- **Parameters**: 
  - `username`: The username to register.
  - `image`: A base64-encoded image of the user's face.

- **Response**:
  ```json
  {
    "message": "Usuario test_user registrado exitosamente",
    "vector": [encoding array]
  }
  ```

### 2. `POST /login`

**Description**: Authenticate a user by matching their facial encoding with stored data.

- **Parameters**: 
  - `image`: A base64-encoded image of the user's face.

- **Response**:
  ```json
  {
    "message": "Bienvenido, test_user",
    "vector": [encoding array]
  }
  ```

## Frontend Integration

The frontend is implemented using HTML, CSS, and JavaScript. It captures the video feed from the user's webcam and sends images to the Flask backend for processing.

### Key Features:

- **Live Webcam Feed**: Uses the browser's MediaDevices API to display the webcam feed.
- **Base64 Image Encoding**: Converts captured frames into base64 format for backend transmission.

### Running the Frontend

1. Ensure the Flask server is running.
2. Access the frontend via:

```
http://127.0.0.1:5000
```

## Troubleshooting

- **Camera Access Denied**: Ensure your browser has permission to access the webcam.
- **Face Not Detected**: Ensure proper lighting and that the user's face is clearly visible to the camera.
- **MySQL Connection Errors**: Verify that MySQL server is running and the credentials in `app.py` are correct.

## Contributing

Feel free to fork this repository and submit pull requests with improvements or bug fixes.
(For some reason the vector drawing works on the desktop, but I couldn't replicate it for the web version).