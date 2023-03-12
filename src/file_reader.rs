use crate::media_objects::Episode;
use anyhow::{Ok, Result};
use chrono::prelude::NaiveDateTime;
use std::fs::File;
use std::sync::mpsc::SyncSender;

/// Read episodes from a .csv file and send them into a a queue for processing.
///
/// Returns a Result with the number of episodes read if everything went ok, the error otherwise
/// # Arguments
///
/// * `filepath` - A String with the correct path of seen_episode.csv
/// * `tx` - The sender from which sends the episodes read for a multithreaded operation
///
pub fn read_episodes(filepath: String, tx: SyncSender<Episode>) -> Result<usize> {
    let file = File::open(filepath)?;

    let mut reader = csv::Reader::from_reader(file);
    let mut counter = 0;

    for line in reader.records() {
        let record = line.unwrap();

        let season = record.get(2).unwrap().parse::<usize>()?;
        let number = record.get(3).unwrap().parse::<usize>()?;
        let tvdb_id = record.get(8).unwrap().parse::<usize>()?;
        let watched_at = record.get(0).unwrap();
        let watched_at = NaiveDateTime::parse_from_str(watched_at, "%Y-%m-%d %H:%M:%S")?;

        tx.send(Episode::new(season, number, tvdb_id, watched_at))?;
        counter += 1;
    }

    Ok(counter)
}
