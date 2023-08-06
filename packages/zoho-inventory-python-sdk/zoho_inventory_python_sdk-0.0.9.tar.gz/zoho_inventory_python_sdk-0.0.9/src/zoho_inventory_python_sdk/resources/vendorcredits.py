from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class VendorCredits(Client):
    def __init__(self, **opts):
        super(VendorCredits, self).__init__(**{**opts, **{"resource": "vendorcredits"}})

    def mark_as_open(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/open/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_void(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/void/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def submit(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/submit/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def approve(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/approve/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_bills(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/bills/",
                                        req={
                                            "method": "GET"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def apply_credits_to_bill(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/bills/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def delete_credits_applied_to_bill(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/bills/:bill_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def refund(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def update_refund(self, id_: str = "", body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "PUT",
                                            "body": body or {},
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def get_refund(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "GET",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_vendor_credit_refunds(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def delete_refund(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_refunds(self, query: dict = None):
        return self.authenticated_fetch(path=f"refunds/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_comments(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/comments/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def add_comment(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/comments/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def delete_comment(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/comments/:comment_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
