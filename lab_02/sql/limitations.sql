ALTER TABLE Driver
ALTER COLUMN first_name SET NOT NULL,
ALTER COLUMN last_name SET NOT NULL,
ALTER COLUMN date_of_birthday SET NOT NULL,
ADD UNIQUE (document_number),
ADD check (document_number >= 100000000 and document_number <= 9999999999);

ALTER TABLE Trip
ALTER COLUMN source_address SET NOT NULL,
ALTER COLUMN destenation_address SET NOT NULL,
ADD PRIMARY KEY (id),
ADD CHECK (price >= 0);

ALTER TABLE Passenger
ALTER COLUMN first_name SET NOT NULL,
ALTER COLUMN last_name SET NOT NULL,
ALTER date_of_birthday SET NOT NULL;

ALTER TABLE Payment
ADD CHECK (invoice >= 100000 and invoice <= 999999);

ALTER TABLE Car 
ADD PRIMARY KEY (id),
ADD CHECK (mileage >= 0);