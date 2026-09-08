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
                <main className='flex flex-col items-center align-middle'>
                    <div className='flex flex-col items-center p-10 m-30 rounded-bl-4xl rounded-tr-4xl bg-gray-900 border-4 border-red-800'>
                        <p className='text-4xl m-10'>Country not found.</p>
                        <Link href="/" className='text-center bg-amber-900 p-4 rounded-2xl w-60'>← Back to all countries</Link>
                    </div>
                </main>
            )
        }

        const gdp = await getGdp(countryId)
        const population = await getPopulation(countryId)
        const exports = await getExports(countryId)
        const industries = await getIndustries(countryId)

        return (
            <main className='p-10 flex items-center align-center justify-around'>
                <Link href="/" className='text-center mb-5 bg-amber-900 p-4 rounded-2xl w-60'>← Back to all countries</Link>
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
