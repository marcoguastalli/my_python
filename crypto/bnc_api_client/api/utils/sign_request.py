# https://binance-docs.github.io/apidocs/spot/en/#endpoint-security-type
import hashlib
import hmac


def sign_request(params_dict, api_key, secret_key):
    if params_dict is None or api_key is None or secret_key is None:
        return None
    param_string = ''
    # Add all the element of the dictionary to param_string
    for key, value in params_dict.items():
        param_string += "&" + key + "="
        param_string += str(params_dict[key])
    # Encode the output as a hex string
    signature = hmac.new(secret_key.encode('utf-8'), param_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return param_string + "&signature=" + signature
