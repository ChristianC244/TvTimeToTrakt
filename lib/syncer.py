import json


class syncer:
    """ Class SYNCER handles the communnication between Trakt API """

    def __init__(self, test: bool = False):
        """
        Parameters
        -----------
        test : bool
            if true will commuicate to test URL
        """
        
        self.WAIT_TIME = 1 # Time to wait between calls

        


