from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class CustomerPayments(Client):
    def __init__(self, **opts):
        super(CustomerPayments, self).__init__(**{**opts, **{"resource": "customerpayments"}})