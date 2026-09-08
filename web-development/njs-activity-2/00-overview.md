# Overview

## What you will build

A small Next.js app that:

1. Shows a list of all countries (home page).
2. Lets you click a country to open a **dynamic route** (`/countries/[id]`) with its details.
3. Gets all data from Supabase using the **PostgREST API** with plain `fetch` (no extra package needed).

You will practice:

- Creating a Next.js app with the App Router (TypeScript).
- Creating reusable components.
- Creating a dynamic route.
- Writing typed **fetch functions** for each kind of data, and using them from pages.

---

## What you already need to know

- How to create **static routes** (`app/page.tsx`, `app/about/page.tsx`, etc.).
- How to create **components** and use them.
- Basic TypeScript (typing props and function return values).

This activity uses **Server Components** (pages that use `async`/`await`). We do **not** need `useEffect` or `useState` — the pages fetch data on the server and render it directly.

---

[← Back to index](./README.md) | [Next: Part 0 — Set up Supabase →](./01-part-0-supabase-setup.md)
