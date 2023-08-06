from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
'''


class CreditNotes(Client):
    def __init__(self, **opts):
        super(CreditNotes, self).__init__(**{**opts, **{"resource": "creditnotes"}})

    def send_credit_note_by_email(self, id_: str = "", body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def get_credit_note_email_history(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/emailhistory/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def get_credit_note_email_content(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_void(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/void/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_draft(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/draft/",
                                        req={
                                            "method": "POST"
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def mark_as_open(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/converttoopen/",
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

    def update_billing_address(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/address/billing/",
                                        req={
                                            "method": "PUT",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def update_shipping_address(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/address/shipping/",
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

    def update_template(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/templates/:template_id/",
                                        req={
                                            "method": "PUT",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_invoices_credited(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/invoices/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def apply_credits_to_invoices(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/invoices/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def delete_credits_applied_to_invoice(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/invoices/:invoice_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
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

    def list_refunds(self, query: dict = None):
        return self.authenticated_fetch(path=f"refunds/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_credit_note_refunds(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/refunds/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def get_credit_note_refund(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "GET",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def refund_credit_note(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def update_credit_note_refund(self, id_: str = "", body: dict = None, path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "PUT",
                                            "body": body or {},
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def delete_credit_note_refund(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/refunds/:refund_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )