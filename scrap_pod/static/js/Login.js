document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById("myModal");
    const btn = document.querySelector("button[type='submit']");
    const span = document.getElementsByClassName("close")[0];
    const form = document.getElementById("loginForm");

    form.onsubmit = function(event) {
        event.preventDefault();
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (email && password) {
            modal.style.display = "block";
        }
    }

    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});