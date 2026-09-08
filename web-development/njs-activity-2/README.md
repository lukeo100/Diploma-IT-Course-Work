# Activity: Countries Explorer — Next.js + Supabase PostgREST (TypeScript + `fetch`)

> Split into separate files by part. Start here, then follow the parts in order.

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

## What you already need to know

- How to create **static routes** (`app/page.tsx`, `app/about/page.tsx`, etc.).
- How to create **components** and use them.
- Basic TypeScript (typing props and function return values).

This activity uses **Server Components** (pages that use `async`/`await`). We do **not** need `useEffect` or `useState` — the pages fetch data on the server and render it directly.

---

## Contents

| File | Description |
|------|-------------|
| [00. Overview](./00-overview.md) | What you will build + prerequisites (this page summarized) |
| [01. Part 0 — Set up Supabase](./01-part-0-supabase-setup.md) | Create project, import `database.sql`, get API keys |
| [02. Part 1 — Create the Next.js app](./02-part-1-nextjs-app.md) | `create-next-app`, prompts, run dev server |
| [03. Part 2 — Typed fetch functions](./03-part-2-api-module.md) | `.env.local` + `lib/api.ts` with all fetch helpers |
| [04. Part 3 — Home page](./04-part-3-home-page.md) | `app/page.tsx` + `CountryCard` component |
| [05. Part 4 — Dynamic route](./05-part-4-dynamic-route.md) | `app/countries/[id]/page.tsx` + `CountryDetails` |
| [06. Part 5 — Loading state & Run it](./06-part-5-loading-and-run.md) | `loading.tsx` + running the app |
| [07. Appendix — How PostgREST works](./07-appendix-postgrest.md) | How Supabase REST queries work |
| [08. Appendix — Troubleshooting](./08-appendix-troubleshooting.md) | Common errors and fixes |
| [Combined (single file)](./nextjs-supabase-activity.md) | Full activity in one file (legacy) |

> All large code blocks are behind expandable `<details>` elements (collapsed by default) — click **“click to expand”** to view.

---

## How to use

1. Start with **Part 0** and go in order through **Part 5**.
2. Use the **Appendix** pages if you get stuck or want to understand PostgREST.

Next: [Part 0 — Set up Supabase](./01-part-0-supabase-setup.md) →
