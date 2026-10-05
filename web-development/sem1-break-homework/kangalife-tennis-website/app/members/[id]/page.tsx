"use client";
import { getMember, getBookingsForMember } from "@/lib/api";
import type { BookingWithDetails, Member } from "@/lib/types";
import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import BookingItem from "@/components/BookingItem";

// MEMBER DETAIL: a DYNAMIC ROUTE. The [id] here is a member_id such as M001.

export default function MemberDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [member, setMember] = useState<Member | null>(null)
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
        const [memberResult, bookingsResult] = await Promise.all([
          getMember(String(id)),
          getBookingsForMember(String(id)),
        ])
        if (!isCancelled) {
          setMember(memberResult)
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
  if (!member) return <p>No data found.</p>
  return (
    <main>
      <h1>{member.name}</h1>
      <ul>
        <li>Member ID: {member.member_id}</li>
        <li>Date of birth: {member.date_of_birth}</li>
        <li>Member level: {member.member_level}</li>
      </ul>
      <h2>Bookings by this member</h2>
      {bookings.length === 0 ? (
        <p>No bookings for this member.</p>
      ) : (
        <ul>
          {bookings.map((booking) => (
            <BookingItem
              key={booking.booking_id}
              booking={booking}
              showMember={false}
            />
          ))}
        </ul>
      )}
    </main>
  );
}
