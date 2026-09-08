# Part 4 — Dynamic route: country details

### 4.1 Create the dynamic route

Create this folder and file:

```text
app/countries/[id]/page.tsx
```

> The `[id]` part is a **dynamic segment**. Next.js turns anything in the URL at that position into a `params` value. For example `/countries/4` gives us `id = 4`.

Paste this code into it:

<details>
<summary><code>app/countries/[id]/page.tsx</code> — click to expand</summary>

```tsx
// app/countries/[id]/page.tsx
import Link from 'next/link'
import {
  getCountry,
  getGdp,
  getPopulation,
  getExports,
  getIndustries,
} from '@/lib/api'
import CountryDetails from '@/components/CountryDetails'

export default async function CountryPage({
  params,
}: {
  params: Promise<{ id: string }>
}) {
  const { id } = await params // Next.js 15: params is a Promise
  const countryId = Number(id) // the URL gives us a string; the DB column is a number

  try {
    const country = await getCountry(countryId)

    if (!country) {
      return (
        <main>
          <p>Country not found.</p>
          <Link href="/">← Back to all countries</Link>
        </main>
      )
    }

    const gdp = await getGdp(countryId)
    const population = await getPopulation(countryId)
    const exports = await getExports(countryId)
    const industries = await getIndustries(countryId)

    return (
      <main>
        <Link href="/">← Back to all countries</Link>
        <CountryDetails
          country={country}
          gdp={gdp}
          population={population}
          exports={exports}
          industries={industries}
        />
      </main>
    )
  } catch {
    return <p>Could not load this country. Check your Supabase setup.</p>
  }
}
```

</details>

**What this does:**

- Reads `id` from the URL.
- Calls the typed fetch functions to get the country, its GDP, population, exports, and industries.
- Passes everything to the `<CountryDetails />` component to display.

### 4.2 Create the CountryDetails component

Create a new file: `components/CountryDetails.tsx`

<details>
<summary><code>components/CountryDetails.tsx</code> — click to expand</summary>

```tsx
// components/CountryDetails.tsx
import type { CountryDetail, GdpRow, PopulationRow } from '@/lib/api'

type Props = {
  country: CountryDetail
  gdp: GdpRow[]
  population: PopulationRow[]
  exports: string[]
  industries: string[]
}

export default function CountryDetails({
  country,
  gdp,
  population,
  exports,
  industries,
}: Props) {
  return (
    <article>
      <h1>{country.name}</h1>
      <p>ISO code: {country.iso3}</p>
      <p>Region: {country.regions?.name}</p>
      <p>Surface area: {country.surface_area_sq_km_2023?.toLocaleString()} km²</p>

      <h2>GDP (USD billion)</h2>
      <ul>
        {gdp.map((row) => (
          <li key={row.year}>
            {row.year}: ${row.gdp_usd_billion}
          </li>
        ))}
      </ul>

      <h2>Population</h2>
      <ul>
        {population.map((row) => (
          <li key={row.year}>
            {row.year}: {row.population.toLocaleString()}
          </li>
        ))}
      </ul>

      <h2>Major exports</h2>
      <ul>
        {exports.map((name) => (
          <li key={name}>{name}</li>
        ))}
      </ul>

      <h2>Major industries</h2>
      <ul>
        {industries.map((name) => (
          <li key={name}>{name}</li>
        ))}
      </ul>
    </article>
  )
}
```

</details>

**What this does:** receives all the data as props and renders it. It contains **no data fetching** — that keeps it reusable and easy to read.

---

[← Part 3](./04-part-3-home-page.md) | [Back to index](./README.md) | [Next: Part 5 — Loading state →](./06-part-5-loading-and-run.md)
