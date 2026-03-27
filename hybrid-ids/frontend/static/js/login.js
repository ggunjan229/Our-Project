// =======================
// SIGNUP FUNCTION
// =======================
function signup(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;
    const confirm = document.getElementById("confirmPassword").value;

    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const confirmError = document.getElementById("confirmError");

    emailError.textContent = "";
    passwordError.textContent = "";
    confirmError.textContent = "";

    let valid = true;

    // ✅ Email validation
    if (!email.includes("@")) {
        emailError.textContent = "Enter valid email";
        valid = false;
    }

    // ✅ Strong password validation
    const strongPassword = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[\W]).{8,}$/;

    if (!strongPassword.test(password)) {
        passwordError.textContent =
            "Min 8 chars, 1 uppercase, 1 number, 1 special char";
        valid = false;
    }

    // ✅ Confirm password
    if (password !== confirm) {
        confirmError.textContent = "Passwords do not match";
        valid = false;
    }

    if (!valid) return;

    let users = JSON.parse(localStorage.getItem("users")) || [];

    // 🔴 FIX: Case-insensitive email check
    const exists = users.some(u => u.email.toLowerCase() === email);

    if (exists) {
        emailError.textContent = "User already exists";
        return;
    }

    // ✅ Save user
    users.push({ email, password });
    localStorage.setItem("users", JSON.stringify(users));

    // ✅ IMPORTANT: Clear old session (prevents bug)
    localStorage.removeItem("loggedInUser");

    // ✅ Redirect to login
    window.location.href = "login.html";
}


// =======================
// LOGIN FUNCTION
// =======================
function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value.trim().toLowerCase();
    const password = document.getElementById("password").value;
    const error = document.getElementById("loginError");

    error.textContent = "";

    let users = JSON.parse(localStorage.getItem("users")) || [];

    const user = users.find(
        u => u.email.toLowerCase() === email && u.password === password
    );

    if (!user) {
        error.textContent = "Invalid email or password";
        return;
    }

    // ✅ Save session
    localStorage.setItem("loggedInUser", email);

    // ✅ Redirect to main page
    window.location.href = "index.html";
}


// =======================
// AUTH CHECK (VERY IMPORTANT)
// =======================
function checkAuth() {
    const user = localStorage.getItem("loggedInUser");

    if (!user) {
        window.location.href = "login.html";
    }
}


// =======================
// LOGOUT FUNCTION
// =======================
function logout() {
    localStorage.removeItem("loggedInUser");
    window.location.href = "login.html";
}


// =======================
// RESET PASSWORD (SIMULATED)
// =======================
function resetPassword() {
    const email = document.getElementById("resetEmail").value.trim().toLowerCase();
    const msg = document.getElementById("resetMsg");

    msg.textContent = "";

    let users = JSON.parse(localStorage.getItem("users")) || [];

    const user = users.find(u => u.email.toLowerCase() === email);

    if (!user) {
        msg.style.color = "red";
        msg.textContent = "Email not found";
        return;
    }

    msg.style.color = "lightgreen";
    msg.textContent = "Reset link sent (simulated)";
}


// =======================
// TOGGLE PASSWORD
// =======================
function togglePassword() {
    const password = document.getElementById("password");

    if (password) {
        password.type = password.type === "password" ? "text" : "password";
    }
}