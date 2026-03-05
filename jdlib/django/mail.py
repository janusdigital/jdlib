from django.conf import settings

from jdlib.mail import send_mail as jdlib_send_mail


def send_mail(subject, message, from_email, recipient_list):
    return jdlib_send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        domain=settings.MAILGUN_DOMAIN,
        api_key=settings.MAILGUN_API_KEY,
    )
