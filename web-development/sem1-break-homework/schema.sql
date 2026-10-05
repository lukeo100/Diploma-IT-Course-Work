CREATE TABLE courts (
    court_number int PRIMARY KEY,
    surface text NOT NULL,
    day_hire_price numeric(8,2) NOT NULL,
    night_hire_price numeric(8,2) NOT NULL
);

CREATE TABLE members (
    member_id text PRIMARY KEY,
    name text NOT NULL,
    date_of_birth date NOT NULL,
    member_level text NOT NULL
);

-- bookings must be created last because it references courts and members
CREATE TABLE bookings (
    booking_id text PRIMARY KEY,
    booking_date date NOT NULL,
    start_time time NOT NULL,
    end_time time NOT NULL,
    court_number int NOT NULL REFERENCES courts (court_number),
    session_type text NOT NULL CHECK (session_type IN ('day', 'night')),
    hirer_type text NOT NULL CHECK (hirer_type IN ('member', 'non-member')),
    member_id text REFERENCES members (member_id), -- nullable: non-member bookings have no member
    amount_charged numeric(8,2) NOT NULL, -- historical record, deliberately not derived from courts
    hirer_name text NOT NULL -- name on the booking, may differ from the member's name
);
