from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                tz = request.user.timezone
                if tz:
                    timezone.activate(ZoneInfo(tz))
            except ZoneInfoNotFoundError, AttributeError, KeyError:
                timezone.deactivate()
        return self.get_response(request)
