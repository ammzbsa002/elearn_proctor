document.addEventListener("DOMContentLoaded", () => {

    /* ================= OTP TIMER ================= */

    const timerEl = document.getElementById("timer");
    let time = 120; // 2 minutes

    if (timerEl) {

        const countdown = setInterval(() => {

            let minutes = Math.floor(time / 60);
            let seconds = time % 60;

            timerEl.textContent =
                `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            time--;

            if (time < 0) {
                clearInterval(countdown);
                timerEl.textContent = "Expired";
            }

        }, 1000);
    }


    /* ================= PASSWORD STRENGTH ================= */

    const pwd = document.getElementById("password");
    const fill = document.getElementById("strengthFill");
    const text = document.getElementById("strengthText");

    if (pwd && fill && text) {

        pwd.addEventListener("input", () => {

            let val = pwd.value;
            let score = 0;

            if (val.length >= 8) score++;
            if (/[A-Z]/.test(val)) score++;
            if (/[0-9]/.test(val)) score++;
            if (/[^A-Za-z0-9]/.test(val)) score++;

            const levels = ["Weak", "Fair", "Good", "Strong"];
            const colors = ["#e74c3c", "#f39c12", "#f1c40f", "#2ecc71"];

            fill.style.width = (score * 25) + "%";
            fill.style.background = colors[score - 1] || "transparent";
            text.textContent = levels[score - 1] || "";
        });
    }


    /* ================= RESEND OTP ================= */

    const resendBtn = document.getElementById("resendOtp");

    if (resendBtn) {
        resendBtn.addEventListener("click", () => {
            window.location.reload();
        });
    }


    /* ================= SUCCESS REDIRECT TIMER ================= */

    // 🔥 THIS MUST MATCH YOUR HTML ID
    const successPopup = document.getElementById("successOverlay");

    if (successPopup) {

        let seconds = 3;

        const redirectText = successPopup.querySelector("p");

        const redirectInterval = setInterval(() => {

            seconds--;

            if (seconds > 0) {

                redirectText.textContent =
                    `Redirecting to login in ${seconds} seconds...`;

            } else {

                clearInterval(redirectInterval);

                // ✅ PROFESSIONAL redirect
                window.location.replace("/login/");
            }

        }, 1000);
    }

});

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
