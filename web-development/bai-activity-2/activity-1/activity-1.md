# Activity 1: Display User Input

## Objective

Write JavaScript to take text from an input field and display it on the page when the user submits the form. If the user types "capybara", show a special message instead.

## Files

- `index.html` - The form HTML
- `styles.css` - Styling (already complete)
- `script.js` - Write your JavaScript here

## Step 1: Get Element References

Add these lines at the top of `script.js`:

```js
const form = document.getElementById('form');
const userInput = document.getElementById('userInput');
const output = document.getElementById('output');
```

## Step 2: Create a Submit Handler

Create a function that runs when the form is submitted:

```js
function onSubmit(e) {
    e.preventDefault();

    if (userInput.value.toLowerCase() === 'capybara') {
        output.innerText = '🦫 You found the secret!';
    } else {
        output.innerText = userInput.value;
    }
}
```

- `e.preventDefault()` stops the page from reloading
- `userInput.value` gets the text from the input
- `.toLowerCase()` makes the check case-insensitive
- The `if` statement checks for the special word
- `output.innerText` sets the text inside the span

## Step 3: Register the Event Listener

Add this line at the bottom:

```js
form.addEventListener('submit', onSubmit);
```

## Testing

1. Open `index.html` in a browser
2. Type something in the input field and click Display - your text should appear
3. Type "capybara" (any capitalization) and click Display - you should see the secret message
4. Type "CAPYBARA" or "Capybara" - should still show the secret message

## Summary

In this activity you learned:
- How to get references to DOM elements with `getElementById`
- How to get a value from an input with `.value`
- How to set text with `.innerText`
- How to handle form submission with `addEventListener`
- How to use `if/else` to run different code based on conditions
- How to use `.toLowerCase()` for case-insensitive comparison
