from django.utils.duration import _get_duration_components


def reformat_duration(duration):
    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    return str(hours * 60 + minutes)
