# Activity 1: Change Background Colour

## Objective

In this activity, you will create a colour picker that allows users to change the background colour of the page. You will practice linking JavaScript files, working with DOM elements, and handling user input.

---

## Starting Point

You have been provided with the following files:

- **index.html** - The HTML structure with a button already in place
- **style.css** - Basic styling for the page
- **main.js** - Contains unrelated code (you won't need this file)

---

## Tasks

Complete the following tasks in order:

### Task 1: Create a New JavaScript File

1. Create a new file called `activity.js` in the same directory as your other files.
2. This is where you will write your JavaScript code.

---

### Task 2: Link the JavaScript File

1. Open `index.html` in your code editor.
2. Add a `<script>` tag to link your new `activity.js` file.
3. Place the script tag **before the closing `</body>` tag**.

> [!IMPORTANT]
> The script tag must be placed **before** the closing `</body>` tag. If placed in the `<head>`, your JavaScript may run before the HTML elements exist, causing errors.

---

### Task 3: Create a Colour Input

1. In `index.html`, add a **label** element with the text content `Colour`.
2. Add an **input** element with the `id` set to `colour`.
3. The input should be of type `text` (or `color` if you prefer a colour picker).
4. Place these elements **before the button** in your HTML.

> [!TIP]
> Using `type="color"` gives users a colour picker instead of typing. Both options work, but the colour picker can be more user-friendly for testing.

---

### Task 4: Create the changeColour Function

1. Open `activity.js` in your code editor.
2. Create a function called `changeColour`.
3. Inside the function:
   - Get a reference to the input element using its id (`colour`).
   - Get a reference to the `pageBody` element (the body has `id="pageBody"`).
   - Change the `style.backgroundColor` property of the body to the value from the input.

---

### Task 5: Register the Button Click Event

1. The button in `index.html` already has `onclick="changeColour()"` set.
2. Verify that clicking the button triggers your `changeColour` function.

> [!NOTE]
> The `onclick` attribute is already set up in the HTML. You do not need to add any event listeners in your JavaScript — just make sure your function name matches exactly (`changeColour`).

3. If the function isn't being called, check that:
   - Your `activity.js` file is linked correctly
   - The function name matches exactly (`changeColour`)

---

### Task 6: Display the Chosen Colour

1. Add a new `<p>` or `<span>` element in your HTML (below the button).
2. Give it an `id` so you can reference it in JavaScript.
3. In your `changeColour` function, update this element's text content to show the colour the user chose.
4. The text should say something like: "You chose: blue"

---

### Task 7: Add a Reset Button

1. Add a new button in your HTML with the text "Reset".
2. Create a new function called `resetColour` in `activity.js`.
3. The `resetColour` function should:
   - Set the background colour of `pageBody` back to white
   - Reset the text colour to its original colour
   - Clear the colour input field
   - Update the display text to show no colour is selected
4. Register the button's `onclick` event to call `resetColour`.

> [!IMPORTANT]
> Remember to reset **all four things**: the background colour, the text colour, the input field, and the display text. Missing one will leave the page in an inconsistent state.

---

### Task 8: Add Console Logging for Red

1. In your `changeColour` function, add logic to check if the user chose the colour **red**.
2. If the user enters `red` OR `#ff0000` (case-insensitive), log the following message to the console:

```
The user chose the colour red
```

**Hint:** You will need to:
- Convert the input to lowercase for comparison
- Check for both `red` and `#ff0000`

> [!CAUTION]
> Users might type `Red`, `RED`, `#FF0000`, or other variations. Use `.toLowerCase()` to convert the input before comparing, otherwise your check may fail for some inputs.

---

### Task 9: Add a Text Colour Input

1. In `index.html`, add a new **label** with the text `Text Colour`.
2. Add a new **input** element with the id `textColour`.
3. Place this next to your existing colour input.
4. In your `changeColour` function, also change the **text colour** of the `pageBody` element using the value from this new input.
5. Update your `resetColour` function to also clear the text colour input and reset the text colour to its original value.

> [!TIP]
> You can set the text colour using `.style.color` on the body element. Try to pick a contrasting colour so the text remains readable.

---

## Useful Information

To help you complete this activity, here are some useful JavaScript concepts:

| Task | What you need | Method/Property |
|------|---------------|------------------|
| Get an element by its id | `document.getElementById()` | Returns the element |
| Get the value of an input | `.value` | Returns the text entered |
| Change a CSS style | `.style.backgroundColor` | Set this to a colour value |
| Change text colour | `.style.color` | Set this to change the text colour |
| Log to the console | `console.log()` | Displays a message in the console |
| Convert text to lowercase | `.toLowerCase()` | Useful for case-insensitive comparison |
| Change element text | `.textContent` or `.innerText` | Set this to change the text inside an element |
| Clear an input | Set `.value` to an empty string | Removes text from an input field |

---

## Testing Your Code

1. Open `index.html` in your web browser.
2. Open the browser's Developer Tools (press `F12` or right-click and select "Inspect").
3. Go to the **Console** tab.
4. Type a colour name (e.g., `blue`) or a hex code (e.g., `#00ff00`) in the input field.
5. Click the **Change Colour** button.

> [!TIP]
> To open Developer Tools, press `F12` (Windows/Linux) or `Cmd + Option + I` (Mac). Make sure you are on the **Console** tab to see any logged messages.

6. Verify:
   - The background colour changes to what you entered
   - The text colour also changes to remain readable
   - The display text updates to show the chosen colour
   - Clicking Reset clears the input, resets the background and text colour, and clears the display text
   - Typing `red` logs the message to the console
   - Typing `#ff0000` also logs the message to the console
