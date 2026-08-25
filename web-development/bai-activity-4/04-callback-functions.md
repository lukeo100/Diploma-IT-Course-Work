# 04 — Callback Functions

## What is a Callback?

A **callback function** is a function that is **passed as an argument** to another function, so that the receiving function can **call it later** when it is ready.

This is useful for asynchronous operations like `fetch()`. You don't know exactly when the network request will finish, so you provide a function and say: "when the response arrives, call this function with the result."

```js
// 1. Define the callback — what to do when the response arrives
function onResponseReady(response) {
    console.log('The server has replied');
    console.log(response);
}

// 2. Pass the callback to .then() — do not call it yourself
fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

The key detail is how you pass the function:

- `.then(onResponseReady)` — passes a **reference** to the function. The browser will call it later when the data is ready.
- `.then(onResponseReady())` — **calls** the function immediately and passes its return value. This is incorrect for callbacks.

> Always pass the function name **without brackets** when using `.then()`.

---

## Named Functions vs Arrow Functions

In these activities we **only** use **named functions** declared with the `function` keyword:

```js
// ✅ Do this — named function
function onResponseReady(response) {
    console.log(response);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

Do **not** use arrow functions (`=>`) or anonymous functions, even though you will see them in other tutorials and documentation:

```js
// ❌ Don't do this in these activities
fetch('https://dummyjson.com/recipes/1').then(function(response) { ... });
fetch('https://dummyjson.com/recipes/1').then((response) => { ... });
fetch('https://dummyjson.com/recipes/1').then(response => console.log(response));
```

Named functions are required in these activities because they make the flow of asynchronous code explicit. Each function has a descriptive name such as `onResponseReady` or `onRecipeReady`, which makes it clear what each step does and makes debugging easier when you check the call stack in Developer Tools.

---

## Callbacks Can Be Chained

A callback that is attached with `.then()` can itself attach another callback with another `.then()`. This is necessary with `fetch()` because converting the response to JSON is also asynchronous:

```js
function onRecipeReady(recipe) {
    console.log('The recipe object is ready');
    console.log(recipe.name);
}

function onResponseReady(response) {
    // response.json() returns a Promise, so it also uses .then()
    response.json().then(onRecipeReady);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

Execution order — try adding `console.log` to see the timeline:

```js
function onRecipeReady(recipe) {
    console.log('3 — recipe ready', recipe.name);
}

function onResponseReady(response) {
    console.log('2 — response arrived');
    response.json().then(onRecipeReady);
}

console.log('1 — sending request');
fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
console.log('1 — request sent, waiting...');
// Console order: 1, 1, 2, 3 — 2 and 3 happen later
```

1. `fetch()` sends the request.
2. Your other code keeps running (`request sent, waiting...`).
3. When the server replies, `onResponseReady` is called with the `Response`.
4. `response.json()` parses the JSON, then `onRecipeReady` is called with the recipe object.

```
fetch(url)  →  wait for network  →  onResponseReady(response)
                                    → response.json()  →  wait for parsing  →  onRecipeReady(recipe)
```

---

## Common Mistakes

| Mistake | Why it's wrong | Fix |
|---------|---------------|-----|
| `.then(onResponseReady())` | The `()` calls the function **immediately**, before `fetch` completes | Remove the brackets: `.then(onResponseReady)` |
| `.then(() => { ... })` | Uses an arrow function | Create a named `function` and pass its name |
| Forgetting the parameter | The callback needs a parameter to receive the data: `function onResponseReady(response)` | Always declare the parameter — `.then()` will pass the result into it |

---

## Quick Check

```js
function handleData(data) {
    console.log(data);
}

function handleResponse(response) {
    response.json().then(handleData);
}

fetch('https://dummyjson.com/recipes/1').then(handleResponse);
```

- Q: How many callback functions are there? **A:** Two — `handleResponse` and `handleData`
- Q: When is `handleResponse` called? **A:** When the `fetch()` Promise resolves with the `Response` object
- Q: When is `handleData` called? **A:** When the `response.json()` Promise resolves with the parsed object

If that is clear, you are ready for the next page.

---

**Previous:** [03 — Using JSON.parse() and JSON.stringify() ←](03-using-json-parse-and-stringify.md)

**Next:** [05 — Promises and .then() →](05-promises-and-then.md)
