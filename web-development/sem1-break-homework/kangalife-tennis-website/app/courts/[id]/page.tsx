"use client";
import { getCourt, getBookingsForCourt } from "@/lib/api";
import type { BookingWithDetails, Court } from "@/lib/types";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import BookingItem from "@/components/BookingItem";

// COURT DETAIL: a DYNAMIC ROUTE. The [id] folder name is the variable part of the URL,
// so /courts/3 and /courts/12 both render this one file.

export default function CourtDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [court, setCourt] = useState<Court | null>(null)
  const [bookings, setBookings] = useState<BookingWithDetails[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let isCancelled = false

    async function loadData() {
      setLoading(true)
      setError(null)
      try {
        // Both requests use the id from the URL, and run at the same time.
        const [courtResult, bookingsResult] = await Promise.all([
          getCourt(String(id)),
          getBookingsForCourt(String(id)),
        ])
        if (!isCancelled) {
          setCourt(courtResult)
          setBookings(bookingsResult)
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
  }, [id])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}</p>
  if (!court) return <p>No data found.</p>
  return (
    <main>
      <h1>Court {court.court_number}</h1>
      <ul>
        <li>Surface: {court.surface}</li>
        <li>Day hire price: {court.day_hire_price}</li>
        <li>Night hire price: {court.night_hire_price}</li>
      </ul>
      <h2>Bookings for this court</h2>
      {bookings.length === 0 ? (
        <p>No bookings for this court.</p>
      ) : (
        <ul>
          {bookings.map((booking) => (
            <BookingItem
              key={booking.booking_id}
              booking={booking}
              showCourt={false}
            />
          ))}
        </ul>
      )}
    </main>
  );
}
