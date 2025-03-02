const jobId = new URLSearchParams(window.location.search).get('id');
const canvas = document.getElementById('promptImageCanvas');
const ctx = canvas.getContext('2d');

let currentImage = null
let selectedPoint = null;

async function loadPromptImage() {
    const response = await fetch(`/jobs/${jobId}/segmentationPromptImage`);
    const blob = await response.blob();
    const img = new Image();

    img.onload = () => {
        canvas.width = img.width;
        canvas.height = img.height;
        currentImage = img

        ctx.drawImage(currentImage, 0, 0);
    };
    img.src = URL.createObjectURL(blob);

    canvas.onclick = (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        selectedPoint = {x, y};

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(currentImage, 0, 0);

        drawPoint(x, y);
        sendPointToServer(x, y);
    };
}

function drawPoint(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = 'red';
    ctx.fill();
}

async function sendPointToServer(x, y) {
    const response = await fetch(`/jobs/${jobId}/segmentationPrompt`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x, y})
    });
    const data = await response.json();
    showPreviews(data.previews);
}

function showPreviews(previews) {
    const container = document.getElementById('previewContainer');
    container.innerHTML = '';
    previews.forEach((base64, index) => {
        const img = new Image();
        img.src = `data:image/png;base64,${base64}`;
        container.appendChild(img);
    });
    document.getElementById('confirmButton').style.display = 'block';
}

async function confirmSegmentation() {
    alert("Hier käme später der Call für 'confirmSegmentation'!");
}

loadPromptImage();