# Fetching Activities — DummyJSON Recipes

JavaScript activities and reading material on how to fetch data from an API using `fetch()` and callback functions with `.then()`.

You will use the **DummyJSON Recipes API**:

- All recipes: `https://dummyjson.com/recipes`
- Single recipe: `https://dummyjson.com/recipes/1` (replace `1` with any id `1`-`50`)
- Search recipes: `https://dummyjson.com/recipes/search?q=pizza`

You can test any URL in your browser to see the JSON it returns.

---

## Reading Material — Read This First

Complete these short readings **before** starting the activities. They explain `fetch()`, callback functions, and `.then()` with the same DummyJSON recipes API you will use.

| Order | Topic | What you will learn |
|-------|-------|---------------------|
| [01 — What is an API and fetch?](01-what-is-an-api-and-fetch.md) | APIs + `fetch()` | What an API is, why `fetch` is asynchronous, what a Promise is |
| [02 — What is JSON?](02-what-is-json.md) | JSON | What JSON is, its syntax rules, and how `response.json()` parses it |
| [03 — Using JSON.parse() and JSON.stringify()](03-using-json-parse-and-stringify.md) | JSON conversion | How to convert between JSON text and JavaScript objects, `localStorage`, and common mistakes |
| [04 — Callback Functions](04-callback-functions.md) | Callbacks | How to write named callback functions and pass them to `.then()` |
| [05 — Promises and .then()](05-promises-and-then.md) | Promises | How `.then()` waits for a Promise to finish and why we need two steps |
| [06 — Fetch with .then() Step by Step](06-fetch-with-then-step-by-step.md) | Putting it together | The exact 2-callback pattern used in every activity |
| [07 — Displaying Data on the Page](07-displaying-data-on-the-page.md) | `getElementById` | How to update the page with `.innerText`, `.innerHTML`, `.src` |
| [08 — Cheat Sheet](08-cheat-sheet.md) | Quick reference | Copy-paste pattern, API URLs, debugging checklist |

> **Tip:** Keep the [Cheat Sheet](08-cheat-sheet.md) open in a second tab while you work through the activities.

---

## Activities

### [Activity 1: Fetch and Display a Single Recipe](activity-1/)

Fetch one recipe and display its details on the page.

**You will learn:**
- How to call `fetch()` with a URL
- How to handle the response with `.then()` and a callback function
- How to convert the response to JSON with `response.json()`
- How to populate the page with `getElementById` and `.innerText` / `.src`

---

### [Activity 2: Fetch and Display All Recipes](activity-2/)

Fetch the full list of recipes and display them as cards.

**You will learn:**
- How to fetch a list (`/recipes` returns an object with a `recipes` array)
- How to loop through an array with a `for` loop
- How to build HTML with string concatenation and set it with `.innerHTML`
- How to chain two `.then()` callbacks together

---

### [Activity 3: Search Recipes on Button Click](activity-3/)

Add a search box and button. When the user clicks search, fetch matching recipes and display the results.

**You will learn:**
- How to read user input with `.value`
- How to trigger a `fetch()` from an event handler
- How to build a query URL with user input
- How to handle empty results and update the page

---

## Getting Started

1. Fork this repository
2. Clone your forked repository to your computer
3. Open the activity folder you want to complete (e.g. `activity-1/`)
4. Read the instructions in the markdown file (`activity-1.md`)
5. Open `script.js` and follow the `TODO` steps — the file contains starter comments
6. Open `index.html` via **Live Server** or **Live Preview**
7. Open Developer Tools (F12) → Console to see logs/errors and **Network → Preview** to inspect the JSON.
8. Check `sample/script.js` only if you are stuck — try to complete the `TODO`s first.

## Samples

Each activity has a `sample/script.js` with the completed solution. Use it to check your work after (or if you get stuck).

- `activity-1/sample/script.js`
- `activity-2/sample/script.js`
- `activity-3/sample/script.js`
