# Part 5 — Add a loading state

When a page is a Server Component that uses `await`, Next.js can show a loading screen automatically while the data is being fetched.

Create this file next to the dynamic route:

```text
app/countries/[id]/loading.tsx
```

Paste this code into it:

<details>
<summary><code>app/countries/[id]/loading.tsx</code> — click to expand</summary>

```tsx
// app/countries/[id]/loading.tsx
export default function Loading() {
  return <p>Loading country…</p>
}
```

</details>

**What this does:** while the dynamic route is fetching its data, Next.js shows this component instead of the page. Once the data is ready, the page renders normally.

---

## Run it

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

You should see:

1. A list of countries on the home page.
2. Clicking a country takes you to `/countries/1`, `/countries/2`, etc.
3. Each detail page shows region, area, GDP, population, exports, and industries.

---

[← Part 4](./05-part-4-dynamic-route.md) | [Back to index](./README.md) | [Next: How PostgREST works →](./07-appendix-postgrest.md)
