# Activity 2: Extended Colour Customiser

## Objective

In this activity, you will extend your colour customiser from Activity 1. You will add new features including a random colour generator, colour presets, an opacity slider, and local storage to remember the user's last selection.

**This is a take-home activity.** Complete all tasks and test your code before the next class.

---

## Starting Point

You should have completed **Activity 1** with the following features:

- A colour input to change the background colour
- A text colour input
- A Change Colour button
- A Reset button
- A display showing the chosen colour

Copy your files from Activity 1 into a new folder called `activity-2` to begin.

---

## Tasks

### Task 1: Create a Random Colour Button

1. Add a new button in `index.html` with the text `Random Colour`.
2. Create a new function called `randomColour` in `activity.js`.
3. The `randomColour` function should:
   - Generate a random hex colour code (e.g., `#a3f2b1`)
   - Set the colour input's value to this random colour
   - Trigger the colour change (you can call `changeColour()` or duplicate the logic)
4. Register the button's `onclick` event to call `randomColour`.

> [!TIP]
> A hex colour code is made up of a `#` followed by 6 characters (0-9 and a-f). You can use `Math.random()` and a string of possible characters to build a random hex code.

---

### Task 2: Add Colour Presets

1. In `index.html`, add a section with 5 preset colour buttons (e.g., Red, Green, Blue, Yellow, Purple).
2. Give each button a class like `preset-btn` so you can style them together.
3. Create a function called `applyPreset` that takes a colour value as a parameter.
4. The `applyPreset` function should:
   - Set the colour input's value to the preset colour
   - Set the background colour of `pageBody`
   - Update the display text to show the chosen colour
5. Each preset button should call `applyPreset` with its specific colour when clicked.

> [!NOTE]
> You can pass values directly in the `onclick` attribute, like `onclick="applyPreset('red')"`. This way one function handles all the preset buttons.

---

### Task 3: Add an Opacity Slider

1. In `index.html`, add a **label** with the text `Opacity`.
2. Add an **input** of type `range` with:
   - An `id` of `opacity`
   - A `min` value of `0`
   - A `max` value of `100`
   - A `value` of `100`
3. Create a new function called `updateOpacity`.
4. The `updateOpacity` function should:
   - Get the value from the opacity slider
   - Convert it to a decimal (0 to 1) by dividing by 100
   - Set the `opacity` style on the `pageBody` element
5. Register the slider's `oninput` event to call `updateOpacity`.
6. Update your `resetColour` function to reset the opacity slider to 100.

> [!TIP]
> The `oninput` event fires every time the slider value changes, giving a live preview as the user drags.

---

### Task 4: Display Current Values

1. In `index.html`, add a new `<div>` or `<section>` with an `id` of `currentSettings`.
2. In this section, display the current values of:
   - Background colour
   - Text colour
   - Opacity percentage
3. Create a function called `updateDisplay` that updates this section with the current values.
4. Call `updateDisplay` from `changeColour` and `updateOpacity` whenever a value changes.

> [!TIP]
> You can use `.textContent` to update the display. For example: `document.getElementById('bgColourDisplay').textContent = colourInput.value;`

---

### Task 5: Save Settings with Local Storage

1. Create a function called `saveSettings` that saves the current settings to `localStorage`.
2. The `saveSettings` function should save:
   - Background colour
   - Text colour
   - Opacity value
3. Call `saveSettings` from `changeColour`, `updateOpacity`, and `applyPreset` so settings are saved automatically.
4. Create a function called `loadSettings` that loads settings from `localStorage` when the page loads.
5. Call `loadSettings` at the end of your script or when the page loads.

> [!IMPORTANT]
> Local storage only stores strings. You will need to use `localStorage.setItem('key', value)` to save and `localStorage.getItem('key')` to retrieve values. Remember to convert numbers back from strings when loading.

---

### Task 6: Add a Clear History Button

1. Add a button with the text `Clear Saved Settings`.
2. Create a function called `clearSettings` that:
   - Removes the saved settings from `localStorage`
   - Calls `resetColour` to reset the page
3. Register the button's `onclick` event to call `clearSettings`.

> [!CAUTION]
> Clearing local storage removes all saved data permanently. Make sure the user confirms before clearing, or add a note that this cannot be undone.

---

## Testing Your Code

1. Open `index.html` in your web browser.
2. Open the browser's Developer Tools (`F12`) and go to the **Console** tab.
3. Test each feature:
   - Changing the background colour and text colour
   - Clicking the Random Colour button
   - Clicking each preset button
   - Dragging the opacity slider
   - Verifying the display updates with current values
   - Refreshing the page to check if settings are saved
   - Clicking Clear Saved Settings to reset everything

4. Verify:
   - Random Colour generates a valid hex code and applies it
   - Preset buttons apply the correct colours
   - Opacity slider changes the page transparency (0% = invisible, 100% = fully visible)
   - Display shows current settings
   - Settings persist after page refresh
   - Clear Saved Settings removes stored data and resets the page

---

## Useful Information

| Task | What you need | Method/Property |
|------|---------------|------------------|
| Random number | `Math.random()` | Returns a decimal between 0 and 1 |
| Round down | `Math.floor()` | Rounds a number down to the nearest whole number |
| Save to local storage | `localStorage.setItem()` | Saves a value with a key |
| Read from local storage | `localStorage.getItem()` | Retrieves a saved value |
| Remove from local storage | `localStorage.removeItem()` | Deletes a saved value |
| Get input value | `.value` | Returns the current value of an input |
| Set element text | `.textContent` | Changes the text inside an element |

---

## Checklist

Before submitting, make sure you have:
- Copied Activity 1 files into a new `activity-2` folder
- Created a Random Colour button that generates and applies a random hex code
- Created 5 preset colour buttons
- Added an opacity slider (0-100)
- Display shows current background colour, text colour, and opacity
- Settings are saved to local storage when changed
- Settings are loaded from local storage on page load
- Clear Saved Settings button removes stored data and resets the page
- Reset button also resets opacity to 100
- Tested all features in the browser
