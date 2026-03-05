import requests

from jdlib import env


MAILGUN_BASE_URL = 'https://api.mailgun.net'


def send_mail(subject, message, from_email, recipient_list, *, domain=None, api_key=None):
    if domain is None:
        domain = env.get('MAILGUN_DOMAIN')
    if api_key is None:
        api_key = env.get('MAILGUN_API_KEY')

    data = {
        'subject': subject,
        'text': message,
        'from': from_email,
        'to': ','.join(recipient_list),
    }

    return requests.post(
        f'{MAILGUN_BASE_URL}/v3/{domain}/messages',
        auth=('api', api_key),
        data=data,
    )
