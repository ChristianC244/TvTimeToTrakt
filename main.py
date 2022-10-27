from lib.syncer import Syncer
from lib.reader import CSVReader
import logging
from time import sleep

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def start():

    test = False
    qnt = 1000

    if test: 
        logging.warning("TESTING ENVIRONMENT: INTERACTING WITH api-staging.trakt.tv")
    
    logging.info("#### STARTED")

    # --- init ---
    Syn = Syncer(test = test)
    Syn.authenticate()
    Reader = CSVReader()
    time_left = remaining_time(Reader, qnt)
    
    # --- upload ---
    while True:
        time_left -= 1
        res, length = Reader.create_ep_dict(qnt)
        _, res = Syn.add_to_history(res)
        print(f"Remaining time... {time_left}s", end="\r")
        if length < qnt:
            break
        sleep(1)
    
    logging.info("--- History Added ---")
    print("History Added")

def remaining_time(rdr: CSVReader, qnt: int):
    """
    Calculates the time (s) to copy the data to trakt, based on the quantity of Object in each POST request and the rate of 1 API Call/s

    Parameters
    ---
    qnt: int
        how many object in a json in the POST request
    rdr: lib.CSVReader
        The Object that stores all the files to sent to trakt
    """
    t = len(rdr.episodes_watched) + len(rdr.movies_watched)

    return t // qnt + 1

    # Adding movies and other


if __name__ == "__main__":
    start()