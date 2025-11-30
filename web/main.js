const API_BASE = "http://127.0.0.1:5000";

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API_BASE}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    });

    const result = await response.json();
    
    if (result.login) {
        document.getElementById("login-status").innerHTML = 
            `✅ Login successful (Role: ${result.role})`;
    } else {
        document.getElementById("login-status").innerHTML = 
            `❌ Invalid username or password`;
    }
}

async function requestAccess() {
    const username = document.getElementById("username").value;
    const resource = document.getElementById("resource").value;

    const response = await fetch(`${API_BASE}/request-access`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, resource })
    });

    const result = await response.json();

    document.getElementById("access-status").innerHTML =
        result.status === "approved"
        ? `✔ Access Approved Until: ${result.valid_until}`
        : `❌ Request Failed`;
}
