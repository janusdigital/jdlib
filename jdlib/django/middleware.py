from zoneinfo import available_timezones, ZoneInfo, ZoneInfoNotFoundError

from django.utils import timezone


def get_timezone_choices():
    return [(tz, tz) for tz in sorted(available_timezones())]


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
