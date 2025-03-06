document.addEventListener("DOMContentLoaded", async () => {
    const params = new URLSearchParams(window.location.search);
    const jobId = params.get("id");

    pollJobDetails(jobId);
    pollJobLog(jobId);
});

function pollJobDetails(jobId) {
    const jobInfo = document.getElementById("jobInfo");

    async function fetchAndUpdateDetails() {
        const response = await fetch(`/jobs/${jobId}`);
        const job = await response.json();

        switch (job.status) {
            case 'ready_for_segmentation':
                document.getElementById('showSegmentationImage').style.display = 'block';
                break;
            case 'awaiting_final_processing':
                document.getElementById('showSegmentationImage').style.display = 'none';
                document.getElementById('segmentationContainer').innerHTML = '';
                break;
            case 'final_result_ready':
                document.getElementById('downloadButton').style.display = 'block';
                break;
        }

        jobInfo.innerHTML = `
            <p><strong>Job-ID:</strong> ${job.id}</p>
            <p><strong>Projektname:</strong> ${job.project_name}</p>
            <p><strong>Status:</strong> ${job.status}</p>
        `;

        setTimeout(fetchAndUpdateDetails, 5000);  // alle 5 Sekunden
    }

    fetchAndUpdateDetails()
}

function pollJobLog(jobId) {
    async function fetchAndUpdateLog() {
        const response = await fetch(`/jobs/${jobId}/logs`);
        const logText = await response.text();

        const logElement = document.getElementById("jobLog");
        logElement.innerText = logText;

        logElement.scrollTop = logElement.scrollHeight;

        setTimeout(fetchAndUpdateLog, 5000);  // alle 5 Sekunden
    }

    fetchAndUpdateLog();
}

function downloadResult() {
    const jobId = new URLSearchParams(window.location.search).get('id');
    window.location.href = `/jobs/${jobId}/downloadResult`;
}