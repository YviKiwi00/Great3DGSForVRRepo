const jobId = new URLSearchParams(window.location.search).get('id');
const canvas = document.getElementById('promptImageCanvas');
const ctx = canvas.getContext('2d');

let currentImage = null
let selectedPoint = null;

async function loadPromptImage() {
    const response = await fetch(`/jobs/${jobId}/segmentationPromptImage`);
    const blob = await response.blob();

    const imgURL = URL.createObjectURL(blob);

    const img = new Image();
    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        currentImage = img

        requestAnimationFrame(() => {
            ctx.drawImage(currentImage, 0, 0);
        });

        setTimeout(() => {
            URL.revokeObjectURL(imgURL);
        }, 5000);
    };

    img.src = imgURL;

    canvas.onclick = (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        selectedPoint = {x, y};

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(currentImage, 0, 0);

        drawPoint(x, y);
        sendPointToServer(x, y);

        alert('Segmentation-Prompt send! Do not select another prompt till preview is back!');
    };
}

function drawPoint(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
}

async function sendPointToServer(x, y) {
    clearPreviews();
    const response = await fetch(`/jobs/${jobId}/segmentationPrompt`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x, y})
    });
    const data = await response.json();
    showPreviews(data.previews);
}

function showPreviews(previews) {
    clearPreviews();
    console.log("Showing Previews!");
    const container = document.getElementById('previewContainer');
    previews.forEach((base64, index) => {
        const img = new Image();
        img.src = `data:image/png;base64,${base64}`;
        container.appendChild(img);
    });
    document.getElementById('confirmButton').style.display = 'block';
}

function clearPreviews() {
    console.log("Clearing Previews!");
    const container = document.getElementById('previewContainer');
    container.innerHTML = '';
    document.getElementById('confirmButton').style.display = 'none';
}

async function confirmSegmentation() {
    const response = await fetch(`/jobs/${jobId}/confirmSegmentation`, {method: 'POST'});

    if (response.ok) {
        alert("Segmentierung bestätigt!");
        document.getElementById('confirmButton').style.display = 'none';
        document.getElementById('previewContainer').innerHTML = '';
    } else {
        alert("Fehler bei der Bestätigung.");
    }
}