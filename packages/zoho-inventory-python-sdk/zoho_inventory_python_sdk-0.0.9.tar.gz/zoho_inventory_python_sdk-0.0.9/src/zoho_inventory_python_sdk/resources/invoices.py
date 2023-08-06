from ..client import Client


'''
TODO: 
    - Override or refactor Client methods create and update to accept query parameters.
    - Missing methods to manage file attachments. 
'''


class Invoices(Client):
    def __init__(self, **opts):
        super(Invoices, self).__init__(**{**opts, **{"resource": "invoices"}})

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

    def send_invoice_by_email(self, id_: str = "", body: dict = None, query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def send_invoices(self, query: dict = None):
        return self.authenticated_fetch(path=f"email/",
                                        req={
                                            "method": "POST",
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def get_invoice_email_content(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/email/",
                                        req={
                                            "method": "GET",
                                            "query": query or {}
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def get_payment_reminder_email_content(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/paymentreminder/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def disable_payment_reminder(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/paymentreminder/disable",
                                        req={
                                            "method": "POST",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def enable_payment_reminder(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/paymentreminder/enable",
                                        req={
                                            "method": "POST",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def bulk_export(self, query: dict = None):
        return self.authenticated_fetch(path=f"pdf/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def bulk_print(self, query: dict = None):
        return self.authenticated_fetch(path=f"print/",
                                        req={
                                            "method": "GET",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def write_off(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/writeoff/",
                                        req={
                                            "method": "POST",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def cancel_write_off(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/writeoff/cancel/",
                                        req={
                                            "method": "POST",
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

    def list_payments(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/payments/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def delete_payment(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/payments/:payment_id/",
                                        req={
                                            "method": "DELETE",
                                            "path_params": path_params or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def list_credits_applied(self, id_: str = ""):
        return self.authenticated_fetch(path=f"{id_}/creditsapplied/",
                                        req={
                                            "method": "GET",
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )

    def apply_credits(self, id_: str = "", body: dict = None):
        return self.authenticated_fetch(path=f"{id_}/credits/",
                                        req={
                                            "method": "POST",
                                            "body": body or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        encode_json_string=True,
                                        )

    def delete_credits_applied(self, id_: str = "", path_params: dict = None):
        return self.authenticated_fetch(path=f"{id_}/creditsapplied/:credit_note_id/",
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

    def add_comment(self, id_: str = "", query: dict = None):
        return self.authenticated_fetch(path=f"{id_}/comments/",
                                        req={
                                            "method": "POST",
                                            "query": query or {},
                                        },
                                        mimetype="application/x-www-form-urlencoded",
                                        )
