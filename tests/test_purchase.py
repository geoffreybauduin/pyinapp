from pyinapp.purchase import Purchase
from pyinapp.receipt import Receipt


def test_create_from_google_play_receipt():
    receipt = {
        'orderId': 1337,
        'productId': 'pew pew',
        'purchaseTime': '01.01.2016 12:00'
    }
    purchase = Purchase.from_google_play_receipt(receipt)

    assert purchase.transaction_id == receipt['orderId']
    assert purchase.product_id == receipt['productId']
    assert purchase.purchased_at == receipt['purchaseTime']
    assert purchase.quantity == 1
    assert purchase.response == None


def test_create_from_test_google_play_receipt():
    receipt = {
        'purchaseToken': 1337,
        'productId': 'pew pew',
        'purchaseTime': '01.01.2016 12:00'
    }
    purchase = Purchase.from_google_play_receipt(receipt)

    assert purchase.transaction_id == receipt['purchaseToken']
    assert purchase.product_id == receipt['productId']
    assert purchase.purchased_at == receipt['purchaseTime']
    assert purchase.quantity == 1


def test_create_from_app_store_receipt():
    response = '["in_app":[]]'
    receipt = {
        'transaction_id': 1337,
        'product_id': 'pew pew',
        'purchase_date': '01.01.2016 12:00',
        'quantity': 100500,
    }
    purchase = Purchase.from_app_store_receipt(receipt, response)

    assert purchase.transaction_id == receipt['transaction_id']
    assert purchase.product_id == receipt['product_id']
    assert purchase.purchased_at == receipt['purchase_date']
    assert purchase.quantity == receipt['quantity']
    assert purchase.response == response


def test_create_from_app_store_receipt_includes_subscriptions():
    response = {
        'latest_receipt': 'zzz',
        'status': 0,
        'latest_receipt_info': [{
            'web_order_line_item_id': '1000000037777533',
            'expires_date_pst': '2018-02-09 02:34:42 America/Los_Angeles',
            'expires_date': '2018-02-09 10:34:42 Etc/GMT',
            'transaction_id': '1000000374740957',
            'is_in_intro_offer_period': 'false',
            'quantity': '1',
            'original_purchase_date_ms': '1517994350000',
            'original_purchase_date_pst': '2018-02-07 01:05:50 America/Los_Angeles',
            'is_trial_period': 'false',
            'purchase_date': '2018-02-09 10:31:42 Etc/GMT',
            'original_transaction_id': '1000000373956032',
            'purchase_date_ms': '1518172302000',
            'expires_date_ms': '1518172482000',
            'original_purchase_date': '2018-02-07 09:05:50 Etc/GMT',
            'product_id': '1_week',
            'purchase_date_pst': '2018-02-09 02:31:42 America/Los_Angeles',
        }],
        'pending_renewal_info': [{
            'auto_renew_product_id': '1_week',
            'is_in_billing_retry_period': '0',
            'original_transaction_id': '1111',
            'auto_renew_status': '0',
            'expiration_intent': '1',
            'product_id': '1_week',
        }],
        'receipt': {
            'bundle_id': 'com.example',
            'receipt_creation_date': '2018-02-07 09:05:50 Etc/GMT',
            'request_date': '2018-02-11 16:51:37 Etc/GMT',
            'original_application_version': '1.0',
            'original_purchase_date': '2013-08-01 07:00:00 Etc/GMT',
            'receipt_creation_date_pst': '2018-02-07 01:05:50 America/Los_Angeles',
            'original_purchase_date_ms': '1375340400000',
            'request_date_pst': '2018-02-11 08:51:37 America/Los_Angeles',
            'original_purchase_date_pst': '2013-08-01 00:00:00 America/Los_Angeles',
            'receipt_creation_date_ms': '1517994350000',
            'request_date_ms': '1518367897158',
            'adam_id': 0,
            'in_app': [{
                'web_order_line_item_id': '1111',
                'expires_date_pst': '2018-02-07 02:05:48 America/Los_Angeles',
                'expires_date': '2018-02-07 10:05:48 Etc/GMT',
                'transaction_id': '1111',
                'is_in_intro_offer_period': 'false',
                'quantity': '1',
                'original_purchase_date_ms': '1517994350000',
                'original_purchase_date_pst': '2018-02-07 01:05:50 America/Los_Angeles',
                'is_trial_period': 'true',
                'purchase_date': '2018-02-07 09:05:48 Etc/GMT',
                'original_transaction_id': '1111',
                'purchase_date_ms': '1517994348000',
                'expires_date_ms': '1517997948000',
                'original_purchase_date': '2018-02-07 09:05:50 Etc/GMT',
                'product_id': '3day_trial',
                'purchase_date_pst': '2018-02-07 01:05:48 America/Los_Angeles',
            }],
            'application_version': '1',
            'version_external_identifier': 0
        }
    }

    receipt = Receipt.from_appstore_response(api_response=response, bundle_id="com.example")
    assert len(receipt.purchases) == 1
    assert receipt.purchases[0].transaction_id == response['receipt']['in_app'][0]['transaction_id']
    assert receipt.purchases[0].quantity == response['receipt']['in_app'][0]['quantity']
    assert receipt.purchases[0].product_id == response['receipt']['in_app'][0]['product_id']
    assert receipt.purchases[0].purchased_at == response['receipt']['in_app'][0]['purchase_date']

    assert len(receipt.pending_renewal_info) == 1
    assert receipt.pending_renewal_info[0].product_id == response['pending_renewal_info'][0]['product_id']
    assert receipt.pending_renewal_info[0].auto_renew_product_id == \
           response['pending_renewal_info'][0]['auto_renew_product_id']

    assert len(receipt.latest_receipt_info) == 1
    assert receipt.latest_receipt_info[0].quantity == response['latest_receipt_info'][0]['quantity']
    assert receipt.latest_receipt_info[0].product_id == response['latest_receipt_info'][0]['product_id']
    assert receipt.latest_receipt_info[0].purchased_at == response['latest_receipt_info'][0]['purchase_date']
