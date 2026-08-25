// Activity 1: Fetch and Display a Single Recipe
//
// Fetch one recipe from https://dummyjson.com/recipes/1
// and display it on the page using getElementById.
//
// Steps (see activity-1.md for details):
// 1. Get references to all elements with getElementById
// 2. Create onRecipeReady(recipe) that populates the page
// 3. Create onResponseReady(response) that calls response.json().then(onRecipeReady)
// 4. Call fetch('https://dummyjson.com/recipes/' + recipeId).then(onResponseReady)
//
// Rules:
// - Do NOT use arrow functions (=>) — use: function myFunc() { }
// - Do NOT use async/await — use .then() with named callbacks
// - Use getElementById for every element

const recipeId = 2; // Change this to fetch a different recipe ID if desired

// TODO Step 1: Get element references — e.g. const recipeName = document.getElementById('recipeName');
const recipeName = document.getElementById("recipeName");
const recipeImage = document.getElementById("recipeImage");
const recipeCuisine = document.getElementById("recipeCuisine");
const recipeDifficulty = document.getElementById("recipeDifficulty");
const recipePrepTime = document.getElementById("recipePrepTime");
const recipeIngredients = document.getElementById("recipeIngredients");
const recipeInstructions = document.getElementById("recipeInstructions");
const recipeRating = document.getElementById("recipeRating");

// TODO Step 2a: Create callback that receives the parsed recipe object
function onRecipeReady(recipe) {
  recipeName.innerText = recipe.name;
  recipeImage.src = recipe.image;
  recipeImage.alt = recipe.name;
  recipeCuisine.innerText = "Cuisine: " + recipe.cuisine;
  recipeDifficulty.innerText = "Difficulty: " + recipe.difficulty;
  recipePrepTime.innerText = "Prep time: " + recipe.prepTimeMinutes + " mins";
  recipeRating.innerText =
    "Rating: " + recipe.rating + " (" + recipe.reviewCount + " reviews)";

  // Build ingredients list as HTML string
  let ingredientsHTML = "";
  for (let i = 0; i < recipe.ingredients.length; i++) {
    ingredientsHTML =
      ingredientsHTML + "<li>" + recipe.ingredients[i] + "</li>";
  }
  recipeIngredients.innerHTML = ingredientsHTML;

  // Build instructions list as HTML string
  let instructionsHTML = "";
  for (let i = 0; i < recipe.instructions.length; i++) {
    instructionsHTML =
      instructionsHTML + "<li>" + recipe.instructions[i] + "</li>";
  }
  recipeInstructions.innerHTML = instructionsHTML;
}

// TODO Step 2b: Create callback that receives the Response and parses JSON
function onResponseReady(response) {
  response.json().then(onRecipeReady);
}

// TODO Step 3: Fetch the recipe
fetch("https://dummyjson.com/recipes/" + recipeId).then(onResponseReady);
