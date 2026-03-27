async function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Please fill all fields");
        return;
    }

    const res = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    const data = await res.json();

    if (data.access_token) {
        // Save token
        localStorage.setItem("token", data.access_token);

        // Redirect to dashboard
        window.location.href = "index.html";
    } else {
        alert("Invalid credentials");
    }
}
async function signup() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    const res = await fetch("http://127.0.0.1:8000/signup", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    const data = await res.json();

    if (data.message) {
        alert("Account created successfully!");
        window.location.href = "login.html";
    } else {
        alert("Signup failed");
    }
}
function showSignupForm() {
    document.getElementById('loginContainer').innerHTML = `
        <div class="card">
            <h1>Create Account</h1>
            <input type="text" id="fullname" placeholder="Full Name">
            <input type="email" id="signupEmail" placeholder="Email">
            <input type="password" id="signupPassword" placeholder="Password">
            <input type="password" id="signupConfirm" placeholder="Confirm Password">
            <button onclick="signupUser()">Sign Up</button>
            <a onclick="location.reload()">Back to Login</a>
        </div>
    `;
}

function signupUser() {
    const fullname = document.getElementById('fullname').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    
    if (password !== confirm) {
        alert('Passwords do not match');
        return;
    }
    
    const users = JSON.parse(localStorage.getItem('users') || '[]');
    users.push({ fullname, email, password });
    localStorage.setItem('users', JSON.stringify(users));
    
    alert('Account created! Please login');
    location.reload();
}

function openForgotModal() {
    document.getElementById("forgotModal").classList.add("active");
  }

  function closeForgotModal() {
    document.getElementById("forgotModal").classList.remove("active");
  }
  function togglePassword() {
    const passwordInput = document.getElementById("password");
    const toggleBtn = document.querySelector(".toggle-password i");

    if (passwordInput.type === "password") {
      passwordInput.type = "text";
      toggleBtn.classList.remove("fa-eye");
      toggleBtn.classList.add("fa-eye-slash");
    } else {
      passwordInput.type = "password";
      toggleBtn.classList.remove("fa-eye-slash");
      toggleBtn.classList.add("fa-eye");
    }
  }

  document.getElementById("loginForm").addEventListener("submit", (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email && password) {
      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userName", email.split("@")[0]);
      window.location.href = "index.html";
    } else {
      alert("Please enter both email and password");
    }
  });