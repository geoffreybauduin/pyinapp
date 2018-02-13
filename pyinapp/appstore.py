from pyinapp.purchase import Purchase
from pyinapp.errors import InAppValidationError
from requests.exceptions import RequestException
import requests
from .receipt import Receipt

api_result_ok = 0
api_result_errors = {
    21000: 'Bad json',
    21002: 'Bad data',
    21003: 'Receipt authentication',
    21004: 'Shared secret mismatch',
    21005: 'Server is unavailable',
    21006: 'Subscription has expired',
    21007: 'Sandbox receipt was sent to the production env',
    21008: 'Production receipt was sent to the sandbox env',
}


class AppStoreValidator(object):
    def __init__(self, bundle_id, sandbox=False):
        self.bundle_id = bundle_id

        if sandbox:
            self.url = 'https://sandbox.itunes.apple.com/verifyReceipt'
        else:
            self.url = 'https://buy.itunes.apple.com/verifyReceipt'

    def _retrieve_from_apple_api(self, receipt_json):
        try:
            api_response = requests.post(self.url, json=receipt_json).json()
        except (ValueError, RequestException) as e:
            raise InAppValidationError('HTTP error: {}'.format(e))
        return api_response

    def validate(self, receipt, password=None):
        receipt_json = {'receipt-data': receipt}
        if password:
            receipt_json.update({'password': password})

        api_response = self._retrieve_from_apple_api(receipt_json=receipt_json)

        status = api_response['status']

        if status != api_result_ok:
            error = InAppValidationError(api_result_errors.get(status, 'Unknown API status'), api_response)
            raise error

        return Receipt.from_appstore_response(bundle_id=self.bundle_id, api_response=api_response)
