# Part 3 — Home page: list all countries

### 3.1 Replace the home page

Open `app/page.tsx` and replace everything with:

<details>
<summary><code>app/page.tsx</code> — click to expand</summary>

```tsx
// app/page.tsx
import { getCountries } from '@/lib/api'
import type { CountrySummary } from '@/lib/api'
import CountryCard from '@/components/CountryCard'

export default async function HomePage() {
  let countries: CountrySummary[] = []

  try {
    countries = await getCountries()
  } catch {
    return <p>Could not load countries. Check your Supabase setup.</p>
  }

  return (
    <main>
      <h1>Countries</h1>
      <ul>
        {countries.map((country) => (
          <CountryCard key={country.id} country={country} />
        ))}
      </ul>
    </main>
  )
}
```

</details>

**What this does:** calls the `getCountries()` function and renders a `<CountryCard />` for each country.

### 3.2 Create the CountryCard component

Create a new file: `components/CountryCard.tsx`

<details>
<summary><code>components/CountryCard.tsx</code> — click to expand</summary>

```tsx
// components/CountryCard.tsx
import Link from 'next/link'
import type { CountrySummary } from '@/lib/api'

type Props = {
  country: CountrySummary
}

export default function CountryCard({ country }: Props) {
  return (
    <li>
      <Link href={`/countries/${country.id}`}>
        <h2>{country.name}</h2>
        <p>
          {country.iso3} — {country.regions?.name}
        </p>
      </Link>
    </li>
  )
}
```

</details>

**What this does:** displays one country and links to its detail page using its `id`.

---

[← Part 2](./03-part-2-api-module.md) | [Back to index](./README.md) | [Next: Part 4 — Dynamic route →](./05-part-4-dynamic-route.md)
