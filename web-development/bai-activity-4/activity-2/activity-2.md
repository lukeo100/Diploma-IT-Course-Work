# Activity 2: Fetch and Display All Recipes

## Objective

Fetch **all** recipes from `https://dummyjson.com/recipes` and display them as cards on the page. Each card should show the recipe image, name, cuisine, difficulty, and rating.

This API endpoint returns an **object** with a `recipes` array inside — not an array directly. You will need to access `data.recipes`.

> **Rules:** Do not use arrow functions (`=>`) and do not use `async`/`await`. Use only named callback functions with `.then()`.

## Files

- `index.html` — Page HTML with a container `<div id="recipeList">`
- `styles.css` — Styling (already complete)
- `script.js` — Write your JavaScript here

## Preview of the HTML

Your `index.html` already contains:

```html
<p id="status" class="status">Loading recipes...</p>
<div id="recipeList" class="grid"></div>
```

You will fill `#recipeList` with cards and update `#status` when done. Open the URL `https://dummyjson.com/recipes` in a new tab first — inspect the raw JSON shape before you code.

## Step 1: Get Element References

At the top of `script.js`:

```js
const recipeList = document.getElementById('recipeList');
const status = document.getElementById('status');
```

- `recipeList` is where you will insert all the recipe cards
- `status` shows how many recipes were loaded (or an error)

## Step 2: Create the Callback That Receives the Data

The response from `https://dummyjson.com/recipes` looks like this:

```json
{
  "recipes": [
    { "id": 1, "name": "Classic Margherita Pizza", "image": "...", ... },
    { "id": 2, "name": "Vegetarian Stir-Fry", ... }
  ],
  "total": 50,
  "skip": 0,
  "limit": 30
}
```

So your callback receives `data`, and the array is `data.recipes`.

Create this function:

```js
function onDataReady(data) {
    const recipes = data.recipes;

    status.innerText = 'Found ' + recipes.length + ' recipes';

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        const recipe = recipes[i];
        html = html + '<div class="card">';
        html = html + '<img src="' + recipe.image + '" alt="' + recipe.name + '">';
        html = html + '<div class="card-body">';
        html = html + '<h3>' + recipe.name + '</h3>';
        html = html + '<p class="meta">' + recipe.cuisine + ' · ' + recipe.difficulty + '</p>';
        html = html + '<p class="rating">★ ' + recipe.rating + '</p>';
        html = html + '<p class="time">Prep: ' + recipe.prepTimeMinutes + ' mins</p>';
        html = html + '</div>';
        html = html + '</div>';
    }

    recipeList.innerHTML = html;
}
```

Key points:
- `data.recipes` is the array — don't loop over `data` itself
- Build one big HTML string with `html = html + '...'`
- Use `innerHTML` to insert HTML tags (not `innerText`, which would show raw `<div>` text)
- Inside the loop, `recipes[i]` is one recipe object

## Step 3: Create the Response Callback

As in Activity 1, `fetch` first gives you a Response object. You need to parse it:

```js
function onResponseReady(response) {
    response.json().then(onDataReady);
}
```

## Step 4: Call fetch()

At the bottom of your file:

```js
fetch('https://dummyjson.com/recipes').then(onResponseReady);
```

### The full chain

```
fetch('https://dummyjson.com/recipes')
   → onResponseReady(response)
      → response.json()
         → onDataReady(data)   // data.recipes is the array
            → loop + build HTML → recipeList.innerHTML = html
```

## Step 5: Test in the Browser

1. Open `index.html` via **Live Server / Live Preview** (not `file://` double-click) — `fetch` needs `http://`.
2. You should see "Found 30 recipes" and 30 cards appear. The API has 50 recipes total, but returns 30 by default (`limit:30`).
3. Each card should show an image, name, cuisine and rating
4. Open Developer Tools → Console — check for errors
5. Compare with the raw JSON at `https://dummyjson.com/recipes` in another tab

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Looping over `data` instead of `data.recipes` | `data` is an object; the array is `data.recipes` |
| `fetch(url).then(onDataReady)` directly | You still need the `onResponseReady` step to call `response.json()` first |
| Using `innerText` for HTML | Use `innerHTML` when your string contains `<div>`, `<img>`, etc. |
| `'<img src=' + recipe.image + '>'` missing quotes | Wrap the value in quotes: `'<img src="' + recipe.image + '" alt="' + recipe.name + '">'` — missing quotes breaks the HTML |
| Arrow functions | Use `function onDataReady(data) { }` not `(data) => { }` |

## Bonus Challenges

1. **Show more info:** Add `recipe.cookTimeMinutes`, `recipe.servings`, or `recipe.mealType` to each card
2. **Limit the results:** Change the URL to `https://dummyjson.com/recipes?limit=6` to fetch only 6 recipes
3. **Handle the image:** If an image fails to load, the `alt` text shows — make sure you set it to `recipe.name`

## Sample Solution

Compare with `sample/script.js` if you get stuck — try the `TODO`s first.

## Summary

In this activity you learned:
- How the `/recipes` endpoint returns an object with a `recipes` array inside
- How to chain `.then()` callbacks: `fetch` → `response.json()` → data handler
- How to loop through an array with a `for` loop
- How to build HTML as a string and inject it with `getElementById` + `.innerHTML`
- How to update a status element with `.innerText`
