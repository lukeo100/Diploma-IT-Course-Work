// Activity 2: Simple Login Form Validation
//
// Write JavaScript to validate a login form.
// Check that both fields are filled in before allowing submission.
// Show error messages when fields are empty.
//
// Open activity-2.md for detailed instructions.
const form = document.getElementById("form");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const usernameError = document.getElementById("usernameError");
const passwordError = document.getElementById("passwordError");
const success = document.getElementById("success");

function showError(error, message) {
  error.textContent = message;
  error.classList.add("visible");
}

function clearError(error) {
  error.textContent = "";
  error.classList.remove("visible");
}

function validateUsername() {
  if (usernameInput.value.trim() === "") {
    showError(usernameError, "Username is required.");
    return false;
  }
  clearError(usernameError);
  return true;
}

function validatePassword() {
  if (passwordInput.value.trim() === "") {
    showError(passwordError, "Password is required.");
    return false;
  }
  clearError(passwordError);
  return true;
}

function onUsernameBlur() {
  validateUsername();
}

function onPasswordBlur() {
  validatePassword();
}

function onSubmit(e) {
  e.preventDefault();
  if (validateUsername() && validatePassword()) {
    form.style.display = "none";
    success.classList.add("visible");
  }
}

usernameInput.addEventListener("blur", onUsernameBlur);
passwordInput.addEventListener("blur", onPasswordBlur);
form.addEventListener("submit", onSubmit);
