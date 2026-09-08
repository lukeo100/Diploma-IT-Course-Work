# Part 0 — Set up Supabase

### 0.1 Create a project

1. Go to [supabase.com](https://supabase.com) and create a free project.
2. Wait for the project to be ready.

### 0.2 Import the database

1. Open your project dashboard.
2. Click **SQL Editor** in the left menu.
3. Click **New query**.
4. Paste the contents of `database.sql` into the editor.
5. Click **Run**.

This creates the tables you will use:

| Table | What it stores | Important columns |
|---|---|---|
| `countries` | One row per country | `id`, `name`, `iso3`, `region_id`, `surface_area_sq_km_2023` |
| `regions` | World regions | `id`, `name` |
| `gdp` | GDP per country per year | `country_id`, `year`, `gdp_usd_billion` |
| `population` | Population per country per year | `country_id`, `year`, `population` |
| `exports` | Export names | `id`, `name` |
| `country_exports` | Which countries export what | `country_id`, `export_id` |
| `industries` | Industry names | `id`, `name` |
| `country_industries` | Which countries have which industries | `country_id`, `industry_id` |

### 0.3 Get your API keys

1. Click **Settings** (gear icon) → **API**.
2. Copy these two values. You need them in the next part:

- **Project URL** (example: `https://abcdefgh.supabase.co`)
- **anon public** key (a long string)

> The **anon** key is safe to use in a browser. It is designed to be public.

---

[← Overview](./00-overview.md) | [Back to index](./README.md) | [Next: Part 1 — Create the Next.js app →](./02-part-1-nextjs-app.md)
