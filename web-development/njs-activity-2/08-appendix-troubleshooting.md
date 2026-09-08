# Appendix — Troubleshooting

**Error: `SUPABASE_URL` is `undefined`**
Check that `.env.local` exists, has no quotes around the values, and restart the dev server.

**Page shows "Could not load countries."**
Make sure your Project URL and anon key are correct, and that `database.sql` was imported into Supabase (Part 0.2).

**`Supabase request failed with status 404`**
The table name or query option in the URL is probably misspelled.

**Page says "Country not found."**
Check that the `countries` table has data (imported `database.sql`).

**TypeScript error: `params` is not a Promise / wrong type**
You are on Next.js 14. Change the props type to `{ params: { id: string } }` and use `const { id } = params` (no `await`).

---

[← How PostgREST works](./07-appendix-postgrest.md) | [Back to index](./README.md)
