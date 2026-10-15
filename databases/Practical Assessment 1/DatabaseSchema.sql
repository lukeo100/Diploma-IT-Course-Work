CREATE TABLE IF NOT EXISTS distribution_centres (
	distribution_centre_id TEXT NOT NULL,
	distribution_centre_name TEXT NOT NULL,
	distribution_centre_suburb TEXT NOT NULL,
	distribution_centre_postcode INTEGER NOT NULL,
	distribution_centre_phone TEXT NOT NULL,
	PRIMARY KEY(distribution_centre_id)
);

CREATE TABLE IF NOT EXISTS clients (
	client_id TEXT NOT NULL,
	client_name TEXT NOT NULL,
	client_type TEXT NOT NULL,
	client_suburb TEXT NOT NULL,
	client_postcode INTEGER NOT NULL,
	client_phone TEXT NOT NULL,
	client_email TEXT NOT NULL,
	PRIMARY KEY(client_id)
);


CREATE TABLE IF NOT EXISTS laptops (
	laptop_id TEXT NOT NULL,
	asset_tag TEXT NOT NULL UNIQUE,
	serial_number TEXT NOT NULL UNIQUE,
	brand TEXT NOT NULL,
	model TEXT NOT NULL,
	screen_size TEXT NOT NULL,
	processor TEXT NOT NULL,
	ram_gb SMALLINT NOT NULL,
	storage_gb INTEGER NOT NULL,
	unit_value NUMERIC(10,2) NOT NULL,
	distribution_status TEXT NOT NULL CHECK(distribution_status IN ('in_stock', 'distributed')),
	distribution_centre_id TEXT NOT NULL REFERENCES distribution_centres(distribution_centre_id),
	PRIMARY KEY(laptop_id)
);


CREATE TABLE IF NOT EXISTS distributions (
	distribution_id TEXT NOT NULL,
	distribution_date DATE NOT NULL,
	laptop_id TEXT NOT NULL UNIQUE REFERENCES laptops(laptop_id),
	client_id TEXT NOT NULL REFERENCES clients(client_id),
	PRIMARY KEY(distribution_id)
);

ALTER TABLE distribution_centres DISABLE ROW LEVEL SECURITY;
ALTER TABLE clients DISABLE ROW LEVEL SECURITY;
ALTER TABLE laptops DISABLE ROW LEVEL SECURITY;
ALTER TABLE distributions DISABLE ROW LEVEL SECURITY;