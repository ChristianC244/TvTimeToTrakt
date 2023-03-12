use chrono::prelude::NaiveDateTime;

#[derive(Debug)]
pub struct Episode {
    season: usize,
    number: usize,
    tvdb_id: usize,
    watched_at: NaiveDateTime,
}
impl Episode {
    pub fn new(season: usize, number: usize, tvdb_id: usize, watched_at: NaiveDateTime) -> Episode {
        Episode {
            season,
            number,
            tvdb_id,
            watched_at,
        }
    }
}

// pub struct Movie {
//     title: String,
//     watched_at: DateTime<Utc>
// }
