# 02 — What is JSON?

## JSON is a Text Format for Data

**JSON** stands for **JavaScript Object Notation**. It is a text format that is used to store and exchange structured data. An API sends JSON as plain text over the network. Your JavaScript code then parses that text into objects and arrays that it can work with.

JSON is not JavaScript, but its syntax is based on JavaScript object and array notation, so it looks familiar if you already know JavaScript.

---

## JSON Syntax

JSON can represent six types of values:

| Type | Example |
|------|---------|
| **String** | `"Classic Margherita Pizza"` |
| **Number** | `300` or `4.6` |
| **Boolean** | `true` or `false` |
| **Null** | `null` |
| **Array** | `["Pizza dough", "Tomato sauce"]` |
| **Object** | `{"name": "Pizza", "rating": 4.6}` |

An object is a collection of key-value pairs enclosed in `{ }`. An array is an ordered list of values enclosed in `[ ]`.

### Example: A Single Recipe in JSON

This is the raw text the DummyJSON API returns for `https://dummyjson.com/recipes/1`:

```json
{
  "id": 1,
  "name": "Classic Margherita Pizza",
  "ingredients": [
    "Pizza dough",
    "Tomato sauce",
    "Fresh mozzarella cheese"
  ],
  "instructions": [
    "Preheat the oven to 475°F (245°C).",
    "Roll out the pizza dough and spread tomato sauce evenly."
  ],
  "prepTimeMinutes": 20,
  "cookTimeMinutes": 15,
  "servings": 4,
  "difficulty": "Easy",
  "cuisine": "Italian",
  "caloriesPerServing": 300,
  "image": "https://cdn.dummyjson.com/recipe-images/1.webp",
  "rating": 4.6,
  "mealType": ["Dinner"]
}
```

### Example: A List Response in JSON

The endpoint `https://dummyjson.com/recipes` returns an object that **contains** an array:

```json
{
  "recipes": [
    {
      "id": 1,
      "name": "Classic Margherita Pizza",
      "cuisine": "Italian"
    },
    {
      "id": 2,
      "name": "Vegetarian Stir-Fry",
      "cuisine": "Asian"
    }
  ],
  "total": 50,
  "skip": 0,
  "limit": 30
}
```

The actual recipes are inside the `recipes` property. To access them in JavaScript you use `data.recipes`.

---

## JSON Rules

JSON is stricter than JavaScript. These rules must be followed exactly, otherwise parsing will fail:

1. **Keys must be double-quoted strings.** `"name"` is valid, `name` and `'name'` are not.
2. **String values must be double-quoted.** `"Italian"` is valid, `'Italian'` is not.
3. **No trailing commas.** The last item in an object or array cannot have a comma after it.
4. **No comments.** JSON does not support `//` or `/* */`.
5. **No functions.** JSON holds only data — strings, numbers, booleans, null, arrays, and objects.

Compare JavaScript and JSON:

```js
// JavaScript object — keys can be unquoted, single quotes are allowed, trailing comma is allowed
const recipe = {
    name: 'Classic Margherita Pizza',
    rating: 4.6,
};

// JSON text — keys and string values must be double-quoted, no trailing comma
// {"name": "Classic Margherita Pizza", "rating": 4.6}
```

---

## JSON Over the Network

When the browser requests `https://dummyjson.com/recipes/1`, the server sends back JSON **text**. You can see this text by opening that URL directly in a browser tab, or in Developer Tools → Network → click the request → Preview tab.

That text is not yet a usable JavaScript object. It must be **parsed** — converted from text into objects and arrays.

When you use `fetch()`, that parsing is done for you by `response.json()` (you will see the full pattern in `06 — Fetch with .then() Step by Step`). For now, just know the two stages:

- `fetch()` gives you a `Response` (the server’s reply)
- `response.json()` converts the JSON text inside it into a JavaScript object you can use like `recipe.name`

Without that second step, you would only have the raw reply and could not do `recipe.name`.

---

## Viewing and Understanding JSON

Open these URLs in a new browser tab to see real JSON:

- `https://dummyjson.com/recipes/1` — a single recipe object
- `https://dummyjson.com/recipes` — an object with a `recipes` array
- `https://dummyjson.com/recipes/search?q=pizza` — a filtered object with a `recipes` array

Use the browser's JSON viewer (Firefox and Chrome format it automatically) to expand and collapse objects and arrays. Look at the structure before you write your JavaScript — check whether you need `data.name` (single object) or `data.recipes[i].name` (list).

### Converting Between JSON and JavaScript

JavaScript has two helpers for manual conversion (detailed on the next page):

- `JSON.parse(jsonString)` — JSON text → JavaScript value
- `JSON.stringify(value)` — JavaScript value → JSON text

You **don’t need these for the fetch activities** — `response.json()` already does the parsing. You need them when you handle JSON yourself, e.g. saving to `localStorage` (an optional extension covered in `03`).

> Next: [03 — Using JSON.parse() and JSON.stringify() →](03-using-json-parse-and-stringify.md) — or skip directly to `04` if you want to start fetching first and return to `03` later.

---

## Key Takeaways

- **JSON** is a strict text format for data, using objects `{ }`, arrays `[ ]`, strings, numbers, booleans, and null.
- Keys and string values in JSON must use **double quotes**.
- An API sends JSON **text**; `response.json()` **parses** that text into a JavaScript object or array.
- The DummyJSON recipes endpoint returns a single object for `/recipes/1` and an object with a `recipes` array for `/recipes` and `/recipes/search?q=...`.
- After parsing, you access data with normal JavaScript property access: `recipe.name`, `recipe.ingredients[0]`, `data.recipes.length`.

---

**Previous:** [01 — What is an API and fetch? ←](01-what-is-an-api-and-fetch.md)

**Next:** [03 — Using JSON.parse() and JSON.stringify() →](03-using-json-parse-and-stringify.md)
