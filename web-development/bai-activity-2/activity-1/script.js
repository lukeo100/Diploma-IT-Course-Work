// Activity 1: Display User Input
//
// Write JavaScript to take the user's input and display it on the page.
// If the user types "capybara", show a special message instead.
//
// Open activity-1.md for detailed instructions.

// Get the elements from the page
const form = document.getElementById('form'); // Form Element
const userInput = document.getElementById('userInput'); // User Input (text box)
const output = document.getElementById('output'); // Output Element (Text below display button)


// This function prevents the default behavior of the browser
// Then takes the users input from the user input element,
// and displays it on the page
function onSubmit(e) {
    e.preventDefault();

    const userInputValue = userInput.value;

    if(userInputValue.toLowerCase() === "capybara") {
        output.innerText = "🎉 You found the secret! 🎉"
    }
    else {
        output.innerText = userInputValue;
    }
}


// This is the wiring of your button to your function
form.addEventListener('submit', onSubmit);