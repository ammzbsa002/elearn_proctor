document.addEventListener("DOMContentLoaded", () => {

    const inputs = document.querySelectorAll(".otp-box");
    const hiddenOtp = document.getElementById("otpValue");

    inputs.forEach((input, index) => {
        input.addEventListener("input", () => {
            if (input.value.length === 1 && index < inputs.length - 1) {
                inputs[index + 1].focus();
            }
            updateOtp();
        });

        input.addEventListener("keydown", (e) => {
            if (e.key === "Backspace" && !input.value && index > 0) {
                inputs[index - 1].focus();
            }
        });
    });

    function updateOtp() {
        hiddenOtp.value = Array.from(inputs).map(i => i.value).join('');
    }

    /* ================= TIMER ================= */
    const timerEl = document.getElementById("timer");
    let time = 120;

    const countdown = setInterval(() => {
        let min = Math.floor(time / 60);
        let sec = time % 60;
        timerEl.textContent = `${min}:${sec < 10 ? '0' : ''}${sec}`;
        time--;

        if (time < 0) {
            clearInterval(countdown);
            timerEl.textContent = "Expired";
        }
    }, 1000);

});
