
let otpTimer;
let countdownInterval;
let isPhoneVerified = false;
let generatedOtp = '';

// Phone number validation and OTP button enable
document.getElementById("phone").addEventListener("input", function() {
    const phone = this.value.replace(/\D/g, '');
    this.value = phone.slice(0, 10);

    const sendOtpBtn = document.getElementById("sendOtpBtn");
    sendOtpBtn.disabled = phone.length !== 10;

    if (isPhoneVerified) {
        isPhoneVerified = false;
        this.classList.remove('phone-verified');
        document.getElementById("otpSection").style.display = "none";
        document.getElementById("otpStatus").textContent = "";
    }
});

// Send OTP functionality
document.getElementById("sendOtpBtn").addEventListener("click", function() {
    const phone = document.getElementById("phone").value;
    if (phone.length !== 10) {
        alert("Please enter a valid 10-digit phone number");
        return;
    }

    generatedOtp = Math.floor(100000 + Math.random() * 900000).toString();
    console.log("Generated OTP:", generatedOtp);
    alert(`OTP sent to ${phone}. For demo purposes, OTP is: ${generatedOtp}`);

    document.getElementById("otpSection").style.display = "flex";
    startCountdown();

    this.disabled = true;
    this.textContent = "OTP Sent";
});

// Verify OTP functionality
document.getElementById("verifyOtpBtn").addEventListener("click", function() {
    const enteredOtp = document.getElementById("otp").value;
    const otpStatus = document.getElementById("otpStatus");

    if (enteredOtp.length !== 6) {
        otpStatus.textContent = "Please enter a 6-digit OTP";
        otpStatus.className = "otp-status error";
        return;
    }

    if (enteredOtp === generatedOtp) {
        isPhoneVerified = true;
        otpStatus.textContent = "✓ Phone number verified successfully";
        otpStatus.className = "otp-status success";

        document.getElementById("phone").classList.add('phone-verified');
        document.getElementById("otp").classList.add('otp-verified');
        document.getElementById("otp").disabled = true;
        this.disabled = true;
        this.textContent = "Verified";

        clearInterval(countdownInterval);
        document.getElementById("otpTimer").style.display = "none";
        document.getElementById("resendOtpBtn").style.display = "none";
    } else {
        otpStatus.textContent = "✗ Invalid OTP. Please try again.";
        otpStatus.className = "otp-status error";
        document.getElementById("otp").focus();
    }
});

// Resend OTP functionality
document.getElementById("resendOtpBtn").addEventListener("click", function() {
    const phone = document.getElementById("phone").value;
    generatedOtp = Math.floor(100000 + Math.random() * 900000).toString();
    alert(`New OTP sent to ${phone}. For demo: ${generatedOtp}`);
    console.log("Resent OTP:", generatedOtp);

    document.getElementById("otp").value = "";
    document.getElementById("otpStatus").textContent = "";
    startCountdown();
    this.style.display = "none";
});

// Countdown timer
function startCountdown() {
    let timeLeft = 60;
    const countdownElement = document.getElementById("countdown");
    const otpTimer = document.getElementById("otpTimer");
    const resendBtn = document.getElementById("resendOtpBtn");

    otpTimer.style.display = "block";
    resendBtn.style.display = "none";

    countdownElement.textContent = timeLeft;
    countdownInterval = setInterval(() => {
        timeLeft--;
        countdownElement.textContent = timeLeft;
        if (timeLeft <= 0) {
            clearInterval(countdownInterval);
            otpTimer.style.display = "none";
            resendBtn.style.display = "inline-block";
        }
    }, 1000);
}

// Auto-format OTP input
document.getElementById("otp").addEventListener("input", function() {
    const otp = this.value.replace(/\D/g, '');
    this.value = otp;
    if (otp.length === 6) {
        document.getElementById("verifyOtpBtn").click();
    }
});

// Pant logic
document.getElementById("pant").addEventListener("change", function() {
    const pantOptionsContainer = document.getElementById("pantOptionsContainer");
    if (this.value === "shwetambar") {
        pantOptionsContainer.classList.remove("hidden");
    } else {
        pantOptionsContainer.classList.add("hidden");
        document.querySelectorAll('input[name="pantOption"]').forEach(radio => radio.checked = false);
    }
});

// ✅ Final form submission logic
document.getElementById("registrationForm").addEventListener("submit", function(e) {
    e.preventDefault();

    if (!isPhoneVerified) {
        alert("Please verify your phone number with OTP before submitting.");
        document.getElementById("phone").focus();
        return;
    }

    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirmPassword");
    const terms = document.getElementById("terms");

    if (password.value !== confirmPassword.value) {
        alert("Passwords do not match!");
        confirmPassword.focus();
        return;
    }

    if (password.value.length < 8) {
        alert("Password must be at least 8 characters!");
        password.focus();
        return;
    }

    if (!terms.checked) {
        alert("You must agree to the Terms and Privacy Policy.");
        terms.focus();
        return;
    }

    if (document.getElementById("pant").value === "shwetambar") {
        const pantOption = document.querySelector('input[name="pantOption"]:checked');
        if (!pantOption) {
            alert("Please select a Pant option.");
            return;
        }
    }

    // ✅ Submit form
    this.submit();
});

// Real-time password confirmation
document.getElementById("confirmPassword").addEventListener("input", function() {
    const password = document.getElementById("password").value;
    this.style.borderColor = (this.value && this.value !== password) ? "#ef4444" : "#d1d5db";
});

// Email validation
document.getElementById("email").addEventListener("blur", function() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (this.value && !emailRegex.test(this.value)) {
        this.style.borderColor = "#ef4444";
        alert("Please enter a valid email address");
    } else {
        this.style.borderColor = "#d1d5db";
    }
});

// Pincode validation
document.getElementById("pincode").addEventListener("input", function() {
    const pincode = this.value.replace(/\D/g, '');
    this.value = pincode.slice(0, 6);
});

