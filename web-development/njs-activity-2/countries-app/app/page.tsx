// app/page.tsx
import { getCountries } from '@/lib/api'
import type { CountrySummary } from '@/lib/api'
import CountryCard from '@/components/CountryCard'

export default async function HomePage() {
  let countries: CountrySummary[] = []

  try {
    countries = await getCountries()
  } catch (e) {
    return (
      <p>
        Could not load countries. Check your Supabase setup.{' '}
        {e instanceof Error ? e.message : String(e)}
      </p>
    )
  }

  return (
    <main>
      <div className='flex font-sans justify-center items-center flex-col mt-5'>
        <span className='text-3xl'>Countries</span>
        <span className='text-lg text-gray-700 italic'>By Luca</span>
      </div>
      <ul className="flex justify-center align-middle p-5">
        {countries.map((country) => (
          <CountryCard key={country.id} country={country} />
        ))}
      </ul>
    </main>
  )
}
