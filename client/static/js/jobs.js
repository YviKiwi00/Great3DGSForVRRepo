document.addEventListener("DOMContentLoaded", async () => {
    const table = document.getElementById("jobTable").querySelector("tbody");
    table.innerHTML = "";

    const response = await fetch('/jobs');
    const jobs = await response.json();

    jobs.forEach(job => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${job.id}</td><td>${job.project_name}</td><td>${job.status}</td>`;
        row.onclick = () => {
            window.location.href = `job.html?id=${job.id}`;
        };
        table.appendChild(row);
    });
});