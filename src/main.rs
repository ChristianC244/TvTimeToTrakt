use serde::{Deserialize, Serialize};
use std::fs::File;
use std::os::unix::prelude::FileExt;
use std::path::Path;
use std::sync::mpsc::sync_channel;
use std::{env, thread};

use tv_time_to_trakt::file_reader;

const CAPACITY: usize = 100;
fn main() {
    let working_directory = env::current_dir().unwrap().to_str().unwrap().to_owned();
    println!("Reading episodes from file...");

    // channel for local episodes watched
    let (tx, rx) = sync_channel(CAPACITY);
    let filepath = String::from(&working_directory) + "/data/seen_episode.csv";

    // This thread reads all the episodes from the right file
    let episode_reader_thread =
        thread::spawn(move || match file_reader::read_episodes(&filepath, tx) {
            Ok(v) => println!("Correctly read: {} episodes", v),
            Err(e) => println!("Error while reading episodes: {:?}", e),
        });

    check_setup(&working_directory);

    while let Ok(episode) = rx.recv() {
        // println!("{:?}", episode);
        drop(episode); //temporary
    }

    episode_reader_thread
        .join()
        .expect("Episode reader thread has panicked");

    println!("Send json to trakt");
}

#[derive(Serialize, Deserialize)]
struct Config {
    client_id: String,
    client_secret: String,
}
impl Config {
    fn new() -> Config {
        Config {
            client_id: String::new(),
            client_secret: String::new(),
        }
    }
}

/// Checks if the file `config.json` already exists
///
/// # Arguments
///
/// + wd - A string with the path of the working directory
fn check_setup(wd: &str) {
    let config_file_path = String::from(wd) + "/config.json";
    let config_file = Path::new(&config_file_path);
    if config_file.exists() {
        todo!("Read parameters and store to struct config")
    } else {
        println!("File config.json does not exists, creating one now.. ");
        let new_config = Config::new();
        let j = serde_json::to_vec(&new_config).unwrap();
        let file = File::create("config.json").expect("Couldn't create file");
        file.write_all_at(&j, 0)
            .expect("Couldn't rite in config.json");
    }
}

#[cfg(test)]
mod tests {
    use crate::check_setup;
    use std::{env, fs, path::Path};

    /// [TEST ONLY] Returns the absolute path of the WD if an empty String is passed
    ///
    /// # Arguments
    /// + `file` - pass an empty string to return the working directory, otherwise pass the relative path
    /// of a file to get the absolute path
    fn working_directory(file: &str) -> String {
        let wd = env::current_dir().unwrap().to_str().unwrap().to_owned();
        wd + file
    }

    /// Test 'check_setup()' behaviour when 'config.json' does not exists
    #[test]
    fn check_setup_no_file() {
        let wd = working_directory("");
        let config_file_path = wd.clone() + "/config.json";
        let config_file = Path::new(&config_file_path);
        if config_file.exists() {
            fs::remove_file(config_file_path).unwrap();
        }

        check_setup(&wd);
    }
    /// Test 'check_setup()' behaviour when 'config.json' does exists
    #[test]
    fn check_setup_file() {
        let wd = working_directory("");
        let config_file_path = wd.clone() + "/config.json";
        let config_file = Path::new(&config_file_path);
        assert!(config_file.exists());

        check_setup(&wd);
    }
}
