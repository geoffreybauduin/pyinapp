from .purchase import Purchase
from .errors import InAppValidationError


class Receipt(object):
    def __init__(self, purchases, latest_receipt=None, pending_renewal_info=None, latest_receipt_info=None):
        self.purchases = purchases
        self.latest_receipt = latest_receipt
        self.pending_renewal_info = pending_renewal_info
        self.latest_receipt_info = latest_receipt_info

    @classmethod
    def from_appstore_response(cls, bundle_id, api_response):
        return cls(purchases=cls._parse_receipt(bundle_id=bundle_id, receipt=api_response.get("receipt"),
                                                response=api_response),
                   latest_receipt=api_response.get("latest_receipt"),
                   pending_renewal_info=PendingRenewalInfo.from_appstore_response(api_response=api_response),
                   latest_receipt_info=cls._parse_ios7_receipt(items=api_response.get("latest_receipt_info", []),
                                                               response=api_response),
                   )

    @classmethod
    def _parse_receipt(cls, bundle_id, receipt, response):
        if 'in_app' in receipt:
            if bundle_id != receipt['bundle_id']:
                error = InAppValidationError('Bundle id mismatch', response)
                raise error
            return cls._parse_ios7_receipt(items=receipt.get("in_app"), response=response)
        if bundle_id != receipt['bid']:
            error = InAppValidationError('Bundle id mismatch', response)
            raise error
        return cls._parse_ios6_receipt(receipt=receipt, response=response)

    @staticmethod
    def _parse_ios6_receipt(receipt, response):
        return [Purchase.from_app_store_receipt(receipt=receipt, response=response)]

    @staticmethod
    def _parse_ios7_receipt(items, response):
        return [Purchase.from_app_store_receipt(receipt=r, response=response) for r in items]


class PendingRenewalInfo(object):
    def __init__(self, product_id, is_in_billing_retry_period, original_transaction_id, auto_renew_status,
                 expiration_intent, auto_renew_product_id):
        self.product_id = product_id
        self.is_in_billing_retry_period = is_in_billing_retry_period
        self.original_transaction_id = original_transaction_id
        self.auto_renew_status = auto_renew_status
        self.expiration_intent = expiration_intent
        self.auto_renew_product_id = auto_renew_product_id

    @classmethod
    def from_appstore_response(cls, api_response):
        if "pending_renewal_info" not in api_response:
            return None
        return [cls(auto_renew_product_id=pri['auto_renew_product_id'],
                    is_in_billing_retry_period=pri['is_in_billing_retry_period'],
                    original_transaction_id=pri['original_transaction_id'],
                    auto_renew_status=pri['auto_renew_status'],
                    expiration_intent=pri['expiration_intent'],
                    product_id=pri['product_id']) for pri in api_response['pending_renewal_info']]
