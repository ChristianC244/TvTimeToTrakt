class Token_info:

    def __init__(self):

        self.access_token = ""
        self.token_type = ""
        self.expires_in = ""
        self.refresh_token = ""
        self.created_at = ""
        
        self.has_values = False
        
    def from_dict(self, dic: dict):

        self.access_token = dic["access_token"]
        self.token_type = dic["token_type"]
        self.expires_in = dic["expires_in"]
        self.refresh_token = dic["refresh_token"]
        self.created_at = dic["created_at"]

        self.has_values = True

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "created_at": self.created_at
        }

