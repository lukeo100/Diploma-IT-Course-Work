# 01 - What is an API and What Does `fetch()` Do?

## What is an API?

**API** stands for **Application Programming Interface**. In web development, an API is a URL that a server makes available so other programs can request data from it.

For example, the **DummyJSON Recipes API** is a server that stores recipe data. It exposes specific URLs (called **endpoints**) that you can request. When you request one, the server responds with data in **JSON** format — a text format for structured data that JavaScript can parse into objects and arrays.

You don't need an account or API key for DummyJSON. You can test it directly in your browser address bar:

| URL (endpoint) | What the server returns |
|-----|--------------|
| `https://dummyjson.com/recipes/1` | One recipe object (id 1) |
| `https://dummyjson.com/recipes` | An object containing an array of 30 recipes |
| `https://dummyjson.com/recipes/search?q=pizza` | An object containing recipes that match "pizza" |

A single recipe object looks like this:

```json
{
  "id": 1,
  "name": "Classic Margherita Pizza",
  "ingredients": ["Pizza dough", "Tomato sauce", "Fresh mozzarella cheese"],
  "instructions": ["Preheat the oven to 475°F...", "Roll out the pizza dough..."],
  "prepTimeMinutes": 20,
  "cookTimeMinutes": 15,
  "cuisine": "Italian",
  "difficulty": "Easy",
  "image": "https://cdn.dummyjson.com/recipe-images/1.webp",
  "rating": 4.6,
  "mealType": ["Dinner"]
}
```

Your code will **request** this data from the API and then **display it on the page**.

---

## What is `fetch()` ?

`fetch()` is a built-in browser function that **sends an HTTP request to a URL and returns the server's response**.

```js
fetch('https://dummyjson.com/recipes/1')
```

That line tells the browser to send a `GET` request to that URL and retrieve the data.

However, network requests take time. The browser has to:

1. Send the request over the network
2. Wait for the server to process it
3. Download the response

JavaScript does **not** pause while waiting. It continues executing the next lines of code and handles the response later, when it arrives. This is called **asynchronous** execution — the response is handled at a later time, not immediately.

To handle data that arrives later, you provide a function that the browser will call once the response is ready. You attach that function with **`.then()`**.

You will learn how that works in `02` (JSON) and `03` (parse/stringify), then `04` (callbacks) and `05` (Promises). For now, just remember: `fetch()` is **asynchronous** — the result comes later.

---

## What `fetch()` Returns

`fetch()` does **not** return the recipe data directly. It returns a **Promise** — think of it as a receipt that says “your request is in progress, I’ll give you the result when it’s ready”. You will learn exactly how a Promise works in `05 — Promises and .then()`.

For now, know that you **cannot** use the return value of `fetch()` as if it were the data:

```js
// ❌ This will NOT work — recipe is a Promise, not the actual data
const recipe = fetch('https://dummyjson.com/recipes/1');
console.log(recipe.name); // undefined — recipe is a Promise, not a recipe
```

Instead, you tell `fetch()` what to do **later**, when the response arrives, by attaching a function with `.then()`:

```js
// ✅ This works — we tell fetch what to do WHEN the response arrives
function onResponseReady(response) {
    console.log('Data has arrived');
    console.log(response);
}

fetch('https://dummyjson.com/recipes/1').then(onResponseReady);
```

`onResponseReady` is not called immediately. It is called **later**, after the server has responded. The `response` parameter is the server’s reply (a `Response` object). How to turn that into usable recipe data is covered in `06 — Fetch with .then() Step by Step`.

---

## Key Takeaways

- An **API endpoint** is a URL that a server provides for requesting data. The server responds with JSON.
- `fetch(url)` **sends an HTTP request**. It is **asynchronous** — it does not block the rest of your code from running.
- `fetch()` returns a **Promise**, not the data itself.
- You handle the result by passing a **callback function** to `.then()`.

---

**Next:** [02 — What is JSON? →](02-what-is-json.md)
