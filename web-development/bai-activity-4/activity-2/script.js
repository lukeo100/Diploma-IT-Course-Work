// Activity 2: Fetch and Display All Recipes
//
// Fetch ALL recipes from https://dummyjson.com/recipes
// and display them as cards using getElementById and innerHTML.
//
// Steps (see activity-2.md):
// 1. Get #recipeList and #status with getElementById
// 2. Create onDataReady(data) — data.recipes is the array. Loop, build HTML string, set innerHTML
// 3. Create onResponseReady(response) — calls response.json().then(onDataReady)
// 4. Call fetch('https://dummyjson.com/recipes').then(onResponseReady)
//
// Rules:
// - Do NOT use arrow functions (=>) — use: function myFunc() { }
// - Do NOT use async/await — use .then() with named callbacks
// - Use getElementById for every element

// TODO Step 1: Get element references
const recipeList = document.getElementById("recipeList");
const status = document.getElementById("status");

// TODO Step 2: Callback that receives the parsed data object
function onDataReady(data) {
  const recipes = data.recipes;

  status.innerText = `Found ${recipes.length} recipes`;

  let html = "";
  for (let i = 0; i < recipes.length; i++) {
    const recipe = recipes[i];
    html = html + '<div class="card">';
    html = html + `<img src="${recipe.image}" alt="${recipe.name}">`;
    html = html + '<div class="card-body">';
    html = html + "<h3>" + recipe.name + "</h3>";
    html =
      html +
      '<p class="meta">' +
      recipe.cuisine +
      " · " +
      recipe.difficulty +
      "</p>";
    html = html + '<p class="rating">★ ' + recipe.rating + "</p>";
    html =
      html + '<p class="time">Prep: ' + recipe.prepTimeMinutes + " mins</p>";
    html = html + `<p class="time">Cook time: ${recipe.cookTimeMinutes}mins`;
    html = html + `<p class="time">Serves: ${recipe.servings}`;
    html = html + "</div>";
    html = html + "</div>";
  }

  recipeList.innerHTML = html;
}

// TODO Step 3: Callback that receives the Response and parses JSON
function onResponseReady(response) {
  response.json().then(onDataReady);
}

// TODO Step 4: Fetch all recipes
fetch("https://dummyjson.com/recipes").then(onResponseReady);
