// Get the login form
const loginForm = document.querySelector("form");

if (loginForm) {

    loginForm.addEventListener("submit", function(event) {

        // Prevent the form from refreshing the page
        event.preventDefault();

        // Get email and password
        const email = document.querySelector('input[type="email"]').value;
        const password = document.querySelector('input[type="password"]').value;

        // Get the role from the URL
        const params = new URLSearchParams(window.location.search);
        const role = params.get("role");

        // Temporary login validation
        if (email === "" || password === "") {
            alert("Please enter email and password.");
            return;
        }

        // Redirect based on role
        if (role === "student") {

            window.location.href = "student-dashboard.html";

        } else if (role === "admin") {

            window.location.href = "admin-dashboard.html";

        } else {

            alert("Invalid login type.");

        }

    });

}