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