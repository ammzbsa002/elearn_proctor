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

// Firebase SDK imports (ES module)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  sendEmailVerification
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// 🔥 Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyDNjmYWSVzb89nDPgfL30IgZYOZ0pNidTc",
  authDomain: "elearn-proctor.firebaseapp.com",
  projectId: "elearn-proctor",
  storageBucket: "elearn-proctor.firebasestorage.app",
  messagingSenderId: "316356956662",
  appId: "1:316356956662:web:8048e126a0e9adad0cb7d7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// ✅ Send OTP (Email Verification)
window.sendOTP = async function () {
  const email = document.getElementById("email").value;
  const tempPassword = "Temp@12345";

  try {
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      tempPassword
    );

    await sendEmailVerification(userCredential.user);

    alert("OTP sent to your email. Please verify.");

  } catch (error) {
    alert(error.message);
  }
};

