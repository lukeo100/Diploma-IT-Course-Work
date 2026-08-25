# Activity 3: Search Recipes on Button Click

## Objective

Add a **search box and button**. When the user types a word and clicks Search, fetch matching recipes from `https://dummyjson.com/recipes/search?q=SEARCH_TERM` and display the results as cards. If no recipes match, show a friendly message.

This activity combines everything from Activities 1 and 2 **plus** reading user input and handling an event.

> **Rules:** Do not use arrow functions (`=>`) and do not use `async`/`await`. Use only named callback functions with `.then()`.

## Files

- `index.html` — Page HTML with an input, a button, and a results container
- `styles.css` — Styling (already complete)
- `script.js` — Write your JavaScript here

## Preview of the HTML

Your `index.html` already contains:

```html
<input type="text" id="searchInput" placeholder="Try pizza, chicken, pasta...">
<button id="searchButton">Search</button>
<p id="status">Type a food and click Search</p>
<div id="recipeList"></div>
```

You will:

1. Read what the user typed from `#searchInput`
2. Fetch from the search URL when `#searchButton` is clicked
3. Fill `#recipeList` and update `#status`

## Step 1: Get Element References

At the top of `script.js`:

```js
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const recipeList = document.getElementById('recipeList');
const status = document.getElementById('status');
```

## Step 2: Create the Data Callback

The search endpoint returns the same shape as `/recipes` — an object with a `recipes` array:

```json
{
  "recipes": [ { "name": "Classic Margherita Pizza", ... } ],
  "total": 2
}
```

So your callback again uses `data.recipes`. This time, also handle the case where nothing was found:

```js
function onSearchDataReady(data) {
    const recipes = data.recipes;

    if (recipes.length === 0) {
        status.innerText = 'No recipes found for "' + searchInput.value + '"';
        recipeList.innerHTML = '<p class="empty">Try searching for "pizza", "chicken", or "pasta".</p>';
        return;
    }

    status.innerText = 'Found ' + recipes.length + ' recipes for "' + searchInput.value + '"';

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        const recipe = recipes[i];
        html = html + '<div class="card">';
        html = html + '<img src="' + recipe.image + '" alt="' + recipe.name + '">';
        html = html + '<div class="card-body">';
        html = html + '<h3>' + recipe.name + '</h3>';
        html = html + '<p class="meta">' + recipe.cuisine + ' · ' + recipe.difficulty + ' · ' + recipe.prepTimeMinutes + ' mins</p>';
        html = html + '<p class="rating">★ ' + recipe.rating + ' (' + recipe.reviewCount + ' reviews)</p>';
        html = html + '</div>';
        html = html + '</div>';
    }

    recipeList.innerHTML = html;
}
```

- `searchInput.value` is what the user typed — use it in the status message
- `return` after the empty case stops the function so the loop doesn't run

## Step 3: Create the Response Callback

Same as before — parse the JSON and chain the next callback:

```js
function onSearchResponseReady(response) {
    response.json().then(onSearchDataReady);
}
```

## Step 4: Create the Click Handler That Starts the Fetch

This function runs when the user clicks Search. It reads the input, checks it, and fetches:

```js
function onSearchClick() {
    const query = searchInput.value.trim();

    // Guard: don't fetch if the box is empty or only spaces
    if (query === '') {
        status.innerText = 'Please type something to search';
        return; // stops here — no fetch below will run
    }

    status.innerText = 'Searching for "' + query + '"...';
    recipeList.innerHTML = ''; // clear old results while loading

    fetch('https://dummyjson.com/recipes/search?q=' + query).then(onSearchResponseReady);
}
```

Key points:

- `searchInput.value` — the text the user typed (`.value` is for inputs, not `.innerText`)
- `.trim()` — removes spaces at the start/end, so `"  "` counts as empty
- `if (query === '') { return; }` — check **before** fetching; `return` stops the function early
- Build the URL by joining the query: `'https://dummyjson.com/recipes/search?q=' + query`

## Step 5: Register the Event Listener

At the bottom of your file, connect the button to your handler:

```js
searchButton.addEventListener('click', onSearchClick);
```

> Pass the function **by name** — no brackets, no arrow function.

### Optional Bonus (not required): Allow the Enter Key

Only try this after the button works:

```js
function onSearchKeydown(event) {
    if (event.key === 'Enter') {
        onSearchClick();
    }
}

searchInput.addEventListener('keydown', onSearchKeydown);
```

## Step 6: Test in the Browser

1. First open `https://dummyjson.com/recipes/search?q=pizza` in a tab — see the 2-result JSON shape.
2. Then open `index.html` via **Live Server / Live Preview** (`http://`, not `file://`).
3. Type `pizza` and click Search — you should see 2 pizza recipes
4. Type `chicken` and click Search — you should see 8 chicken recipes
5. Type `asdfgh` (nonsense) and click Search — you should see "No recipes found"
6. Click Search with an empty box (or just spaces) — you should see "Please type something to search"
7. Open F12 → Console and check for errors

### The full chain for this activity

```
User clicks Search
  → onSearchClick()
     → fetch('.../search?q=' + query).then(onSearchResponseReady)
        → onSearchResponseReady(response)
           → response.json().then(onSearchDataReady)
              → onSearchDataReady(data)
                 → update status + recipeList via getElementById
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `fetch('https://dummyjson.com/recipes/search?q=' + query).then(onSearchDataReady)` directly | You still need the `onSearchResponseReady` step to call `response.json()` first |
| `searchInput.value()` with brackets | `.value` is a property, not a function — no brackets |
| `searchInput.innerText` | Inputs use `.value`, not `.innerText` |
| Not handling `recipes.length === 0` | User sees a blank page — always show a message |
| `query` with spaces not working | For these activities `fetch` handles basic spaces; `encodeURIComponent(query)` is an advanced option you don’t need yet |

## Bonus Challenges

1. **Show more detail:** Add `recipe.cookTimeMinutes`, `recipe.servings`, or `recipe.tags` to each card
2. **Search on load:** At the bottom of your file, add `fetch('https://dummyjson.com/recipes/search?q=chicken').then(onSearchResponseReady);` so the page isn't empty on first load
3. **Clear button:** Add a button that clears the input and results when clicked

## Sample Solution

Completed code is in `sample/script.js` — check there after attempting the `TODO`s.

## Summary

In this activity you learned:
- How to read user input with `getElementById` + `.value`
- How to build a URL from user input and `fetch()` inside an event handler
- How to handle empty searches (`recipes.length === 0`) and empty input
- How to update the page with `.innerText` and `.innerHTML` after a search
- How the same two-callback `.then()` pattern works even when triggered by a button click
