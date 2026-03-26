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