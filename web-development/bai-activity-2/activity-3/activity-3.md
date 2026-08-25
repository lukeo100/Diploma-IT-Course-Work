# Activity 3: Registration Form Validation

## Objective

Add JavaScript validation to the registration form. The form should validate each field when the user leaves it (on blur) and again when they submit. Show error messages for invalid input.

## Files

- `index.html` - The form HTML
- `styles.css` - Styling (already complete)
- `script.js` - Write your JavaScript here

## Requirements

### 1. Get References to DOM Elements

At the top of your script, get references to:
- The form (`#form`)
- All four inputs (`#username`, `#email`, `#password`, `#confirmPassword`)
- All four error elements (`#usernameError`, `#emailError`, `#passwordError`, `#confirmPasswordError`)
- The success message (`#success`)

### 2. Create Helper Functions

Create these two functions:

**showError(error, message)**
- Set the error element's text content to the message
- Add the `visible` class to the error element

**hideError(error)**
- Remove the `visible` class from the error element

### 3. Create Validation Functions

Create these four functions. Each should validate the input and call `showError` or `hideError`. Return `true` if valid, `false` if invalid.

**validateUsername()**
- Cannot be empty
- Must be at least 3 characters
- Cannot be longer than 32 characters
- Cannot contain spaces
- Can only contain letters and numbers (use regex: `/^[a-zA-Z0-9]+$/`)

**validateEmail()**
- Cannot be empty
- Must be a valid email format (use regex: `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`)

**validatePassword()**
- Cannot be empty
- Must be at least 6 characters

**validateConfirmPassword()**
- Cannot be empty
- Must match the password field

### 4. Register Event Listeners

Create named functions for each event handler:

```js
function onUsernameBlur() {
    validateUsername();
}

// ... similar for other fields
```

Then register them:

```js
usernameInput.addEventListener('blur', onUsernameBlur);
// ... similar for other fields
```

### 5. Handle Form Submission

Create an `onSubmit` function that:
- Calls `e.preventDefault()` to stop the form from submitting
- Calls all four validation functions
- Stores each result in a variable
- If all are valid, hide the form and show the success message

Register it:

```js
form.addEventListener('submit', onSubmit);
```

## Rules

- Use `const` for variables that don't change
- Use `let` for variables that do change
- Use named functions, no arrow functions or anonymous functions
- Do not over-comment your code

## Testing

1. Open `index.html` in a browser
2. Click in a field, then click out without typing - error should appear
3. Type invalid data and click out - appropriate error should appear
4. Fill all fields correctly and submit - success message should appear
5. Try submitting with invalid data - errors should appear and form should not submit

## Expected Error Messages

| Field | Error |
|-------|-------|
| Username (empty) | Username is required |
| Username (too short) | Username must be at least 3 characters |
| Username (too long) | Username must be 32 characters or less |
| Username (spaces) | Username cannot contain spaces |
| Username (special chars) | Username can only contain letters and numbers |
| Email (empty) | Email is required |
| Email (invalid) | Please enter a valid email |
| Password (empty) | Password is required |
| Password (too short) | Password must be at least 6 characters |
| Confirm (empty) | Please confirm your password |
| Confirm (mismatch) | Passwords do not match |
