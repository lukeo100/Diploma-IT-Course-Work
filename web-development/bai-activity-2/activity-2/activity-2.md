# Activity 1: Simple Form Validation

## Objective

Add JavaScript to validate a login form. Check that both fields are filled in before allowing submission.

## Files

- `index.html` - The form HTML
- `styles.css` - Styling (already complete)
- `script.js` - Write your JavaScript here

## Step 1: Get Element References

Add these lines at the top of `script.js`:

```js
const form = document.getElementById('form');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const usernameError = document.getElementById('usernameError');
const passwordError = document.getElementById('passwordError');
const success = document.getElementById('success');
```

## Step 2: Create Helper Functions

Add these two functions. They will show and hide error messages.

```js
function showError(error, message) {
    error.textContent = message;
    error.classList.add('visible');
}

function hideError(error) {
    error.classList.remove('visible');
}
```

## Step 3: Create Validation Functions

Create two functions that check if each field is empty.

**validateUsername**
```js
function validateUsername() {
    if (usernameInput.value.trim() === '') {
        showError(usernameError, 'Username is required');
        return false;
    }
    hideError(usernameError);
    return true;
}
```

**validatePassword**
```js
function validatePassword() {
    if (passwordInput.value === '') {
        showError(passwordError, 'Password is required');
        return false;
    }
    hideError(passwordError);
    return true;
}
```

## Step 4: Create Event Handler Functions

Create these functions to handle events:

```js
function onUsernameBlur() {
    validateUsername();
}

function onPasswordBlur() {
    validatePassword();
}

function onSubmit(e) {
    e.preventDefault();

    const usernameValid = validateUsername();
    const passwordValid = validatePassword();

    if (usernameValid && passwordValid) {
        form.style.display = 'none';
        success.classList.add('visible');
    }
}
```

## Step 5: Register Event Listeners

Add these lines at the bottom of your script:

```js
usernameInput.addEventListener('blur', onUsernameBlur);
passwordInput.addEventListener('blur', onPasswordBlur);
form.addEventListener('submit', onSubmit);
```

## Testing

1. Open `index.html` in a browser
2. Click in the username field, then click out - "Username is required" should appear
3. Click in the password field, then click out - "Password is required" should appear
4. Type something in both fields and click out - errors should disappear
5. Click Log In with both fields filled - success message should appear
6. Click Log In with empty fields - errors should appear and form should not submit

## Summary

In this activity you learned:
- How to get references to DOM elements
- How to add and remove CSS classes with JavaScript
- How to validate form fields
- How to handle blur and submit events
- How to prevent default form submission
