# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+t9_0qhdz$s@rqd5mvw@t8hgh!mqz!4q#13m)94e)z2n^vjfdn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ZARINPAL = {
    'gateway_request_url': 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl',
    'gateway_callback_url': 'http://127.0.0.1:8000/finance/verify',
    'merchant_id': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
}
