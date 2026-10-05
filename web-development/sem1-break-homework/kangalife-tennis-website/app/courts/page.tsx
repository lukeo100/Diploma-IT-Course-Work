"use client";
import type { Court } from "@/lib/types";
import { useState, useEffect } from "react";
import { getCourts } from "@/lib/api";
import Link from "next/link";

// COURTS LIST: every court, each linking to its own page at /courts/[court_number].

export default function CourtsPage() {
  const [courts, setCourts] = useState<Court[]>([]);
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isCancelled = false

    async function loadData() {
      setLoading(true)
      setError(null)
      try {
        const result = await getCourts()
        if (!isCancelled) {
          setCourts(result)
        }
      } catch (err: unknown) {
        if (!isCancelled) {
          setError(err instanceof Error ? err.message : 'Something went wrong')
        }
      } finally {
        if (!isCancelled) {
          setLoading(false)
        }
      }
    }

    loadData()

    // Cleanup function prevents setting state on unmounted component
    return () => {
      isCancelled = true
    }
  }, [])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>
  if (!courts.length) return <p>No data found.</p>

  return (
    <main>
      <h1>Courts</h1>
      <ul>
        {courts.map((court) => (
          <li key={court.court_number}>
            <Link href={`/courts/${court.court_number}`}>
              Court Number {court.court_number} | {court.surface}
            </Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
