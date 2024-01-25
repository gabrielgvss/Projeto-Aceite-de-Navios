document
    .getElementById("toggle-btn")
    .addEventListener("click", function () {
        document.querySelector(".sidebar").classList.toggle("active");
        document.querySelector(".menutoggle").classList.toggle("active")
    });