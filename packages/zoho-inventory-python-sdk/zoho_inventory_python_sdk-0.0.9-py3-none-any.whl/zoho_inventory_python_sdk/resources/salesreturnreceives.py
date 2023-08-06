from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
    - Override update, get and list Client methods to raise error.  
'''


class SalesReturnReceives(Client):
    def __init__(self, **opts):
        super(SalesReturnReceives, self).__init__(**{**opts, **{"resource": "salesreturnreceives"}})