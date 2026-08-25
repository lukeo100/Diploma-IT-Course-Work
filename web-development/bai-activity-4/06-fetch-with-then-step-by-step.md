# 06 — Putting It Together: `fetch()` with `.then()` Step by Step

Now you know what `fetch()` and `.then()` do separately. Let's put them together into the **exact pattern** you will use in all three activities.

> **Tip if you are new to DOM:** The first example below uses `console.log`. The page-update version with `getElementById` is in the next reading (`07`). You can try the `console.log` version first, then add the page update.

---

## The Pattern — Two Callbacks, Two `.then()` Calls

Every `fetch` in these activities follows the same three lines:

```js
// 1. Define what to do with the FINAL data
function onRecipeReady(recipe) {
    console.log(recipe.name);
}

// 2. Define what to do with the RESPONSE (and parse it)
function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

// 3. Start the request
fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

That's it. Read it bottom to top to follow the timeline:

- **Line 3** runs first — sends the request.
- **Line 2** runs later — when the server replies, parse the JSON.
- **Line 1** runs last — when parsing is done, use the recipe.

> You can define the functions in any order, but the names must match what you pass to `.then()`.

---

## Step 1 — Fetch a Single Recipe (console first)

Start with `console.log` to confirm the fetch works, before touching the page:

```js
function onRecipeReady(recipe) {
    console.log(recipe.name); // should log "Classic Margherita Pizza"
    console.log(recipe.cuisine);
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

Open `https://dummyjson.com/recipes/1` in a browser tab first to see the raw JSON, then run the code above and check **F12 → Console**.

Once that logs correctly, add the page update (full version is also in `07`):

```js
const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');

function onRecipeReady(recipe) {
    console.log(recipe.name); // keep the log for debugging
    recipeName.innerText = recipe.name;
    recipeImage.src = recipe.image;
    recipeImage.alt = recipe.name;
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

---

## Step 2 — Fetch a List of Recipes

The list endpoint returns an **object with an array inside**:

```json
{
  "recipes": [ { "id": 1, ... }, { "id": 2, ... } ],
  "total": 50
}
```

So the callback receives `data`, and you use `data.recipes`:

```js
const recipeList = document.getElementById('recipeList');

function onDataReady(data) {
    const recipes = data.recipes;

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        html = html + '<p>' + recipes[i].name + '</p>';
    }

    recipeList.innerHTML = html;
}

function onResponseReady(response) {
    response.json().then(onDataReady);
}

fetch('https://dummyjson.com/recipes').then(onResponseReady);
```

Notice the pattern is identical — only the final callback (`onDataReady`) changes to loop through an array.

---

## Step 3 — Fetch Based on User Input (Search) — same pattern inside a click

The `fetch` itself is unchanged — it just runs **when the user clicks** instead of on page load. The click handler builds the URL from the input:

```js
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const recipeList = document.getElementById('recipeList');

// These two are the same two-step pattern as before
function onSearchDataReady(data) {
    console.log('found', data.recipes.length);
    const recipes = data.recipes;

    if (recipes.length === 0) {
        recipeList.innerHTML = '<p>No recipes found for "' + searchInput.value + '"</p>';
        return;
    }

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        html = html + '<p>' + recipes[i].name + '</p>';
    }
    recipeList.innerHTML = html;
}

function onSearchResponseReady(response) {
    response.json().then(onSearchDataReady);
}

// This is the only new part: read input and start the fetch on click
function onSearchClick() {
    const query = searchInput.value;
    fetch('https://dummyjson.com/recipes/search?q=' + query).then(onSearchResponseReady);
}

searchButton.addEventListener('click', onSearchClick);
```

> You will learn `.value` and `getElementById` in detail on the next page (`07`). For now, notice the `fetch` + two callbacks are identical to Steps 1 and 2.

---

## Comparing the Three Variations

| Scenario | URL | What the final callback receives |
|----------|-----|----------------------------------|
| Single recipe | `https://dummyjson.com/recipes/1` | One recipe object (`recipe.name`, `recipe.image`, ...) |
| All recipes | `https://dummyjson.com/recipes` | Object with `data.recipes` array |
| Search | `https://dummyjson.com/recipes/search?q=pizza` | Object with `data.recipes` array (filtered) |

All three use the same structure:

```
fetch(url).then(onResponseReady)
                 │
                 ▼
         response.json().then(onDataReady)
                              │
                              ▼
                     update page with getElementById
```

---

## Checklist Before You Move On

- [ ] You call `fetch(url)` with a **string** URL in quotes
- [ ] You chain `.then()` with a **named function** — no brackets, no `=>`
- [ ] That function calls `response.json().then(nextFunction)`
- [ ] The second function receives the **parsed object** and uses `getElementById` to update the page
- [ ] You open the browser console (F12) and see no errors

---

**Previous:** [05 — Promises and .then() ←](05-promises-and-then.md)

**Next:** [07 — Displaying Data on the Page →](07-displaying-data-on-the-page.md)
