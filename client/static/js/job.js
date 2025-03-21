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
            case job.status.includes('done_colmap'):
                updateButtons(true, true, false, false, false, false)
                break;
            case job.status.includes('done_mcmc'):
                updateButtons(true, true, true, false, false, false)
                break;
            case job.status.includes('done_segmentation_preparation'):
                updateButtons(true, true, true, true, false, false)
                break;
            case job.status.includes('done_gaussian_segmentation'):
                updateButtons(true, true, true, true, true, false)
                break;
            case job.status.includes('done_frosting'):
                updateButtons(true, true, true, true, true, true)
                break;
            case job.status.includes('failed_colmap'):
                updateButtons(true, false, false, false, false, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('failed_mcmc'):
                updateButtons(true, true, false, false, false, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('failed_segmentation_preparation'):
                updateButtons(true, true, true, false, false, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('failed_gaussian_segmentation'):
                updateButtons(true, true, true, true, false, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('failed_frosting'):
                updateButtons(true, true, true, true, true, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('running'):
                updateButtons(false, false, false, false, false, false)
                clearSegmentationContainer()
                break;
            case job.status.includes('failed'):
                updateButtons(true, true, true, true, true, true)
                clearSegmentationContainer()
                break;
            case job.status.includes('removed_job_queue'):
                updateButtons(true, true, true, true, true, true)
                clearSegmentationContainer()
                break;
            case job.status.includes('job_queued'):
                clearSegmentationContainer()
                break;
        }

        jobInfo.innerHTML = `
            <p><strong>Job-ID:</strong> ${job.id}</p>
            <p><strong>Projektname:</strong> ${job.project_name}</p>
            <p><strong>Status:</strong> ${job.status}</p>
            <p><strong>Queued Processes:</strong> ${job.queued_processes}</p>
        `;

        setTimeout(fetchAndUpdateDetails, 5000);
    }

    fetchAndUpdateDetails()
}

function pollJobLog(jobId) {
    async function fetchAndUpdateLog() {
        const response = await fetch(`/jobs/${jobId}/logs`);
        const logText = await response.text();

        const logElement = document.getElementById("jobLog");
        const isScrolledToBottom = logElement.scrollHeight - logElement.scrollTop <= logElement.clientHeight + 5;
        logElement.innerText = logText;

        if (isScrolledToBottom) {
            logElement.scrollTop = logElement.scrollHeight;
        }

        setTimeout(fetchAndUpdateLog, 5000);
    }

    fetchAndUpdateLog();
}

function updateButtons(colmap, mcmc, segPrep, segmentation, frosting, download) {
    const colmapButton = document.getElementById('colmapButton');
    const mcmcButton = document.getElementById('mcmcButton');
    const segPrepButton = document.getElementById('segPrepButton');
    const showSegmentationImageButton = document.getElementById('showSegmentationImageButton');
    const frostingWholeButton = document.getElementById('frostingWholeButton');
    const frostingSegButton = document.getElementById('frostingSegButton');
    const downloadButton = document.getElementById('downloadButton');

    colmapButton.style.display = colmap ? 'block' : 'none';
    mcmcButton.style.display = mcmc ? 'block' : 'none';
    segPrepButton.style.display = segPrep ? 'block' : 'none';
    showSegmentationImageButton.style.display = segmentation ? 'block' : 'none';
    frostingWholeButton.style.display = frosting ? 'block' : 'none';
    frostingSegButton.style.display = frosting ? 'block' : 'none';
    downloadButton.style.display = download ? 'block' : 'none';
}

function clearSegmentationContainer() {
    document.getElementById('segmentationContainer').innerHTML = `
    <canvas id="promptImageCanvas"></canvas>
    <div id="previewContainer"></div>
    <button id="confirmButton" style="display:none;" onclick="confirmSegmentation()">Confirm Segmentation</button>
`;
}

async function startColmap() {
    const response = await fetch(`/jobs/${jobId}/colmap`, {method: 'POST'});

    if (!response.ok){
        alert("Something went wrong on queueing Colmap-Process!");
        return;
    }

    alert('Colmap-Process queued!');
}

async function startMCMC() {
    const response = await fetch(`/jobs/${jobId}/mcmc`, {method: 'POST'});

    if (!response.ok){
        alert("Something went wrong on queueing MCMC-Process!");
        return;
    }

    alert('MCMC-Process queued!');
}

async function startSegPrep() {
    const response = await fetch(`/jobs/${jobId}/segmentationPreparation`, {method: 'POST'});

    if (!response.ok){
        alert("Something went wrong on queueing Segmentation_Preparation-Process!");
        return;
    }

    alert('Segmentation_Preparation-Process queued!');
}

async function startFrostingWhole() {
    const response = await fetch(`/jobs/${jobId}/frosting_whole`, {method: 'POST'});

    if (!response.ok){
        alert("Something went wrong on queueing Frosting-Process!");
        return;
    }

    alert('Frosting-Process queued!');
}

async function startFrostingSeg() {
    const response = await fetch(`/jobs/${jobId}/frosting_seg`, {method: 'POST'});

    if (!response.ok){
        alert("Something went wrong on queueing Frosting-Process!");
        return;
    }

    alert('Frosting-Process queued!');
}

async function downloadResult() {
    alert('Download started, could take a while over SSH, please be patient!')

    const response = await fetch(`/jobs/${jobId}/download`, { method: 'GET' });

    if (!response.ok) {
        console.error("Download request failed.");
        return;
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${jobId}_result.zip`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}