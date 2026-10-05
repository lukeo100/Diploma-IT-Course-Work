import Link from "next/link";
import type { BookingWithDetails } from "@/lib/types";

// One booking in a list. No hooks, so this stays a Server Component and can be used
// inside the Client Component pages.
// showCourt / showMember let a detail page hide the link back to itself.
export default function BookingItem({
  booking,
  showCourt = true,
  showMember = true,
}: {
  booking: BookingWithDetails;
  showCourt?: boolean;
  showMember?: boolean;
}) {
  return (
    <li className="p-4 pt-8 pb-8 bg-gray-900 rounded-2xl transition hover:bg-gray-800">
      <p className="font-bold text-xl">
        {booking.booking_date} | {booking.start_time.slice(0, 5)} to{" "}
        {booking.end_time.slice(0, 5)} | {booking.session_type}
      </p>
      <p>
        {showCourt && (
          <>
            <Link href={`/courts/${booking.court_number}`}>
              Court {booking.court_number}
            </Link>{" "}
            ({booking.courts.surface}) |{" "}
          </>
        )}
        Hirer:{" "}
        {showMember && booking.member_id ? (
          <Link href={`/members/${booking.member_id}`}>{booking.hirer_name}</Link>
        ) : (
          booking.hirer_name
        )}{" "}
        ({booking.hirer_type}) | Charged: {Number(booking.amount_charged).toFixed(2)}
      </p>
    </li>
  );
}
