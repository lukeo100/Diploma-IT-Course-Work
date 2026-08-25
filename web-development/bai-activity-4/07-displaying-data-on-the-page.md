# 07 — Displaying Data on the Page with `getElementById`

Fetching data is only half the job — you also need to **show it** on the page. For that we use `document.getElementById()` together with `.innerText`, `.innerHTML`, and `.src`.

---

## 1. Get the Element

Every element you want to change must have an `id` in the HTML:

```html
<h2 id="recipeName"></h2>
<img id="recipeImage" src="" alt="">
<p id="recipeRating"></p>
<ul id="recipeIngredients"></ul>
```

In JavaScript, you get a reference to it once at the top of your file:

```js
const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');
const recipeRating = document.getElementById('recipeRating');
const recipeIngredients = document.getElementById('recipeIngredients');
```

- `document` means "the whole page"
- `getElementById('recipeName')` searches for `id="recipeName"`
- Store it in a `const` so you can reuse it without searching again

> If `getElementById` returns `null` in the console, check that the `id` in HTML exactly matches the string in JavaScript (case-sensitive, no typos).

---

## 2. Update Text with `.innerText` and `.innerHTML`

### Plain text — use `.innerText`

When you just want to set text with no HTML tags:

```js
function onRecipeReady(recipe) {
    recipeName.innerText = recipe.name;
    recipeRating.innerText = 'Rating: ' + recipe.rating;
}
```

### HTML — use `.innerHTML`

When your string **contains HTML tags** like `<li>` or `<div>`, you must use `.innerHTML` so the browser parses the tags:

```js
function onRecipeReady(recipe) {
    // Build a string of <li> tags
    let html = '';
    for (let i = 0; i < recipe.ingredients.length; i++) {
        html = html + '<li>' + recipe.ingredients[i] + '</li>';
    }

    // Insert the HTML — browser will create real list items
    recipeIngredients.innerHTML = html;
}
```

| Property | When to use | Example |
|----------|-------------|---------|
| `.innerText` | Plain text, no tags | `recipeName.innerText = recipe.name` |
| `.innerHTML` | String contains `<li>`, `<div>`, `<img>` etc. | `recipeIngredients.innerHTML = '<li>...</li>'` |

> Never use `.innerText` for HTML — you will see raw `<li>` text on the page instead of a list.

---

## 3. Update Images with `.src` and `.alt`

Images have special properties:

```js
function onRecipeReady(recipe) {
    recipeImage.src = recipe.image;  // URL of the image
    recipeImage.alt = recipe.name;   // Text shown if image fails to load
}
```

- `.src` is the image URL (e.g. `https://cdn.dummyjson.com/recipe-images/1.webp`)
- `.alt` is important for accessibility — always set it

---

## 4. Building Cards in a Loop

For Activity 2 and 3 you will create many cards at once. The trick is to **build one big HTML string** in a loop, then set it once:

```js
const recipeList = document.getElementById('recipeList');

function onDataReady(data) {
    const recipes = data.recipes;

    let html = '';

    for (let i = 0; i < recipes.length; i++) {
        const recipe = recipes[i];

        html = html + '<div class="card">';
        html = html + '<img src="' + recipe.image + '" alt="' + recipe.name + '">';
        html = html + '<h3>' + recipe.name + '</h3>';
        html = html + '<p>' + recipe.cuisine + ' · ' + recipe.difficulty + '</p>';
        html = html + '</div>';
    }

    recipeList.innerHTML = html;
}
```

Each time through the loop you **append** (`html = html + ...`) another card to the string. At the end, one assignment to `innerHTML` creates all the cards.

> Tip for building cards: It’s easy to miss a quote when concatenating. Always write the attribute as `'"' + recipe.image + '"'` with quotes around the value. Check `console.log(recipe)` inside the loop (F12 → Console) to see what properties each recipe has.

---

## 5. Handling Empty Results (for Activity 3)

This is only needed in `activity-3` when a search finds nothing. `data.recipes` will be an empty array (`length === 0`) — show a message instead of a blank page:

```js
function onSearchDataReady(data) {
    const recipes = data.recipes;

    if (recipes.length === 0) {
        recipeList.innerHTML = '<p>No recipes found. Try searching for "pizza" or "chicken".</p>';
        return; // stops the function so the loop below doesn't run
    }

    // ... otherwise build cards as in Section 4
}
```

You don’t need this check in Activities 1 and 2.

---

## Putting It All Together

Here is a minimal complete example for a single recipe:

```html
<!-- index.html -->
<h2 id="recipeName">Loading...</h2>
<img id="recipeImage" src="" alt="">
<p id="recipeCuisine"></p>
<ul id="recipeIngredients"></ul>
```

```js
// script.js
const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');
const recipeCuisine = document.getElementById('recipeCuisine');
const recipeIngredients = document.getElementById('recipeIngredients');

function onRecipeReady(recipe) {
    recipeName.innerText = recipe.name;
    recipeImage.src = recipe.image;
    recipeImage.alt = recipe.name;
    recipeCuisine.innerText = 'Cuisine: ' + recipe.cuisine;

    let html = '';
    for (let i = 0; i < recipe.ingredients.length; i++) {
        html = html + '<li>' + recipe.ingredients[i] + '</li>';
    }
    recipeIngredients.innerHTML = html;
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

1. `getElementById` — get references at the top
2. `fetch` + `.then()` — get data from the API
3. `innerText` / `innerHTML` / `src` — put data on the page

---

**Previous:** [06 — Fetch with .then() Step by Step ←](06-fetch-with-then-step-by-step.md)

**Next:** [08 — Cheat Sheet →](08-cheat-sheet.md)
