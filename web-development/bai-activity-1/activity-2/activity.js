const colourPicker = document.querySelector("#colour");
const textColour = document.querySelector("#textColour");
const pageBody = document.querySelector("#pageBody");
const colourResult = document.querySelector("#colourResult");
const opacitySlider = document.querySelector("#opacitySlider");

function updateResult(content) {
  colourResult.textContent = content;
}

function changeColour(bgColour, txtColour) {
  // If a colour is provided, use it; otherwise, use the values from the colour pickers
  if (bgColour) {
    colourPicker.value = bgColour;
    pageBody.style.backgroundColor = bgColour;
  } else {
    pageBody.style.backgroundColor = colourPicker.value;
  }

  if (txtColour) {
    textColour.value = txtColour;
    pageBody.style.color = txtColour;
  } else {
    pageBody.style.color = textColour.value;
  }
  updateResult(
    `You selected: BG: ${colourPicker.value} - Text: ${textColour.value}`,
  );
  updateDisplay();
  saveSettings();

  // Check if the user selected red (edge case)
  if (
    colourPicker.value.toLowerCase() === "#ff0000" ||
    colourPicker.value.toLowerCase() === "red"
  ) {
    console.log("The user chose the colour red");
  }
}

// Opacity adjustment function
function updateOpacity(value) {
  pageBody.style.opacity = value;
  opacitySlider.value = value;
  updateResult(`Opacity set to: ${value}`);
  updateDisplay();
  saveSettings();
}

// Random colour generator function
function randomColour() {
  changeColour(
    `#${Math.floor(Math.random() * 16777215).toString(16)}`,
    `#${Math.floor(Math.random() * 16777215).toString(16)}`,
  );
}

// Reset function to restore default settings
function resetColour() {
  pageBody.style.backgroundColor = "white";
  pageBody.style.color = "black";
  colourPicker.value = "#ffffff";
  textColour.value = "#000000";
  updateOpacity(1);
  updateResult("Colour reset");
  updateDisplay();
  saveSettings();
}

// Function to update the display of current settings
function updateDisplay() {
  document.querySelector("#currentBackground").textContent =
    `Background Colour: ${pageBody.style.backgroundColor}`;
  document.querySelector("#currentText").textContent =
    `Text Colour: ${pageBody.style.color}`;
  document.querySelector("#currentOpacity").textContent =
    `Opacity: ${pageBody.style.opacity}`;
}

// Save settings to local storage
function saveSettings() {
  const settings = {
    backgroundColor: pageBody.style.backgroundColor,
    textColor: pageBody.style.color,
    opacity: pageBody.style.opacity,
  };
  localStorage.setItem("userSettings", JSON.stringify(settings));
  updateResult("Settings saved");
}

// Load settings from local storage
function loadSettings() {
  const settings = JSON.parse(localStorage.getItem("userSettings"));
  if (settings) {
    changeColour(settings.backgroundColor, settings.textColor);
    updateOpacity(settings.opacity);
    updateResult("Settings loaded");
    updateDisplay();
  }
}
document.addEventListener("DOMContentLoaded", loadSettings);

// Clear settings from local storage
function clearSettings() {
  if (confirm("Are you sure you want to clear your settings?")) {
    localStorage.removeItem("userSettings");
    updateResult("Settings cleared");
    updateDisplay();
  }
}
