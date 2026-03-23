import logging

from anymail.backends.mailgun import EmailBackend as MailgunEmailBackend

logger = logging.getLogger(__name__)


def _rq_send_messages(messages):
    """RQ job function that sends messages via the real Mailgun backend."""
    backend = MailgunEmailBackend()
    return backend.send_messages(messages)


def _is_rq_configured():
    """Check if django-rq is installed and configured."""
    try:
        import django_rq
        from django.conf import settings

        return bool(getattr(settings, 'RQ_QUEUES', None))
    except ImportError:
        return False


class EmailBackend(MailgunEmailBackend):
    """
    Mailgun email backend that enqueues messages via django-rq when available.

    Falls back to synchronous sending if django-rq is not installed or configured.
    """

    def __init__(self, *, rq_queue='default', **kwargs):
        self._rq_queue = rq_queue
        super().__init__(**kwargs)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        if not _is_rq_configured():
            return super().send_messages(email_messages)

        import django_rq

        queue = django_rq.get_queue(self._rq_queue)
        enqueued = 0
        for message in email_messages:
            try:
                queue.enqueue(_rq_send_messages, [message])
                enqueued += 1
            except Exception:
                logger.exception('Failed to enqueue email message')
                if not self.fail_silently:
                    raise

        return enqueued
