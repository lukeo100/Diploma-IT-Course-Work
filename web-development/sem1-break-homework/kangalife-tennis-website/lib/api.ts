import type { BookingWithDetails, Court, Member } from "./types";

// Both values come from .env.local. Restart `npm run dev` after changing that file.
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
export const SUPABASE_PUBLISHABLE_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;

// ---------- Shared helper ----------
// This is the only place that uses fetch directly.
// T is the type of the JSON we expect back.
async function fetchFromSupabase<T>(path: string): Promise<T> {
  // Fail early with a clear message instead of sending "undefined" as the key.
  // The check also narrows both values from string | undefined to string.
  if (!SUPABASE_URL || !SUPABASE_PUBLISHABLE_KEY) {
    throw new Error(
      "Missing Supabase environment variables. Check .env.local and restart npm run dev.",
    );
  }

  const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    headers: {
      // New-style publishable keys (sb_publishable_...) go in the apikey header only.
      // Do not also send them as Authorization: Bearer, because that header expects a JWT.
      apikey: SUPABASE_PUBLISHABLE_KEY,
    },
  });

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(
      `Supabase request failed with status ${res.status} ${res.statusText}${
        errorBody ? ` - ${errorBody}` : ""
      }`,
    );
  }

  return res.json() as Promise<T>;
}

// These are plain fetch calls to the Supabase REST API.

const COURT_COLUMNS = "court_number,surface,day_hire_price,night_hire_price";
const MEMBER_COLUMNS = "member_id,name,date_of_birth,member_level";

// Bookings come back with their court and member joined in, in one request.
// courts(...) and members(...) work because bookings has foreign keys to those tables:
// Supabase follows the foreign key and nests the matching row inside each booking.
// A non-member booking has member_id null, so its "members" value comes back as null.
const BOOKING_SELECT =
  "booking_id,booking_date,start_time,end_time,court_number,session_type,hirer_type,member_id,amount_charged,hirer_name," +
  "courts(court_number,surface),members(member_id,name)";

// Newest booking_date first, then latest start time first within a day.
const BOOKING_ORDER = "order=booking_date.desc,start_time.desc";

export async function getBookings(): Promise<BookingWithDetails[]> {
  return fetchFromSupabase<BookingWithDetails[]>(
    `bookings?select=${BOOKING_SELECT}&${BOOKING_ORDER}`,
  );
}

export async function getCourts(): Promise<Court[]> {
  return fetchFromSupabase<Court[]>(
    `courts?select=${COURT_COLUMNS}&order=court_number.asc`,
  );
}

export async function getCourt(courtNumber: string): Promise<Court | null> {
  // court_number is an integer column, so anything that is not digits cannot match a court.
  // Returning null here avoids a Supabase 400 error for URLs like /courts/abc.
  if (!/^\d+$/.test(courtNumber)) return null;

  // Filters are written column=eq.value. Supabase always returns an array,
  // so take the first row, or null if the array is empty.
  const rows = await fetchFromSupabase<Court[]>(
    `courts?select=${COURT_COLUMNS}&court_number=eq.${courtNumber}`,
  );
  return rows[0] ?? null;
}

export async function getMembers(): Promise<Member[]> {
  return fetchFromSupabase<Member[]>(
    `members?select=${MEMBER_COLUMNS}&order=name.asc`,
  );
}

export async function getMember(memberId: string): Promise<Member | null> {
  // member_id is text (for example M001), so encode it before putting it in the URL.
  const rows = await fetchFromSupabase<Member[]>(
    `members?select=${MEMBER_COLUMNS}&member_id=eq.${encodeURIComponent(memberId)}`,
  );
  return rows[0] ?? null;
}

export async function getBookingsForCourt(
  courtNumber: string,
): Promise<BookingWithDetails[]> {
  if (!/^\d+$/.test(courtNumber)) return [];
  return fetchFromSupabase<BookingWithDetails[]>(
    `bookings?select=${BOOKING_SELECT}&court_number=eq.${courtNumber}&${BOOKING_ORDER}`,
  );
}

export async function getBookingsForMember(
  memberId: string,
): Promise<BookingWithDetails[]> {
  return fetchFromSupabase<BookingWithDetails[]>(
    `bookings?select=${BOOKING_SELECT}&member_id=eq.${encodeURIComponent(memberId)}&${BOOKING_ORDER}`,
  );
}
