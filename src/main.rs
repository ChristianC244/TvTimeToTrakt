use std::{sync::mpsc::sync_channel, thread};

use tv_time_to_trakt::file_reader;

const CAPACITY: usize = 100;
fn main() {
    println!("Reading episodes from file...");

    let (tx, rx) = sync_channel(CAPACITY);
    let filepath = String::from("/home/chris/TvTimeToTrakt/data/seen_episode.csv");

    let episode_reader_thread =
        thread::spawn(move || match file_reader::read_episodes(filepath, tx) {
            Ok(v) => println!("Correctly read: {} episodes", v),
            Err(e) => println!("Error while reading episodes: {:?}", e),
        });

    while let Ok(episode) = rx.recv() {
        println!("{:?}", episode);
    }

    episode_reader_thread
        .join()
        .expect("Episode reader thread has panicked");

    println!("Send json to trakt");
}
