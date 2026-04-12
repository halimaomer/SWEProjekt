DROP INDEX IF EXISTS
    standort_hotel_id_idx,
    standort_plz_idx,
    zimmer_hotel_id_idx,
    zimmer_nummer_idx,
    hotel_name_idx;

DROP TABLE IF EXISTS
    standort,
    zimmer,
    hotel;