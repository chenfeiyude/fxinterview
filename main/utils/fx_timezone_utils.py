from django.utils import timezone


def get_local_time_now():
    return timezone.localtime(timezone.now())