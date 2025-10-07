-- CREATE TABLE driver_extended_info (
--     driver_id INTEGER PRIMARY KEY REFERENCES driver(id) ON DELETE CASCADE,
--     profile JSONB NOT NULL
-- );


INSERT INTO driver_extended_info (driver_id, profile) VALUES
(1, '{
    "personal": {
        "full_name": "Иван Петров",
        "phone": "+79001234567",
        "email": "ivan.petrov@example.com"
    },
    "vehicle": {
        "brand": "Toyota",
        "model": "Camry",
        "year": 2020,
        "color": "Серебристый",
        "features": ["кондиционер", "навигация", "бесплатный Wi-Fi"]
    },
    "work_preferences": {
        "max_trip_distance_km": 50,
        "available_hours": {"start": "08:00", "end": "22:00"},
        "payment_methods": ["card", "cash"],
        "pets_allowed": true
    },
    "ratings_detail": {
        "punctuality": 4.8,
        "cleanliness": 4.6,
        "driving_style": 4.9,
        "total_trips": 127
    }
}'::JSONB),

(2, '{
    "personal": {
        "full_name": "Анна Смирнова",
        "phone": "+79009876543",
        "email": "anna.smirnova@example.com"
    },
    "vehicle": {
        "brand": "Hyundai",
        "model": "Solaris",
        "year": 2022,
        "color": "Белый",
        "features": ["кондиционер", "подогрев сидений"]
    },
    "work_preferences": {
        "max_trip_distance_km": 30,
        "available_hours": {"start": "10:00", "end": "20:00"},
        "payment_methods": ["card"],
        "pets_allowed": false
    },
    "ratings_detail": {
        "punctuality": 4.9,
        "cleanliness": 4.8,
        "driving_style": 4.7,
        "total_trips": 89
    }
}'::JSONB),

(3, '{
    "personal": {
        "full_name": "Елена Козлова",
        "phone": "+79005556677",
        "email": "elena.kozlova@example.com"
    },
    "vehicle": {
        "brand": "Kia",
        "model": "Rio",
        "year": 2021,
        "color": "Чёрный",
        "features": ["кондиционер", "бесплатная вода", "детское кресло"]
    },
    "work_preferences": {
        "max_trip_distance_km": 40,
        "available_hours": {"start": "07:00", "end": "23:00"},
        "payment_methods": ["card", "cash", "crypto"],
        "pets_allowed": true
    },
    "ratings_detail": {
        "punctuality": 4.7,
        "cleanliness": 4.9,
        "driving_style": 4.8,
        "total_trips": 203
    }
}'::JSONB);