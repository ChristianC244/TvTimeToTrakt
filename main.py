from lib.syncer import Syncer
from lib.reader import CSVReader
import logging
from time import sleep

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def start():

    test = True
    if test: 
        logging.warning("TESTING ENVIRONMENT: INTERACTING WITH api-staging.trakt.tv")
    
    logging.info("#### STARTED")
    Syn = Syncer(test = test)
    Syn.authenticate()

    Reader = CSVReader()
    qnt = 1000
    remaining_time = len(Reader.episodes_watched)//qnt +1

    while True:
        remaining_time -= 1
        res, length = Reader.create_ep_dict(qnt)
        _, res = Syn.add_to_history(res)
        print(f"Remaining time... {remaining_time}s", end="\r")
        if length < qnt:
            break
        sleep(1)
    
    logging.info("History Added")
    print("History Added")

def remaining_time(rdr: CSVReader, qnt: int):
    len(rdr.episodes_watched)// qnt +1
    # Adding movies and other


if __name__ == "__main__":
    start()