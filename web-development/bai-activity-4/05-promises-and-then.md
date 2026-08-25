# 05 — Promises and `.then()`

## What is a Promise?

A **Promise** is a JavaScript object that represents the **eventual result** of an asynchronous operation.

When you call `fetch()`, the browser starts a network request but does not have the result yet. Instead of returning the data directly, `fetch()` returns a Promise that will **resolve** with the `Response` when it arrives, or **reject** only if the network itself fails (no internet, DNS failure).

Similarly, `response.json()` returns a Promise that will resolve with the parsed JavaScript object once the response body has been read and parsed.

A Promise has three states:

| State | Meaning |
|-------|---------|
| **Pending** | The asynchronous operation is still in progress |
| **Fulfilled** | The operation completed successfully — the Promise now holds the result |
| **Rejected** | The operation failed at the network level (no internet, DNS failure) — the Promise holds an error. HTTP errors like `404` do **not** reject; they fulfil with `ok === false` |

You do not poll or check the state manually. Instead, you specify what should happen when a Promise fulfils by attaching a callback with **`.then()`**.

---

## What Does `.then()` Do?

`.then()` is a method available on every Promise. It accepts a **callback function** and registers it to be called when the Promise fulfils. When that happens, the fulfilment value is passed as an argument to your callback.

```js
function onResponseReady(response) {
    console.log('Promise fulfilled — response is available');
    console.log(response);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

Step by step:

1. `fetch('https://dummyjson.com/recipes/1')` — sends the HTTP request and returns a Promise in the pending state.
2. `.then(onResponseReady)` — registers `onResponseReady` as the handler for when that Promise fulfils.
3. The browser waits for the network. Your other code continues to run.
4. When the server responds, the Promise fulfils with a `Response` object.
5. The JavaScript engine calls `onResponseReady(response)` and passes that `Response` object in.

The `response` parameter contains the HTTP response — including the status code and headers. To get the body as a usable JavaScript object, you call `response.json()`.

---

## Chaining `.then()` — Two Steps to Get JSON

`fetch()` fulfils with a **Response object**, not the parsed data. The Response holds the raw JSON text. The method `response.json()` parses that text and returns a **new Promise** that fulfils with the resulting object.

Because two asynchronous steps are involved, you need two `.then()` calls:

```js
function onRecipeReady(recipe) {
    // This is the fully parsed JavaScript object
    console.log(recipe.name); // "Classic Margherita Pizza"
    console.log(recipe.ingredients);
}

function onResponseReady(response) {
    // response.json() returns a new Promise
    // Attach the next callback to that Promise
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

Chain of events:

```
fetch(url)  ──Promise 1──▶  onResponseReady(response)
                                │
                                ▼
                         response.json()  ──Promise 2──▶  onRecipeReady(recipe)
                                                              │
                                                              ▼
                                                         Use the data
```

Both Promises work the same way: `.then()` registers a function to run when the async work for that step is complete. The first step handles the network; the second handles parsing.

---

## What About Errors?

Two kinds of failure can happen:

1. **Network failure** (no internet, DNS failure) — the `fetch()` Promise **rejects**. You can handle this with `.catch()`.
2. **HTTP error** (wrong URL or missing resource, e  `404 Not Found`) — the `fetch()` Promise still **fulfils**, but the `Response` has `ok === false` and a `status` like `404`.

You can check this with DummyJSON (optional — not needed for activities):

```js
function onDataReady(data) {
    console.log(data); // { message: "Recipe with id '999' not found" }
}

function onResponseReady(response) {
    console.log(response.status); // 404
    console.log(response.ok);     // false — not the success path
    response.json().then(onDataReady);
}

fetch('https://dummyjson.com/recipes/999').then(onResponseReady);
```

For the activities, just focus on the success path (`200`, `ok === true`). If nothing appears, open Developer Tools → **Console** and **Network** to check the `status`. Always double-check the URL.

---

## You Do NOT Need `async` / `await` Here

You may see an alternative syntax online that uses `async` and `await`:

```js
// ❌ Not used in these activities
async function getRecipe() {
    const response = await fetch('https://dummyjson.com/recipes/1');
    const recipe = await response.json();
    console.log(recipe);
}
```

`async`/`await` is another way to wait for Promises using different keywords instead of `.then()`. It does not change how `fetch` or Promises work — just a different writing style.

In these activities we **only** use `.then()` with named callback functions so the Promise chain is visible and each step has an explicit name.

> **Rule for these activities:** No `async`, no `await`, no arrow functions. Only `function` declarations and `.then()`.

---

## Key Takeaways

- A **Promise** is an object that represents the future result of an asynchronous operation. It starts pending and then becomes fulfilled or rejected.
- **`.then(callback)`** registers `callback` to be called when the Promise fulfils, receiving the result as its argument.
- `fetch()` requires **two** `.then()` steps: one for the `Response` from the network, and one for the parsed object from `response.json()`.
- Pass the function **by name** without calling it: `.then(onResponseReady)` not `.then(onResponseReady())`.

---

**Previous:** [04 — Callback Functions ←](04-callback-functions.md)

**Next:** [06 — Fetch with .then() Step by Step →](06-fetch-with-then-step-by-step.md)
