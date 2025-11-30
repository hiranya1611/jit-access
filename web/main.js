const API_URL = "http://localhost:5000";

async function requestAccess() {
    const username = document.getElementById("username").value.trim();
    if (!username) return alert("Enter username!");

    const res = await fetch(`${API_URL}/grant`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username })
    });

    const data = await res.json();
    document.getElementById("response").innerText = data.message;
}

async function revokeAccess() {
    const username = document.getElementById("username").value.trim();
    if (!username) return alert("Enter username!");

    const res = await fetch(`${API_URL}/revoke`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username })
    });

    const data = await res.json();
    document.getElementById("response").innerText = data.message;
}
