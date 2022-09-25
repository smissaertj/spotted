import re
from decouple import config

flask_config = {
    "SECRET_KEY": config('FLASK_SECRET'),
    "DEBUG": config('FLASK_DEBUG'),
    "PORT": config('FLASK_PORT')
}

firebaseAdmin_config = {
    "type": "service_account",
    "project_id": config('FBA_PROJECT_ID'),
    "private_key_id": config('FBA_PRIVATE_KEY_ID'),
    "private_key": re.sub(r'\\n', '\n', config('FBA_PRIVATE_KEY')),
    "client_email": config('FBA_CLIENT_EMAIL'),
    "client_id": config('FBA_CLIENT_EMAIL'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": config('FBA_CLIENT_X509_CERT_URL')
}
