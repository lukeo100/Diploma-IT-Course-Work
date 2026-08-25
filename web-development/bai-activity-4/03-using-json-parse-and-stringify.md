# 03 — Using `JSON.parse()` and `JSON.stringify()`

## JSON is Text, JavaScript Needs Objects

When an API sends data, it sends it as **JSON text** — a single string. JavaScript cannot access properties on a string (`'{"name": "Pizza"}'.name` is `undefined`). To work with the data, the text must be converted into a JavaScript object. When you want to store or send data, the reverse is needed: a JavaScript object must be converted back into JSON text.

JavaScript provides two methods for this conversion. Both are **synchronous** — they complete immediately and return a result, unlike `fetch()` which is asynchronous.

| Method | Direction | Input | Output |
|--------|-----------|-------|--------|
| `JSON.parse()` | JSON text → JavaScript value | String | Object, array, string, number, boolean, or null |
| `JSON.stringify()` | JavaScript value → JSON text | Object, array, or other value | String |

---

## `JSON.parse()` — From Text to Object

### Signature

```js
const value = JSON.parse(jsonString);
```

- `jsonString` must be valid JSON text (double-quoted keys and strings, no trailing commas, no comments).
- Returns the JavaScript value represented by the JSON.

### Basic Examples

```js
const name = JSON.parse('"Classic Margherita Pizza"');
console.log(name); // "Classic Margherita Pizza" — a string
console.log(typeof name); // "string"

const rating = JSON.parse('4.6');
console.log(rating); // 4.6 — a number

const ingredients = JSON.parse('["Pizza dough", "Tomato sauce", "Fresh mozzarella cheese"]');
console.log(ingredients); // ["Pizza dough", "Tomato sauce", "Fresh mozzarella cheese"]
console.log(ingredients.length); // 3
console.log(ingredients[0]); // "Pizza dough"
```

### Parsing a Recipe Object

```js
const jsonString = '{"id": 1, "name": "Classic Margherita Pizza", "cuisine": "Italian", "rating": 4.6}';
const recipe = JSON.parse(jsonString);

console.log(recipe.name); // "Classic Margherita Pizza"
console.log(recipe.cuisine); // "Italian"
console.log(recipe.rating); // 4.6
```

After `JSON.parse()`, `recipe` is a normal JavaScript object and you can use dot notation and bracket notation as usual.

### What Happens with Invalid JSON

If the string is not valid JSON, `JSON.parse()` throws an error and stops execution:

```js
// ❌ Single quotes are not valid in JSON
JSON.parse("{'name': 'Pizza'}"); // SyntaxError

// ❌ Missing quotes around key
JSON.parse('{name: "Pizza"}'); // SyntaxError

// ❌ Trailing comma
JSON.parse('{"name": "Pizza",}'); // SyntaxError

// ✅ Correct — double quotes everywhere
JSON.parse('{"name": "Pizza"}'); // { name: "Pizza" }
```

When the JSON comes from an API, it is always valid. Errors usually happen only when you write JSON by hand.

---

## `JSON.stringify()` — From Object to Text

### Signature

```js
const jsonString = JSON.stringify(value);
const jsonStringFormatted = JSON.stringify(value, null, 2);
```

- `value` is a JavaScript object, array, string, number, boolean, or null.
- Returns a JSON string.
- The optional `null, 2` arguments format the output with 2-space indentation for readability.

### Basic Examples

```js
const title = "Classic Margherita Pizza";
console.log(JSON.stringify(title)); // "\"Classic Margherita Pizza\""

const rating = 4.6;
console.log(JSON.stringify(rating)); // "4.6"

const ingredients = ["Pizza dough", "Tomato sauce", "Fresh mozzarella cheese"];
console.log(JSON.stringify(ingredients));
// '["Pizza dough","Tomato sauce","Fresh mozzarella cheese"]'
```

### Stringifying a Recipe Object

```js
const recipe = {
    id: 1,
    name: "Classic Margherita Pizza",
    cuisine: "Italian",
    rating: 4.6,
    ingredients: ["Pizza dough", "Tomato sauce", "Fresh mozzarella cheese"]
};

const jsonString = JSON.stringify(recipe);
console.log(jsonString);
// '{"id":1,"name":"Classic Margherita Pizza","cuisine":"Italian","rating":4.6,"ingredients":["Pizza dough","Tomato sauce","Fresh mozzarella cheese"]}'

// Formatted for readability — useful for console logging
const formatted = JSON.stringify(recipe, null, 2);
console.log(formatted);
/*
{
  "id": 1,
  "name": "Classic Margherita Pizza",
  "cuisine": "Italian",
  "rating": 4.6,
  "ingredients": [
    "Pizza dough",
    "Tomato sauce",
    "Fresh mozzarella cheese"
  ]
}
*/
```

The compact version (without `null, 2`) is used when storing or sending data. The formatted version is useful when you want to inspect the data in the console.

---

## Why You Need Both

### `fetch()` Already Parses for You

When you use `fetch()`, you do not need to call `JSON.parse()` directly. The method `response.json()` reads the response body and parses it internally:

```js
function onRecipeReady(recipe) {
    console.log(recipe.name); // already a JavaScript object
}

function onResponseReady(response) {
    response.json().then(onRecipeReady); // .json() does the parsing
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

`response.json()` is equivalent to doing `JSON.parse()` on the response text, but it handles the asynchronous reading of the network stream at the same time.

You only use `JSON.parse()` and `JSON.stringify()` directly when you handle JSON text yourself, outside of `fetch()`.

### Storing Data in `localStorage`

`localStorage` can only store strings. To save an object, you must stringify it. To get it back, you must parse it.

```js
const recipe = {
    id: 1,
    name: "Classic Margherita Pizza",
    cuisine: "Italian"
};

// Save — object → string
const jsonString = JSON.stringify(recipe);
localStorage.setItem('favouriteRecipe', jsonString);

// Load — string → object
const savedString = localStorage.getItem('favouriteRecipe');
const savedRecipe = JSON.parse(savedString);
console.log(savedRecipe.name); // "Classic Margherita Pizza"
```

Forgetting `JSON.stringify()` when saving, or `JSON.parse()` when loading, are common mistakes:

```js
// ❌ Saving without stringify — stores "[object Object]" which cannot be parsed back
localStorage.setItem('recipe', recipe);

// ❌ Using the stored string as if it were already an object
const saved = localStorage.getItem('favouriteRecipe');
console.log(saved.name); // undefined — saved is still a string
console.log(JSON.parse(saved).name); // ✅ correct — parse first
```

### Round Trip

Parsing and stringifying are reversible. A round trip should give you back the original structure:

```js
const original = {
    name: "Vegetarian Stir-Fry",
    cookTimeMinutes: 20,
    ingredients: ["Tofu", "Broccoli", "Soy sauce"]
};

const jsonString = JSON.stringify(original);
const copy = JSON.parse(jsonString);

console.log(copy.name); // "Vegetarian Stir-Fry"
console.log(copy.ingredients[1]); // "Broccoli"
console.log(copy.cookTimeMinutes); // 20
```

---

## What `JSON.stringify()` Omits and Transforms

JSON only supports data, not behaviour. Some JavaScript values cannot be represented in JSON:

| JavaScript Value | Result in `JSON.stringify()` |
|------------------|------------------------------|
| Function | Omitted (removed from objects, replaced with `null` in arrays) |
| `undefined` | Omitted from objects, replaced with `null` in arrays |
| `Infinity`, `NaN` | Converted to `null` |
| `Date` object | Converted to an ISO date string, e.g. `"2026-05-13T00:00:00.000Z"` |

```js
function myHelper() {}

const data = {
    name: "Pizza",
    rating: undefined,       // omitted
    helper: myHelper,        // omitted — functions cannot be stored in JSON
    rating2: NaN,            // becomes null
    created: new Date('2026-05-13') // becomes "2026-05-13T00:00:00.000Z"
};

console.log(JSON.stringify(data));
// '{"name":"Pizza","rating2":null,"created":"2026-05-13T00:00:00.000Z"}'
```

This is not a problem for recipe data from DummyJSON, which only contains strings, numbers, booleans, arrays, and objects — all of which are fully supported.

---

## Common Mistakes

| Mistake | Why it fails | Fix |
|---------|--------------|-----|
| `JSON.parse(recipe)` where `recipe` is already an object | `JSON.parse()` expects a string, not an object | Only parse strings: `JSON.parse(jsonString)` |
| `JSON.stringify('{"name": "Pizza"}')` where the value is already a JSON string | Double-encodes — result is a string containing escaped JSON | Only stringify objects: `JSON.stringify(recipeObject)` |
| Forgetting the second parse after `localStorage.getItem()` | `getItem()` always returns a string | `const recipe = JSON.parse(localStorage.getItem('key'))` |
| Using single quotes in JSON text | JSON requires double quotes | `JSON.parse('{"name": "Pizza"}')` not `"{'name': 'Pizza'}"` |
| Calling `response.json()` and then `JSON.parse()` again | `response.json()` already returns a parsed object | Use the object directly — do not parse again |

---

## How This Connects to the Activities

In Activities 1–3 you will use `response.json().then(callback)` to get parsed recipe objects from the API:

```js
function onRecipeReady(recipe) {
    // recipe is already parsed — no JSON.parse() needed here
    const recipeName = document.getElementById('recipeName');
    recipeName.innerText = recipe.name;
}

function onResponseReady(response) {
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

If you later save that recipe to `localStorage` or send it elsewhere, you will use `JSON.stringify()` and `JSON.parse()` explicitly:

```js
function onRecipeReady(recipe) {
    // 1. Display it
    const recipeName = document.getElementById('recipeName');
    recipeName.innerText = recipe.name;

    // 2. Save it for later — object → string
    const jsonString = JSON.stringify(recipe);
    localStorage.setItem('lastRecipe', jsonString);
}

// Later, on another page or after reload — string → object
const savedString = localStorage.getItem('lastRecipe');
if (savedString !== null) {
    const savedRecipe = JSON.parse(savedString);
    console.log(savedRecipe.name);
}
```

---

## Key Takeaways

- `JSON.parse(jsonString)` converts a JSON **string** into a JavaScript value. Use it when you have JSON text that you need to work with.
- `JSON.stringify(value)` converts a JavaScript value into a JSON **string**. Use it when you need to store or transmit data.
- `JSON.parse()` requires valid JSON (double-quoted keys and strings, no trailing commas). Invalid JSON throws a syntax error.
- `response.json()` in the `fetch` pattern already parses for you — do not call `JSON.parse()` on its result.
- `localStorage` stores only strings, so you must `stringify` when saving and `parse` when loading.
- Both methods are synchronous and return immediately.

---

**Previous:** [02 — What is JSON? ←](02-what-is-json.md)

**Next:** [04 — Callback Functions →](04-callback-functions.md)
