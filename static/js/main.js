const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const responseDiv = document.getElementById("response");

navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((error) => {
        console.error("No se pudo acceder a la cámara:", error);
    });

function captureImage() {
    const context = canvas.getContext("2d");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL("image/jpeg");
}

async function register() {
    const username = document.getElementById("register-username").value;
    const image = captureImage();

    const formData = new FormData();
    formData.append("username", username);
    formData.append("image", image);

    try {
        const response = await fetch("/register", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();
        responseDiv.textContent = result.message || result.error;
    } catch (error) {
        console.error(error);
        responseDiv.textContent = "Error durante el registro.";
    }
}

async function login() {
    const image = captureImage();

    const formData = new FormData();
    formData.append("image", image);

    try {
        const response = await fetch("/login", {
            method: "POST",
            body: formData,
        });
        const result = await response.json();
        responseDiv.textContent = result.message || result.error;
    } catch (error) {
        console.error(error);
        responseDiv.textContent = "Error durante el inicio de sesión.";
    }
}