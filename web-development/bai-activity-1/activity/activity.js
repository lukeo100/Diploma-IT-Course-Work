const colourPicker = document.querySelector("#colour");
const textColour = document.querySelector("#textColour");
const pageBody = document.querySelector("#pageBody");
const colourResult = document.querySelector("#colourResult");

function updateResult(content) {
  colourResult.textContent = content;
}

function changeColour() {
  pageBody.style.backgroundColor = colourPicker.value;
  pageBody.style.color = textColour.value;
  updateResult(
    `You selected: BG: ${colourPicker.value} - Text: ${textColour.value}`,
  );

  // Check if the user selected red
  if (
    colourPicker.value.toLowerCase() === "#ff0000" ||
    colourPicker.value.toLowerCase() === "red"
  ) {
    console.log("The user chose the colour red");
  }
}

function resetColour() {
  pageBody.style.backgroundColor = "white";
  pageBody.style.color = "black";
  colourPicker.value = "#ffffff";
  textColour.value = "#000000";
  updateResult("Colour reset");
}
