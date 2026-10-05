"use client";
import type { BookingWithDetails } from "@/lib/types";
import { useState, useEffect } from "react";
import { getBookings } from "@/lib/api";
import BookingItem from "@/components/BookingItem";

// HOME PAGE: every booking in a schedule list, newest booking_date first.

export default function HomePage() {
  const [bookings, setBookings] = useState<BookingWithDetails[]>([]);
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isCancelled = false

    async function loadData() {
      setLoading(true)
      setError(null)
      try {
        const result = await getBookings()
        if (!isCancelled) {
          setBookings(result)
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
  if (!bookings.length) return <p>No data found.</p>

  return (
    <main>
      <h1 className="p-5">All bookings</h1>
      <ul className="grid grid-cols-2 gap-4">
        {bookings.map((booking) => (
          <BookingItem key={booking.booking_id} booking={booking} />
        ))}
      </ul>
    </main>
  );
}
