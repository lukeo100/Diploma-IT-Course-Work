# Activity 1: Fetch and Display a Single Recipe

## Objective

Fetch **one** recipe from the DummyJSON API and display its details on the page using `fetch()`, callback functions with `.then()`, and `getElementById`.

You will fetch recipe **#1** (Classic Margherita Pizza) from `https://dummyjson.com/recipes/1` and show its name, image, cuisine, difficulty, prep time, ingredients and instructions.

> **Rules:** Do not use arrow functions (`=>`) and do not use `async`/`await`. Use only named callback functions with `.then()` — see the examples below.

## Files

- `index.html` — The page HTML (already complete)
- `styles.css` — Styling (already complete)
- `script.js` — Write your JavaScript here

## Preview of the HTML

Your `index.html` already contains elements with these ids — you will fill them with JavaScript:

```html
<h2 id="recipeName"></h2>
<img id="recipeImage">
<p id="recipeCuisine"></p>
<p id="recipeDifficulty"></p>
<p id="recipePrepTime"></p>
<ul id="recipeIngredients"></ul>
<ol id="recipeInstructions"></ol>
<p id="recipeRating"></p>
```

## Step 1: Get Element References

At the **top** of `script.js`, get references to every element you need to update:

```js
const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');
const recipeCuisine = document.getElementById('recipeCuisine');
const recipeDifficulty = document.getElementById('recipeDifficulty');
const recipePrepTime = document.getElementById('recipePrepTime');
const recipeIngredients = document.getElementById('recipeIngredients');
const recipeInstructions = document.getElementById('recipeInstructions');
const recipeRating = document.getElementById('recipeRating');
```

- `document.getElementById()` finds the element with that `id`
- Store it in a `const` so you can use it later without searching again

## Step 2: Create Your Callback Functions

You need **two** callback functions. `fetch()` is asynchronous, so you use `.then()` to run a function when the data arrives.

### 2a. Function to handle the parsed recipe

This function receives the **final recipe object** and puts it on the page:

```js
function onRecipeReady(recipe) {
    recipeName.innerText = recipe.name;
    recipeImage.src = recipe.image;
    recipeImage.alt = recipe.name;
    recipeCuisine.innerText = 'Cuisine: ' + recipe.cuisine;
    recipeDifficulty.innerText = 'Difficulty: ' + recipe.difficulty;
    recipePrepTime.innerText = 'Prep time: ' + recipe.prepTimeMinutes + ' mins';
    recipeRating.innerText = 'Rating: ' + recipe.rating + ' (' + recipe.reviewCount + ' reviews)';

    // Build ingredients list as HTML string
    let ingredientsHTML = '';
    for (let i = 0; i < recipe.ingredients.length; i++) {
        ingredientsHTML = ingredientsHTML + '<li>' + recipe.ingredients[i] + '</li>';
    }
    recipeIngredients.innerHTML = ingredientsHTML;

    // Build instructions list as HTML string
    let instructionsHTML = '';
    for (let i = 0; i < recipe.instructions.length; i++) {
        instructionsHTML = instructionsHTML + '<li>' + recipe.instructions[i] + '</li>';
    }
    recipeInstructions.innerHTML = instructionsHTML;
}
```

> Notice: `recipe` is a normal JavaScript object. You access properties with `recipe.name`, `recipe.image`, etc.

### 2b. Function to handle the fetch Response

`fetch()` first gives you a **Response object**, not the JSON yet. You must call `.json()` on it, which also returns a Promise:

```js
function onResponseReady(response) {
    response.json().then(onRecipeReady);
}
```

- `response.json()` parses the JSON text into a JavaScript object
- `.then(onRecipeReady)` says: "when parsing is done, call `onRecipeReady` with the result"

## Step 3: Call fetch()

At the bottom of your file, make the request. Chain `.then()` with your callback **by name** (no brackets, no arrow function):

```js
fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

This line means: "Fetch this URL, and when the response arrives, call `onResponseReady`."

### The full flow

```
fetch(url)  →  onResponseReady(response)  →  response.json()  →  onRecipeReady(recipe)  →  update page
```

## Step 4: Test in the Browser

1. Open `https://dummyjson.com/recipes/1` in a browser tab first — see the raw JSON structure.
2. Then open `index.html` via **Live Server / Live Preview** (don’t double-click the file — `fetch` needs `http://`).
3. You should see the Classic Margherita Pizza details appear
4. Open Developer Tools (F12) → Console — there should be no errors
5. Try changing the URL in `script.js` to `https://dummyjson.com/recipes/5` (Mango Salsa Chicken) and refresh — you should see a different recipe
6. Try `https://dummyjson.com/recipes/2` for Vegetarian Stir-Fry

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `fetch(url).then(onResponseReady())` with brackets | Remove brackets: `.then(onResponseReady)` — you pass the function, you don't call it |
| `fetch(url).then(() => { ... })` | Don't use arrow functions — create a named `function` and pass its name |
| `response.json` without `()` | It is a function: `response.json()` |
| Using `innerText` for HTML with `<li>` | Use `innerHTML` when you are inserting HTML tags, `innerText` for plain text |
| Forgetting `.alt` on the image | Always set `recipeImage.alt` for accessibility |

## Bonus Challenge

Once it works with recipe `1`, try using a variable for the id — this shows string concatenation with `+`:

```js
const recipeId = 1;

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

// '+' joins the number onto the URL string
fetch('https://dummyjson.com/recipes/' + recipeId).then(onResponseReady);
```

Change `recipeId` to any number from `1` to `50` to see different recipes. All 8 elements (`recipeName`, `recipeImage`, etc.) were listed in Step 1 — if this is a lot, focus on `recipeName` + `recipeImage` first, then add the rest.

## Sample Solution

If you get stuck, compare with `sample/script.js` in this folder — try the `TODO`s first.

## Summary

In this activity you learned:
- How to call `fetch()` to request data from an API
- How to use `.then()` with a **named callback function** (no arrow functions, no `async`/`await`)
- Why you need **two** `.then()` steps: one for the Response, one for the JSON
- How to use `document.getElementById()` to get elements
- How to populate the page with `.innerText`, `.innerHTML`, and `.src`
