# https://exchange-docs.crypto.com/spot/index.html?python#digital-signature
import hashlib
import hmac


def sign_request(params_dict, api_key, secret_key):
    if params_dict is None or api_key is None or secret_key is None:
        return None
    # First ensure the params are alphabetically sorted by key
    param_string = ''
    if 'params' in params_dict:
        for key in sorted(params_dict['params']):
            param_string += key
            param_string += str(params_dict['params'][key])
    # Combine method + id + api_key + parameter string + nonce
    sig_pay_load = params_dict['method'] + str(params_dict['id']) + params_dict['api_key'] + param_string + str(params_dict['nonce'])
    # Use HMAC-SHA256 to hash the above using the API Secret as the cryptographic key
    params_dict['api_key'] = api_key
    params_dict['sig'] = hmac.new(
        bytes(str(secret_key), 'utf-8'),
        msg=bytes(sig_pay_load, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    # Encode the output as a hex string
    return params_dict
