class Purchase(object):
    def __init__(self, transaction_id, product_id, quantity, purchased_at, response=None,
                 original_transaction_id=None, expires_date_ms=None, original_purchase_date=None,
                 original_purchase_date_ms=None, purchase_date_ms=None, web_order_line_item_id=None,
                 expires_date=None, original_purchase_date_pst=None, purchase_date_pst=None,
                 expires_date_pst=None, is_in_intro_offer_period=None, is_trial_period=None):
        self.transaction_id = transaction_id
        self.product_id = product_id
        self.quantity = quantity
        self.purchased_at = purchased_at
        self.response = response
        self.original_transaction_id = original_transaction_id
        self.expires_date_ms = expires_date_ms
        self.original_purchase_date = original_purchase_date
        self.original_purchase_date_ms = original_purchase_date_ms
        self.purchase_date_ms = purchase_date_ms
        self.web_order_line_item_id = web_order_line_item_id
        self.expires_date = expires_date
        self.original_purchase_date_pst = original_purchase_date_pst
        self.purchase_date_pst = purchase_date_pst
        self.expires_date_pst = expires_date_pst
        self.is_in_intro_offer_period = is_in_intro_offer_period
        self.is_trial_period = is_trial_period

    @classmethod
    def from_app_store_receipt(cls, receipt, response):
        purchase = {
            'transaction_id': receipt['transaction_id'],
            'product_id': receipt['product_id'],
            'quantity': receipt['quantity'],
            'purchased_at': receipt['purchase_date'],
            'response': response,
        }
        for key in ("original_transaction_id", "expires_date_ms", "original_purchase_date",
                    "original_purchase_date_ms", "purchase_date_ms", "web_order_line_item_id",
                    "expires_date", "original_purchase_date_pst", "purchase_date_pst",
                    "expires_date_pst", "is_in_intro_offer_period", "is_trial_period"):
            if key in receipt:
                purchase[key] = receipt[key]
        return cls(**purchase)

    @classmethod
    def from_google_play_receipt(cls, receipt):
        purchase = {
            'transaction_id': receipt.get('orderId', receipt.get('purchaseToken')),
            'product_id': receipt['productId'],
            'quantity': 1,
            'purchased_at': receipt['purchaseTime']
        }
        return cls(**purchase)
