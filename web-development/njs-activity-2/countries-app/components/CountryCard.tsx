// components/CountryCard.tsx
import Link from 'next/link'
import type { CountrySummary } from '@/lib/api'

type Props = {
  country: CountrySummary
}

export default function CountryCard({ country }: Props) {
  return (
    <li className="p-5 m-3 bg-emerald-900 rounded-2xl w-full flex align-middle justify-center transition hover:bg-emerald-950">
      <Link href={`/countries/${country.id}`}>
        <h2>{country.name}</h2>
        <p>
          {country.iso3} — {country.regions?.name}
        </p>
      </Link>
    </li>
  )
}
