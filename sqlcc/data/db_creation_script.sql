CREATE TABLE neighbourhoods
  (
     neighbourhood_id INTEGER NOT NULL CONSTRAINT neigbourhood_id PRIMARY KEY,
     neighbourhood    TEXT NOT NULL
  );

CREATE TABLE listings
  (
     listing_id       INTEGER NOT NULL,
     listing          TEXT NOT NULL,
     host_id          INTEGER NOT NULL CONSTRAINT listings_pk UNIQUE,
     host             TEXT,
     neighbourhood_id INTEGER NOT NULL CONSTRAINT listings_neigbourhoods_null_fk
     REFERENCES neigbourhoods,
     room_type        TEXT,
     price_in_dollar  REAL
  );

CREATE TABLE calendar
  (
     listing_id      INTEGER NOT NULL CONSTRAINT calendar_listings_null_fk
     REFERENCES
     listings (listing_id)
     ON UPDATE CASCADE ON DELETE CASCADE,
     date            TEXT NOT NULL,
     available       TEXT,
     price_in_dollar REAL,
     minimum_nights  INTEGER,
     CONSTRAINT calendar_pk PRIMARY KEY (listing_id, date)
  );

CREATE TABLE reviews
  (
     listing_id  INTEGER NOT NULL CONSTRAINT reviews_listings_null_fk REFERENCES
     listings (listing_id)
     ON UPDATE CASCADE ON DELETE CASCADE,
     review_id   INTEGER NOT NULL CONSTRAINT reviews_pk PRIMARY KEY,
     date        TEXT,
     reviewer_id INTEGER NOT NULL,
     reviewer    TEXT,
     comments    TEXT
  ); 