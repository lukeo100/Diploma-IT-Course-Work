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
        <article className='w-250 rounded-bl-4xl rounded-tr-4xl border-2 border-yellow-400 bg-gray-900 p-6'>
            <h1 className='mb-5 self-center text-4xl'>{country.name}</h1>
            <div className='flex justify-between'>
                <span>ISO code</span>
                <span className="flex-1 border-b-2 border-dotted border-gray-300 mx-2 mb-1"></span>
                <span>{country.iso3}</span>
            </div>
            <div className='flex justify-between'>
                <span>Region</span>
                <span className="flex-1 border-b-2 border-dotted border-gray-300 mx-2 mb-1"></span>
                <span>{country.regions?.name}</span>
            </div>
            <div className='mb-5 flex justify-between'>
                <span>Surface area</span>
                <span className="flex-1 border-b-2 border-dotted border-gray-300 mx-2 mb-1"></span>
                <span>{country.surface_area_sq_km_2023?.toLocaleString()} km²</span>
            </div>

            <section className='mb-5'>
                <h2 className='mb-2 text-2xl'>GDP (USD billion)</h2>
                <ul className='space-y-1'>
                    {gdp.map((row) => (
                        <li className='flex justify-between' key={row.year}>
                            <span>{row.year}</span>
                            <span className="flex-1 border-b-2 border-dotted border-gray-300 mx-2 mb-1"></span>
                            <span>${row.gdp_usd_billion}</span>
                        </li>
                    ))}
                </ul>
            </section>

            <section className='mb-5'>
                <h2 className='mb-2 text-2xl'>Population</h2>
                <ul className='space-y-1'>
                    {population.map((row) => (
                        <li className='flex justify-between' key={row.year}>
                            <span>{row.year}</span>
                            <span className="flex-1 border-b-2 border-dotted border-gray-300 mx-2 mb-1"></span>
                            <span>{row.population.toLocaleString()}</span>
                        </li>
                    ))}
                </ul>
            </section>

            <section className='mb-5'>
                <h2 className='mb-2 text-2xl'>Major exports</h2>
                <ul className='list-disc space-y-1 pl-5'>
                    {exports.map((name) => (
                        <li key={name}>{name}</li>
                    ))}
                </ul>
            </section>

            <section>
                <h2 className='mb-2 text-2xl'>Major industries</h2>
                <ul className='list-disc space-y-1 pl-5'>
                    {industries.map((name) => (
                        <li key={name}>{name}</li>
                    ))}
                </ul>
            </section>
        </article>
    )
}
