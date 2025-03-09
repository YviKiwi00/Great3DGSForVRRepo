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

        switch (true) {
            case job.status.includes('done'):
                updateButtons(true, true, true, false, false)
                break;
            case job.status.includes('failed'):
                updateButtons(true, true, true, false, false)
                break;
            case job.status.includes('ready_for_segmentation'):
                updateButtons(true, true, true, true, false)
                break;
            case job.status.includes('running'):
                updateButtons(false, false, false, false, false)
                document.getElementById('segmentationContainer').innerHTML = '';
                break;
            case job.status.includes('final_result_ready'):
                updateButtons(true, true, true, true, true)
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

function updateButtons(colmap, mcmc, segPrep, segmentation, download) {
    const colmapButton = document.getElementById('colmapButton');
    const mcmcButton = document.getElementById('mcmcButton');
    const segPrepButton = document.getElementById('segPrepButton');
    const showSegmentationImageButton = document.getElementById('showSegmentationImageButton');
    const downloadButton = document.getElementById('downloadButton');

    colmapButton.style.display = colmap ? 'block' : 'none';
    mcmcButton.style.display = mcmc ? 'block' : 'none';
    segPrepButton.style.display = segPrep ? 'block' : 'none';
    showSegmentationImageButton.style.display = segmentation ? 'block' : 'none';
    downloadButton.style.display = download ? 'block' : 'none';
}

async function startColmap() {
    const response = await fetch(`/jobs/${jobId}`);
    const job = await response.json();

    if (job.status.includes('running')) {
        alert('There is still a Job running, please wait.');
        return;
    }
    await fetch(`/jobs/${jobId}/colmap`, {method: 'POST'});
    alert('Colmap-Process started!');
}

async function startMCMC() {
    const response = await fetch(`/jobs/${jobId}`);
    const job = await response.json();

    if (job.status.includes('running')) {
        alert('There is still a Job running, please wait.');
        return;
    }
    await fetch(`/jobs/${jobId}/mcmc`, {method: 'POST'});
    alert('MCMC-Process started!');
}

async function startSegPrep() {
    const response = await fetch(`/jobs/${jobId}`);
    const job = await response.json();

    if (job.status.includes('running')) {
        alert('There is still a Job running, please wait.');
        return;
    }
    await fetch(`/jobs/${jobId}/segmentationPreparation`, {method: 'POST'});
    alert('Segmentation_Preparation-Process started!');
}

function downloadResult() {
    const jobId = new URLSearchParams(window.location.search).get('id');
    window.location.href = `/jobs/${jobId}/downloadResult`;
}