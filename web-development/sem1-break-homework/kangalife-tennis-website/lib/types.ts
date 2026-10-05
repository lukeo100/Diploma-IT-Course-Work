// Shapes of the rows in each Supabase table (matches schema.sql).
// JSON from Supabase gives numeric columns as numbers, and date/time columns as strings.

export type Court = {
  court_number: number;
  surface: string;
  day_hire_price: number;
  night_hire_price: number;
};

export type Member = {
  member_id: string;
  name: string;
  date_of_birth: string; // "yyyy-mm-dd"
  member_level: string;
};

export type Booking = {
  booking_id: string;
  booking_date: string; // "yyyy-mm-dd"
  start_time: string; // "HH:MM:SS"
  end_time: string; // "HH:MM:SS"
  court_number: number;
  session_type: string; // "day" or "night"
  hirer_type: string; // "member" or "non-member"
  member_id: string | null; // null for non-member bookings
  amount_charged: number;
  hirer_name: string;
};

// A booking as returned with its joined rows (see BOOKING_SELECT in lib/api.ts).
// courts is always present because every booking has a court.
// members is null for non-member bookings because member_id is null.
export type BookingWithDetails = Booking & {
  courts: Pick<Court, "court_number" | "surface">;
  members: Pick<Member, "member_id" | "name"> | null;
};
