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
            window.location.reload(); // triggers OTP resend via backend
        });
    }

    /* ================= SUCCESS REDIRECT TIMER ================= */
    /*
        This runs ONLY if success popup exists
        Does NOT affect login / OTP / strength / resend logic
    */

    const successPopup = document.getElementById("successPopup");
    const redirectText = document.getElementById("redirectTimer");
    let redirectSeconds = 3;

    if (successPopup && redirectText) {
        redirectText.textContent = redirectSeconds;

        const redirectInterval = setInterval(() => {
            redirectSeconds--;
            redirectText.textContent = redirectSeconds;

            if (redirectSeconds === 0) {
                clearInterval(redirectInterval);
                window.location.href = "/login/";
            }
        }, 1000);
    }

});
