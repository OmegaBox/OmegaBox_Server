from django.utils.duration import _get_duration_components
from google.auth.transport import requests
from google.oauth2 import id_token

from config.settings._base import BOOT_PAY_REST_APP_ID, BOOT_PAY_PRIVATE_KEY, GOOGLE_CLIENT_ID
from utils.excepts import FailToGetBootPayAccessTokenException, UnverifiedReceiptException, VerifyRequestFailException, \
    PaymentCancelFailException, InvalidGoogleAccessTokenException
from .bootpay import BootpayApi
from .business_data import PRICE_BY_SCREEN_TYPE_CHART, PRICE_DISCOUNT_RATE_CHART


def reformat_duration(duration):
    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    return str(hours * 60 + minutes)


def calculate_seat_price(screen_type, grade):
    original_price = PRICE_BY_SCREEN_TYPE_CHART.get(screen_type, 'default')
    discount_rate = PRICE_DISCOUNT_RATE_CHART.get(grade, 'default')
    return int("%.0f" % (original_price * discount_rate))


def verify_receipt_from_bootpay_server(receipt_id, price):
    bootpay = BootpayApi(BOOT_PAY_REST_APP_ID, BOOT_PAY_PRIVATE_KEY)
    result = bootpay.get_access_token()
    if result['status'] is 200:
        verify_result = bootpay.verify(receipt_id)
        if verify_result['status'] is 200:
            if verify_result['data']['status'] == 1 and verify_result['data']['price'] == price:
                return verify_result['data']
            raise UnverifiedReceiptException
        raise VerifyRequestFailException
    raise FailToGetBootPayAccessTokenException


def cancel_payment_from_bootpay_server(receipt_id, price):
    bootpay = BootpayApi(BOOT_PAY_REST_APP_ID, BOOT_PAY_PRIVATE_KEY)
    result = bootpay.get_access_token()
    if result['status'] is 200:
        cancel_result = bootpay.cancel(receipt_id, price, name='omegabox', reason='변심')
        if cancel_result['status'] is 200:
            return cancel_result['data']
        raise PaymentCancelFailException


def check_google_oauth_api(google_id_token):
    client_id = GOOGLE_CLIENT_ID
    try:
        info = id_token.verify_oauth2_token(google_id_token, requests.Request(), client_id)
        unique_id = info['sub']
        return unique_id
    except ValueError:
        raise InvalidGoogleAccessTokenException
