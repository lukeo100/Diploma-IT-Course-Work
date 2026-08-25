// Activity 3: Registration Form Validation
//
// Write JavaScript to validate a registration form with 4 fields.
// Validate on blur (when user leaves a field) and on submit.
// Show appropriate error messages for each type of invalid input.
//
// Open activity-3.md for detailed instructions.
const form = document.querySelector("#form");

//Input fields
const usernameInput = document.querySelector("#username");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const confirmPasswordInput = document.querySelector("#confirmPassword");

// Error message elements
const usernameError = document.querySelector("#usernameError");
const emailError = document.querySelector("#emailError");
const passwordError = document.querySelector("#passwordError");
const confirmPasswordError = document.querySelector("#confirmPasswordError");

const success = document.querySelector("#success");

// Helper function
function showError(errorElement, message) {
  errorElement.textContent = message;
  errorElement.classList.add("visible");
}

function hideError(errorElement) {
  errorElement.textContent = "";
  errorElement.classList.remove("visible");
}

// validation functions
function validateUsername() {
  if (usernameInput.value.trim() === "") {
    showError(usernameError, "Username is required.");
    return false;
  }
  if (usernameInput.value.trim().length < 3) {
    showError(usernameError, "Username must be at least 3 characters.");
    return false;
  }
  if (usernameInput.value.trim().length > 32) {
    showError(usernameError, "Username must be 32 characters or less.");
    return false;
  }
  if (usernameInput.value.trim().includes(" ")) {
    showError(usernameError, "Username cannot contain spaces.");
    return false;
  }
  if (!/^[a-zA-Z0-9]+$/.test(usernameInput.value.trim())) {
    showError(usernameError, "Username can only contain letters and numbers.");
    return false;
  }

  // If all checks pass, hide the error message
  hideError(usernameError);
  return true;
}

function validateEmail() {
  if (emailInput.value.trim() === "") {
    showError(emailError, "Email is required.");
    return false;
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailInput.value.trim())) {
    showError(emailError, "Please enter a valid email.");
    return false;
  }
  hideError(emailError);
  return true;
}

function validatePassword() {
  if (passwordInput.value.trim() === "") {
    showError(passwordError, "Password is required.");
    return false;
  }
  if (passwordInput.value.trim().length < 6) {
    showError(passwordError, "Password must be at least 6 characters.");
    return false;
  }
  hideError(passwordError);
  return true;
}

function validateConfirmPassword() {
  if (confirmPasswordInput.value.trim() === "") {
    showError(confirmPasswordError, "Please confirm your password.");
    return false;
  }
  if (confirmPasswordInput.value.trim() !== passwordInput.value.trim()) {
    showError(confirmPasswordError, "Passwords do not match.");
    return false;
  }
  hideError(confirmPasswordError);
  return true;
}

// Event listeners for blur events
usernameInput.addEventListener("blur", validateUsername);
emailInput.addEventListener("blur", validateEmail);
passwordInput.addEventListener("blur", validatePassword);
confirmPasswordInput.addEventListener("blur", validateConfirmPassword);

// function for form submission
function handleSubmit(event) {
  event.preventDefault(); // Prevent form submission
  validateUsername();
  validateEmail();
  validatePassword();
  validateConfirmPassword();
}
form.addEventListener("submit", handleSubmit);
