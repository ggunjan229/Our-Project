// If not logged in → redirect to login
if (!localStorage.getItem("token")) {
    window.location.href = "login.html";
}