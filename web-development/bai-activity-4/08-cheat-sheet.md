# 08 — Cheat Sheet

Quick reference for all activities. Keep this open while you work.

---

## The Pattern (Memorise This)

```js
// 1. Get elements
const recipeName = document.getElementById('recipeName');
const recipeImage = document.getElementById('recipeImage');

// 2. Callback for FINAL data → updates the page
function onRecipeReady(recipe) {
    recipeName.innerText = recipe.name;
    recipeImage.src = recipe.image;
    recipeImage.alt = recipe.name;
}

// 3. Callback for RESPONSE → parses JSON
function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

// 4. Start the fetch
fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

---

## API URLs

| Need | URL |
|------|-----|
| Single recipe (id 1–50) | `https://dummyjson.com/recipes/1` |
| All recipes (30 by default) | `https://dummyjson.com/recipes` |
| Limit results | `https://dummyjson.com/recipes?limit=6` | — returns 6 of 50 |
| Search by name | `https://dummyjson.com/recipes/search?q=pizza` | — returns 2 matching recipes |
| Search + limit | `https://dummyjson.com/recipes/search?q=pizza&limit=6` | — limit caps at total matches (2 for pizza) |

> Tip: paste any URL into your browser to see the JSON.

---

## Recipe Object Properties

```js
recipe.id                // number — 1
recipe.name              // string — "Classic Margherita Pizza"
recipe.image             // string — URL to image
recipe.cuisine           // string — "Italian"
recipe.difficulty        // string — "Easy"
recipe.prepTimeMinutes   // number — 20
recipe.cookTimeMinutes   // number — 15
recipe.servings          // number — 4
recipe.rating            // number — 4.6
recipe.reviewCount       // number — 98
recipe.mealType          // array — ["Dinner"]
recipe.ingredients       // array — ["Pizza dough", "Tomato sauce", ...]
recipe.instructions      // array — ["Preheat the oven...", ...]
recipe.caloriesPerServing// number — 300
recipe.tags              // array — ["Pizza", "Italian"]
```

Loop example:

```js
for (let i = 0; i < recipe.ingredients.length; i++) {
    console.log(recipe.ingredients[i]);
}
```

---

## DOM Methods

| Task | Code |
|------|------|
| Get element | `document.getElementById('myId')` |
| Set plain text | `element.innerText = 'Hello'` |
| Set HTML | `element.innerHTML = '<li>Hello</li>'` |
| Set image source | `element.src = recipe.image` |
| Set image alt | `element.alt = recipe.name` |
| Get input value | `element.value` |
| Listen for click | `button.addEventListener('click', onClick)` |
| Listen for submit | `form.addEventListener('submit', onSubmit)` |

**Remember:** `innerText` for text, `innerHTML` for HTML tags.

---

## Do and Don't

| ✅ Do | ❌ Don't |
|-------|---------|
| `function onResponseReady(response) { }` | `const onResponseReady = (response) => { }` |
| `.then(onResponseReady)` | `.then(onResponseReady())` |
| `response.json().then(onRecipeReady)` | `response.json` (missing `()`) |
| `document.getElementById('recipeName')` | `document.querySelector('#recipeName')` (use getElementById in these activities) |
| `let html = ''; html = html + '...'` | Trying to use `+=` before learning it (fine, but `html = html +` is clearer for now) |
| `fetch(url).then(onResponseReady)` | `await fetch(url)` |

---

## JSON Methods

| Task | Code |
|------|------|
| JSON text → object | `JSON.parse(jsonString)` |
| Object → JSON text | `JSON.stringify(value)` |
| Object → formatted JSON | `JSON.stringify(value, null, 2)` |
| Save to localStorage | `localStorage.setItem('key', JSON.stringify(object))` |
| Load from localStorage | `JSON.parse(localStorage.getItem('key'))` |

**Remember:** `response.json()` already parses for you — do not call `JSON.parse()` on its result. Use `JSON.parse`/`stringify` only when you handle JSON text yourself (e.g. `localStorage`). `JSON.parse` requires valid JSON (double quotes, no trailing commas) or it will throw.

---

## Debugging Checklist

1. **Open Console:** F12 → Console tab. Red text = error.
2. **`null` error?** Your `getElementById` id doesn't match HTML. Check spelling and case.
3. **Nothing appears but no error?** Did you forget `response.json().then(...)`? You need **two** `.then()` steps.
4. **Raw `<li>` text on page?** You used `innerText` instead of `innerHTML` for HTML.
5. **404 error?** Check URL — `https://dummyjson.com/recipes/1` not `recipe` or `recipess`.
6. **`undefined` for `recipe.name`?** You may be looping over `data` instead of `data.recipes`.
7. **Network tab:** F12 → Network → reload page → click the `recipes` request → Preview tab to see JSON.

---

## Minimal Examples — Copy and Adapt

**Single recipe** (`/recipes/1` returns one object):

```js
const title = document.getElementById('title');

function onRecipeReady(recipe) {
    title.innerText = recipe.name;
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

**List / Search** (`/recipes` or `/search?q=...` returns `{ recipes: [...] }`):

```js
const title = document.getElementById('title');
const list = document.getElementById('list');

function onDataReady(data) {
    const recipes = data.recipes;
    title.innerText = 'Found ' + recipes.length + ' recipes';

    let html = '';
    for (let i = 0; i < recipes.length; i++) {
        html = html + '<li>' + recipes[i].name + '</li>';
    }
    list.innerHTML = html;
}

function onResponseReady(response) {
    response.json().then(onDataReady);
}

fetch('https://dummyjson.com/recipes').then(onResponseReady);
```

---

**Previous:** [07 — Displaying Data on the Page ←](07-displaying-data-on-the-page.md)

**Activities:**

- [Activity 1 — Fetch a Single Recipe →](activity-1/activity-1.md)
- [Activity 2 — Fetch All Recipes →](activity-2/activity-2.md)
- [Activity 3 — Search Recipes →](activity-3/activity-3.md)
