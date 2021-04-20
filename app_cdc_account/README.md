# CDD Account App #
Read account information from CDC

### dependencies to install ###
datetime
requests
python-dotenv

## inspiring links ##
https://github.com/IgorJakovljevic/crypto-com-api

### API ###
https://exchange-docs.crypto.com/spot/index.html#introduction
https://exchange-docs.crypto.com/spot/index.html?python#digital-signature
https://exchange-docs.crypto.com/spot/index.html#public-get-instruments
https://exchange-docs.crypto.com/spot/index.html#private-get-account-summary

## play ##
cd ~/dev/repository/git/my_python/app_cdc_account
python3 app_cdc_account.py
python3 app_cdc_public.py

##### SQL #####
SELECT "currency",
       "balance",
       "available",
       "order",
       "stake"
  FROM "Account"
 WHERE "currency" = 'USDT';