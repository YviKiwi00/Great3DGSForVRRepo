document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get("id");

    document.getElementById("jobInfo").innerHTML = `<p>Job ID: ${jobId}</p><p>Status: running</p>`;
    document.getElementById("jobLog").innerText = "Hier könnte ihr Log stehen...";
});

function downloadResult() {
    alert('Download wird später hier gestartet');
}