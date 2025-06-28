Somray Mardi#
<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Wallet + Admin Login</title>
  <style>
    body {
      font-family: Arial;
      max-width: 500px;
      margin: 20px auto;
      border: 2px solid #333;
      padding: 20px;
      border-radius: 10px;
    }
    input, button {
      width: 100%;
      padding: 8px;
      margin-top: 5px;
    }
    .link {
      color: blue;
      cursor: pointer;
      text-decoration: underline;
      margin-top: 10px;
      display: block;
    }
    .info, .error {
      margin-top: 10px;
    }
    .error { color: red; }
    .hidden { display: none; }
    table {
      width: 100%;
      margin-top: 10px;
      border-collapse: collapse;
    }
    th, td {
      border: 1px solid #aaa;
      padding: 6px;
      text-align: left;
    }
  </style>
</head>
<body>

<h2>Login System</h2>

<div id="selectLogin">
  <button onclick="showUserLogin()">User Login</button>
  <button onclick="showAdminLogin()">Admin Login</button>
</div>

<!-- User Signup/Login -->
<div id="userAuth" class="hidden">
  <div id="signupDiv">
    <h3>User Signup</h3>
    <input type="text" id="signupUsername" placeholder="Username" />
    <input type="password" id="signupPassword" placeholder="Password" />
    <button onclick="signup()">Signup</button>
    <span class="link" onclick="showLogin()">Already user? Login</span>
  </div>

  <div id="loginDiv" class="hidden">
    <h3>User Login</h3>
    <input type="text" id="loginUsername" placeholder="Username" />
    <input type="password" id="loginPassword" placeholder="Password" />
    <button onclick="login()">Login</button>
    <span class="link" onclick="showSignup()">New user? Signup</span>
  </div>
</div>

<!-- Admin Login -->
<div id="adminAuth" class="hidden">
  <h3>Admin Login</h3>
  <input type="text" id="adminUsername" placeholder="Admin Username" />
  <input type="password" id="adminPassword" placeholder="Admin Password" />
  <button onclick="adminLogin()">Login as Admin</button>
  <div id="adminLoginError" class="error"></div>
</div>

<!-- Admin Dashboard -->
<div id="adminPanel" class="hidden">
  <h3>🛡️ Admin Dashboard</h3>
  <table>
    <thead>
      <tr>
        <th>Username</th><th>Wallet</th><th>Coins</th><th>Referrals</th><th>Joins</th>
      </tr>
    </thead>
    <tbody id="adminUserTable"></tbody>
  </table>
  <button onclick="logout()">Logout</button>
</div>

<!-- User Dashboard -->
<div id="userPanel" class="hidden">
  <h3>Welcome, <span id="userNameDisplay"></span></h3>
  <button onclick="joinUser()">Join ₹500</button>

  <div class="info" id="walletInfo">--</div>

  <h4>Refer & Earn</h4>
  <input type="text" id="referName" placeholder="Refer Name" />
  <button onclick="addReferral()">Add Referral</button>
  <div id="referralInfo">--</div>

  <h4>Withdraw ₹600</h4>
  <input type="text" id="upiId" placeholder="Your UPI ID" />
  <button onclick="withdraw()">Withdraw</button>
  <div id="withdrawInfo"></div>

  <button style="margin-top: 20px;" onclick="logout()">Logout</button>
</div>

<script>
let currentUser = null;
const STORAGE_KEY = "walletUsersData";

// Auth display toggles
function showUserLogin() {
  document.getElementById("selectLogin").classList.add("hidden");
  document.getElementById("userAuth").classList.remove("hidden");
}
function showAdminLogin() {
  document.getElementById("selectLogin").classList.add("hidden");
  document.getElementById("adminAuth").classList.remove("hidden");
}
function showSignup() {
  document.getElementById("signupDiv").classList.remove("hidden");
  document.getElementById("loginDiv").classList.add("hidden");
}
function showLogin() {
  document.getElementById("signupDiv").classList.add("hidden");
  document.getElementById("loginDiv").classList.remove("hidden");
}

// Storage
function loadUsers() {
  return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
}
function saveUsers(users) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
}

// Signup
function signup() {
  const user = document.getElementById("signupUsername").value.trim();
  const pass = document.getElementById("signupPassword").value.trim();
  if (!user || !pass) return alert("Fill all fields.");
  const users = loadUsers();
  if (users[user]) return alert("Username already exists.");
  users[user] = {
    password: pass, walletBalance: 0, silverCoins: 0,
    referrals: [], localAdminBenefit: 0, systemBenefit: 0,
    joinCount: 0
  };
  saveUsers(users);
  alert("Signup successful. Now login.");
  showLogin();
}

// Login
function login() {
  const user = document.getElementById("loginUsername").value.trim();
  const pass = document.getElementById("loginPassword").value.trim();
  const users = loadUsers();
  if (!users[user] || users[user].password !== pass) return alert("Invalid login.");
  currentUser = user;
  document.getElementById("userAuth").classList.add("hidden");
  document.getElementById("userPanel").classList.remove("hidden");
  document.getElementById("userNameDisplay").innerText = currentUser;
  updateWallet();
}

// ✅ Admin Login with: Admin / 123
function adminLogin() {
  const u = document.getElementById("adminUsername").value.trim();
  const p = document.getElementById("adminPassword").value.trim();
  if (u === "Admin" && p === "123") {
    document.getElementById("adminAuth").classList.add("hidden");
    document.getElementById("adminPanel").classList.remove("hidden");
    loadAdminTable();
  } else {
    document.getElementById("adminLoginError").innerText = "❌ गलत Admin Username या Password.";
  }
}

// Admin User Table
function loadAdminTable() {
  const users = loadUsers();
  let html = "";
  for (let user in users) {
    let u = users[user];
    html += `<tr>
      <td>${user}</td>
      <td>₹${u.walletBalance}</td>
      <td>${u.silverCoins}</td>
      <td>${u.referrals.length}</td>
      <td>${u.joinCount}</td>
    </tr>`;
  }
  document.getElementById("adminUserTable").innerHTML = html;
}

// Join ₹500
function joinUser() {
  const users = loadUsers();
  let u = users[currentUser];
  u.walletBalance += 200;
  u.walletBalance -= 500;
  u.silverCoins += 2000;
  u.joinCount += 1;
  users[currentUser] = u;
  saveUsers(users);
  updateWallet();
  alert(`Joined successfully! ₹200 cashback, 2000 silver coins.`);
}

// Referral
function addReferral() {
  const name = document.getElementById("referName").value.trim();
  if (!name) return alert("Referral name required.");
  const users = loadUsers();
  let u = users[currentUser];
  u.referrals.push(name);
  u.walletBalance += 200;
  u.localAdminBenefit += 100;
  u.systemBenefit += 200;
  users[currentUser] = u;
  saveUsers(users);
  updateWallet();
  document.getElementById("referName").value = "";
  alert("Referral added.");
}

// Withdrawal
function withdraw() {
  const upi = document.getElementById("upiId").value.trim();
  const users = loadUsers();
  let u = users[currentUser];
  if (!upi.includes("@")) return alert("Valid UPI required.");
  if (u.referrals.length < 3) return alert("Need 3 referrals to withdraw.");
  if (u.walletBalance < 600) return alert("Need ₹600 in wallet.");
  u.walletBalance -= 600;
  users[currentUser] = u;
  saveUsers(users);
  updateWallet();
  document.getElementById("withdrawInfo").innerHTML = `Withdraw ₹600 to <b>${upi}</b> initiated.`;
}

// Wallet update
function updateWallet() {
  const users = loadUsers();
  const u = users[currentUser];
  document.getElementById("walletInfo").innerHTML = `
    Wallet: ₹${u.walletBalance}<br>
    Coins: ${u.silverCoins}<br>
    Joins: ${u.joinCount}<br>
    Referrals: ${u.referrals.length}<br>
    Local Admin: ₹${u.localAdminBenefit}<br>
    System Benefit: ₹${u.systemBenefit}
  `;
  document.getElementById("referralInfo").innerHTML =
    u.referrals.length === 0 ? "No referrals yet." :
    "<ul>" + u.referrals.map(r => `<li>${r}</li>`).join('') + "</ul>";
}

// Logout
function logout() {
  currentUser = null;
  document.querySelectorAll("div").forEach(d => d.classList.add("hidden"));
  document.getElementById("selectLogin").classList.remove("hidden");
}
</script>

</body>
</html>
