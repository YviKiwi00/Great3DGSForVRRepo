document.addEventListener("DOMContentLoaded", async () => {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get("id");

    loadJobDetails(jobId);
    pollJobLog(jobId);
});

async function loadJobDetails(jobId) {
    const response = await fetch(`/jobs/${jobId}`);
    const job = await response.json();

    const jobInfo = document.getElementById("jobInfo");
    jobInfo.innerHTML = `
        <p><strong>Job-ID:</strong> ${job.id}</p>
        <p><strong>Projektname:</strong> ${job.project_name}</p>
        <p><strong>Status:</strong> ${job.status}</p>
    `;
}

function pollJobLog(jobId) {
    async function fetchAndUpdateLog() {
        const response = await fetch(`/jobs/${jobId}/logs`);
        const logText = await response.text();
        document.getElementById("jobLog").innerText = logText;

        setTimeout(fetchAndUpdateLog, 5000);  // alle 5 Sekunden
    }

    fetchAndUpdateLog();
}

function downloadResult() {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get("id");
    window.location.href = `/jobs/${jobId}/downloadResult`;
}