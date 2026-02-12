document.addEventListener("DOMContentLoaded", () => {

    /* ================= OTP INPUT LOGIC ================= */

    const otpBoxes = document.querySelectorAll(".otp-box");
    const otpHidden = document.getElementById("otpValue");
    const otpForm = document.getElementById("otpForm");

    // Auto move, numeric only, backspace
    otpBoxes.forEach((box, index) => {

        box.addEventListener("input", () => {

            // Allow only numbers
            box.value = box.value.replace(/[^0-9]/g, '');

            // Move to next box
            if (box.value && index < otpBoxes.length - 1) {
                otpBoxes[index + 1].focus();
            }
        });

        box.addEventListener("keydown", (e) => {

            // Backspace → move to previous
            if (e.key === "Backspace" && !box.value && index > 0) {
                otpBoxes[index - 1].focus();
            }
        });
    });

    // Combine OTP before submit
    otpForm.addEventListener("submit", (e) => {

        let otp = "";

        otpBoxes.forEach(box => {
            otp += box.value;
        });

        // Validate full OTP
        if (otp.length !== 6) {
            e.preventDefault();
            alert("Please enter the complete 6-digit OTP");
            return;
        }

        otpHidden.value = otp;
    });


    /* ================= OTP TIMER (2 MINUTES) ================= */

    const timerEl = document.getElementById("timer");
    let timeLeft = 120;

    if (timerEl) {

        const countdown = setInterval(() => {

            let minutes = Math.floor(timeLeft / 60);
            let seconds = timeLeft % 60;

            timerEl.textContent =
                `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            timeLeft--;

            if (timeLeft < 0) {
                clearInterval(countdown);
                timerEl.textContent = "Expired";

                // Disable inputs when expired
                otpBoxes.forEach(box => box.disabled = true);
            }

        }, 1000);
    }

});
