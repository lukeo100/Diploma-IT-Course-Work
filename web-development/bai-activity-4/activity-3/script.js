// Activity 3: Search Recipes on Button Click
//
// When the user types a term and clicks Search, fetch from:
//   https://dummyjson.com/recipes/search?q=SEARCH_TERM
// and display results as cards.
//
// Steps (see activity-3.md):
// 1. Get #searchInput, #searchButton, #recipeList, #status with getElementById
// 2. Create onSearchDataReady(data) — handles data.recipes, empty case, builds HTML, sets innerHTML
// 3. Create onSearchResponseReady(response) — calls response.json().then(onSearchDataReady)
// 4. Create onSearchClick() — reads searchInput.value.trim(), validates, fetches with query
// 5. Register: searchButton.addEventListener('click', onSearchClick)
//
// Rules:
// - Do NOT use arrow functions (=>) — use: function myFunc() { }
// - Do NOT use async/await — use .then() with named callbacks
// - Use getElementById for every element

// TODO Step 1: Get element references
const searchInput = document.getElementById("searchInput");
const searchButton = document.getElementById("searchButton");
const recipeList = document.getElementById("recipeList");
const status = document.getElementById("status");

// TODO Step 2: Callback that receives the parsed search data
function onSearchDataReady(data) {
  const recipes = data.recipes;

  if (recipes.length === 0) {
    status.innerText = 'No recipes found for "' + searchInput.value + '"';
    recipeList.innerHTML =
      '<p class="empty">Try searching for "pizza", "chicken", or "pasta".</p>';
    return;
  }

  status.innerText = `Found ${recipes.length} recipes for "${searchInput.value}"`;

  let html = "";
  for (let i = 0; i < recipes.length; i++) {
    const recipe = recipes[i];
    html = html + '<div class="card">';
    html = html + `<img src="${recipe.image}" alt="${recipe.name}">`;
    html = html + '<div class="card-body">';
    html = html + `<h3>${recipe.name}</h3>`;
    html =
      html +
      `<p class="meta">${recipe.cuisine} - ${recipe.difficulty} - ${recipe.prepTimeMinutes}mins</p>`;
    html =
      html +
      `<p class="rating">★ ${recipe.rating} (${recipe.reviewCount} reviews)</p>`;
    html = html + "</div>";
    html = html + "</div>";
  }

  recipeList.innerHTML = html;
}

// TODO Step 3: Callback that receives the Response and parses JSON
function onSearchResponseReady(response) {
  response.json().then(onSearchDataReady);
}

// TODO Step 4: Click handler that reads input and starts fetch
function onSearchClick() {
  const query = searchInput.value.trim();

  // don't fetch is the box is empty of only spaces
  if (query === "") {
    status.innerText = "Please type something to search";
    return;
  }

  status.innerText = `Searching for ${query}...`;
  recipeList.innerHTML = "";

  fetch("https://dummyjson.com/recipes/search?q=" + query).then(
    onSearchResponseReady,
  );
}

function onSearchKeydown(event) {
  if (event.key === "Enter") {
    onSearchClick();
  }
}

function clearResults() {
  recipeList.innerHTML = "";
  searchInput.value = "";
  status.innerText = "Please type something to search";
}

// TODO Step 5: Register event listener
searchButton.addEventListener("click", onSearchClick);
searchInput.addEventListener("keydown", onSearchKeydown);

fetch("https://dummyjson.com/recipes/search?q=chicken").then(
  onSearchResponseReady,
);
