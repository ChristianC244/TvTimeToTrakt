from lib.syncer import Syncer
import logging

logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)

def start():
    
    Syn = Syncer(test = True)
    Syn.authenticate()
    


if __name__ == "__main__":
    start()