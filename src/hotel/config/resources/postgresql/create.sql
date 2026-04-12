SET default_tablespace = hotelspace;

CREATE TABLE IF NOT EXISTS hotel (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    version       INTEGER NOT NULL DEFAULT 0,
    name          TEXT NOT NULL,
    erzeugt       TIMESTAMP NOT NULL,
    aktualisiert  TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS hotel_name_idx ON hotel(name);

CREATE TABLE IF NOT EXISTS standort (
    id           INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    strasse      TEXT NOT NULL,
    hausnummer   TEXT NOT NULL,
    plz          TEXT NOT NULL CHECK (plz ~ '\d{5}'),
    ort          TEXT NOT NULL,
    land         TEXT NOT NULL,
    hotel_id     INTEGER NOT NULL UNIQUE REFERENCES hotel ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS standort_hotel_id_idx ON standort(hotel_id);
CREATE INDEX IF NOT EXISTS standort_plz_idx ON standort(plz);

CREATE TABLE IF NOT EXISTS zimmer (
    id            INTEGER GENERATED ALWAYS AS IDENTITY(START WITH 1000) PRIMARY KEY,
    preis         NUMERIC(10,2) NOT NULL,
    zimmernummer  TEXT NOT NULL,
    hotel_id      INTEGER NOT NULL REFERENCES hotel ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS zimmer_hotel_id_idx ON zimmer(hotel_id);
CREATE INDEX IF NOT EXISTS zimmer_nummer_idx ON zimmer(zimmernummer);