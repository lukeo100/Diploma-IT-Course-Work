# Part 2 — Create typed fetch functions for Supabase

### 2.1 Add your keys

Create a file named `.env.local` in the **root** of the project:

```bash
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

> Replace the values with the ones you copied in Part 0.3.
> Do **not** put quotes around the values.

### 2.2 Create the API module

Supabase's PostgREST endpoint always needs two headers: `apikey` and `Authorization`.

We will put **all data fetching in one file** (`lib/api.ts`) as small, typed functions. Pages and components then just import and call those functions — they never write a query themselves.

Create a new folder and file: `lib/api.ts`

<details>
<summary><code>lib/api.ts</code> — click to expand</summary>

```ts
// lib/api.ts

// The `!` tells TypeScript: "trust me, this value exists."
// These values come from your .env.local file.
const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!
const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

// ---------- Types for the data we get back from Supabase ----------

export type Region = {
  id: number
  name: string
}

// The data we need for each country in the list on the home page.
export type CountrySummary = {
  id: number
  name: string
  iso3: string
  regions: Region | null
}

// The full data we need on a country's detail page.
export type CountryDetail = {
  id: number
  name: string
  iso3: string
  surface_area_sq_km_2023: number | null
  regions: Region | null
}

export type GdpRow = {
  year: number
  gdp_usd_billion: number
}

export type PopulationRow = {
  year: number
  population: number
}

// ---------- Shared helper ----------
// This is the only place that uses fetch directly.
// T is the type of the JSON we expect back.
async function fetchFromSupabase<T>(path: string): Promise<T> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    headers: {
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
    },
  })

  if (!res.ok) {
    throw new Error(`Supabase request failed with status ${res.status}`)
  }

  return res.json() as Promise<T>
}

// ---------- One typed function for each kind of data ----------

export async function getCountries(): Promise<CountrySummary[]> {
  return fetchFromSupabase<CountrySummary[]>(
    'countries?select=id,name,iso3,regions(name)&order=name.asc'
  )
}

export async function getCountry(id: number): Promise<CountryDetail | null> {
  const list = await fetchFromSupabase<CountryDetail[]>(
    `countries?id=eq.${id}&select=id,name,iso3,surface_area_sq_km_2023,regions(name)`
  )

  // PostgREST returns an array. Return the first item, or null if empty.
  if (list.length === 0) {
    return null
  }
  return list[0]
}

export async function getGdp(countryId: number): Promise<GdpRow[]> {
  return fetchFromSupabase<GdpRow[]>(
    `gdp?country_id=eq.${countryId}&select=year,gdp_usd_billion&order=year.asc`
  )
}

export async function getPopulation(countryId: number): Promise<PopulationRow[]> {
  return fetchFromSupabase<PopulationRow[]>(
    `population?country_id=eq.${countryId}&select=year,population&order=year.asc`
  )
}

export async function getExports(countryId: number): Promise<string[]> {
  const rows = await fetchFromSupabase<{ exports: { name: string } }[]>(
    `country_exports?country_id=eq.${countryId}&select=exports(name)`
  )
  return rows.map((row) => row.exports.name)
}

export async function getIndustries(countryId: number): Promise<string[]> {
  const rows = await fetchFromSupabase<{ industries: { name: string } }[]>(
    `country_industries?country_id=eq.${countryId}&select=industries(name)`
  )
  return rows.map((row) => row.industries.name)
}
```

</details>

**What this does:**

- Defines TypeScript types for the data (so everything is type-safe).
- Has one small private helper (`fetchFromSupabase`) that adds the required headers.
- Exports one function per data type: `getCountries`, `getCountry`, `getGdp`, `getPopulation`, `getExports`, `getIndustries`.

> After creating or editing `.env.local`, restart the dev server (`Ctrl+C` then `npm run dev`).

---

[← Part 1](./02-part-1-nextjs-app.md) | [Back to index](./README.md) | [Next: Part 3 — Home page →](./04-part-3-home-page.md)
