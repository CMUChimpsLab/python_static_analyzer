def connected(function):
    """
    Decorator that checks the api status
    before doing any request
    """
    def check_connection(self, *args, **kwargs):
        print("checking connection")
        print(self.api)
        if self.api is not None:
            print(self.api.authSubToken)
        if self.api is None or self.api.authSubToken is None:
            print("connecting")
            self.connect()
        return function(self, *args, **kwargs)
    return check_connection
