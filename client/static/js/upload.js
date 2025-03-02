function startUpload() {
    const files = document.getElementById('fileInput').files;
    const projectName = document.getElementById('projectName').value || "UnnamedProject";

    if (files.length === 0) {
        document.getElementById('uploadStatus').innerText = "Bitte mindestens eine Datei auswählen.";
        return;
    }

    const formData = new FormData();
    formData.append('projectName', projectName);

    for (let file of files) {
        formData.append('files', file);
    }

    fetch('/imageUpload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.job_id) {
            document.getElementById('uploadStatus').innerText = `Upload erfolgreich! Job-ID: ${data.job_id}`;
            setTimeout(() => {
                window.location.href = `jobs.html`;
            }, 2000);
        } else {
            document.getElementById('uploadStatus').innerText = "Upload fehlgeschlagen.";
        }
    })
    .catch(error => {
        console.error('Error during upload:', error);
        document.getElementById('uploadStatus').innerText = "Fehler beim Upload.";
    });
}