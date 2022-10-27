import pathlib
import csv
from datetime import datetime
import logging
import json
import os


class CSVReader:

    def __init__(self):
        self.PATH = str(pathlib.Path(__file__).parent.resolve()) + "/../"
        self.episodes_watched = list()
        self.movies_watched = list()
        self.ep_index = 0
        self.movie_index = 0
        self.reaction_index = 0 # TODO

        self.__load_indexes() # Update indexes        
        self.__read_watched_episodes()

    def create_ep_dict(self, n: int):
        """
        It creates the json for the post request, if available the episode will have the watchtime
        Returns an empty dictionary if there are no more episodes to send

        Params
        -------------
        n: int
            how many episodes to store in the json
        """
        episodes = []
        length = 0
        limit = min(n, len(self.episodes_watched) - self.ep_index)

        for t in self.episodes_watched[self.ep_index: self.ep_index + limit]:
            length += 1
            k = {
                "watched_at": t[0].strftime('%Y-%m-%dT%H:%M:%S.000Z'),
                "ids": {
                    "tvdb": t[1]
                }
            }
            episodes.append(k)
        
        final = {"episodes": episodes}
        
        self.ep_index += limit
        self.__save_indexes()

        return (final, length)

    def __read_watched_episodes(self):
        """
        This function reads the watched episodes, and stores them into the class.
        """
        """
        The episode is saved as a tuple (x, y)
        From the csv file: 
            x: obj[0]: timestamp | 28/09/2022 18:48:36 -
            y: obj[8]: episode_id        
        """
        with open(self.PATH + "data/seen_episode.csv") as csvfile:
            data = csv.reader(csvfile)
            next(csvfile) # skip first row

            for row in data:
            
                watched_at = datetime.strptime(row[0], "%Y-%m-%d  %H:%M:%S") 
                self.episodes_watched.append((watched_at, int(row[8]))) # Every episode is a tuple 

    def create_movie_dict(self, n: int):
        return

    def __read_watched_movies(self):
        """
        This function reads the watched movies, and stores them into the class.
        """
        """
        The episode is saved as a tuple (x, y)
        From the csv file: 
            x: obj[4]: timestamp | 28/09/2022 18:48:36 -
            y: obj[12]: movie_name       
        """
        with open(self.PATH + "data/tracking-prod-records.csv") as csvfile:
            data = csv.reader(csvfile)
            next(csvfile) # skip first row

            for row in data:
                watched_at = datetime.strptime(row[4], "%Y-%m-%d  %H:%M:%S") 
                self.movies_watched.append((watched_at, row[12])) # Every movie is a tuple
    
    # ---------------------------------------------- UTILS ------------------------------------------------------

    def __save_indexes(self):
        """Save indexes for movie/episodes list to history.json"""
        # TODO Add more indexes

        data = {"ep_index": self.ep_index, "movie_index": self.movie_index }
        with open(self.PATH + "history.json", "w") as file:
            json.dump(data, file, indent=4)
        
        logging.debug(f"ep_index saved: {self.ep_index} | movie_index: {self.movie_index}")
    
    def __load_indexes(self):
        """Loads indexes for movie/episodes list from history.json, if not initializated it creates it with indexes = 0"""
        # TODO Add more indexes

        if not os.path.exists(self.PATH + "history.json"):
            # If there isn't any config.json, it creates one
            history = {"ep_index": 0, "movie_index": 0}
            with open(self.PATH + "history.json", "w") as file:
                json.dump(history, file)


        with open(self.PATH + "history.json") as file:
            jload = json.load(file)
            self.ep_index = jload["ep_index"]
            self.movie_index = jload["movie_index"]
            
    

                