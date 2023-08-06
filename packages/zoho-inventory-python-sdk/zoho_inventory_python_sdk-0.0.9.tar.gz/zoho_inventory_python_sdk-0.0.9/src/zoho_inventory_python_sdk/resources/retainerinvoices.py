from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
    - Missing methods to manage file attachments. 
'''


class RetainerInvoices(Client):
    def __init__(self, **opts):
        super(RetainerInvoices, self).__init__(**{**opts, **{"resource": "retainerinvoices"}})

    def mark_as_sent(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/sent/",
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

    def mark_as_draft(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/status/draft/",
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

    def update_template(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/templates/:template_id/",
                                        req={
                                            "method": "PUT",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def send_by_email(self, id_: str = "", body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def get_email_content(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "GET",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def update_billing_address(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/address/billing/",
                                        req={
                                            "method": "PUT",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def list_templates(self):
        return self.authenticated_fetch(path=f"templates/",
                                        req={
                                            "method": "GET",
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

    def update_comment(self, id_: str = "", body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/comments/:comment_id/",
                                        req={
                                            "method": "PUT",
                                            "body": body or {},
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )
