// ================= OVERLAY TOGGLE =================
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

if (signUpButton && signInButton && container) {
    signUpButton.addEventListener('click', () => {
        container.classList.add("right-panel-active");
    });

    signInButton.addEventListener('click', () => {
        container.classList.remove("right-panel-active");
    });
}

function toggleLoginPassword() {


const password = document.getElementById("loginPassword");
const icon = document.getElementById("loginEyeIcon");

if (password.type === "password") {
    password.type = "text";
    icon.textContent = "🙈";
} else {
    password.type = "password";
    icon.textContent = "👁️";
}


}


function togglePassword() {

    const passwordField = document.getElementById("regPassword");
    const eyeIcon = document.getElementById("eyeIcon");

    if (passwordField.type === "password") {
        passwordField.type = "text";
        eyeIcon.textContent = "🙈";
    } else {
        passwordField.type = "password";
        eyeIcon.textContent = "👁️";
    }
}

// ================= REGISTER PASSWORD STRENGTH =================
const regPwd = document.getElementById("regPassword");
const regFill = document.getElementById("regStrengthFill");
const regText = document.getElementById("regStrengthText");
const regBtn = document.getElementById("regSubmit");

if (regPwd && regFill && regText && regBtn) {
    regPwd.addEventListener("input", () => {
        let val = regPwd.value;
        let score = 0;

        if (val.length >= 8) score++;
        if (/[A-Z]/.test(val)) score++;
        if (/[0-9]/.test(val)) score++;
        if (/[^A-Za-z0-9]/.test(val)) score++;

        const levels = ["Weak", "Fair", "Good", "Strong"];
        const colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71"];

        regFill.style.width = (score * 25) + "%";
        regFill.style.background = colors[score - 1] || "transparent";
        regText.textContent = levels[score - 1] || "";

        // 🔥 Enable only if STRONG
        regBtn.disabled = score < 4;
    });
}
