document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll("nav a");
    const current = window.location.pathname.split("/").pop();

    links.forEach(link => {
        if (link.getAttribute("href") === current) {
            link.style.textDecoration = "underline";
            link.style.color = "var(--highlight)";
        }
    });
});