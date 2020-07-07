from django.utils.duration import _get_duration_components

from utils.business_data import PRICE_BY_SCREEN_TYPE_CHART, PRICE_DISCOUNT_RATE_CHART


def reformat_duration(duration):
    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)
    return str(hours * 60 + minutes)


def convert_list_to_dict(movies_list):
    movies_dict = {
        0: None,
        1: None,
        2: None
    }

    for idx, movie_id in enumerate(movies_list):
        movies_dict[idx] = movie_id

    return movies_dict


def calculate_seat_price(screen_type, grade):
    original_price = PRICE_BY_SCREEN_TYPE_CHART.get(screen_type, 'default')
    discount_rate = PRICE_DISCOUNT_RATE_CHART.get(grade, 'default')
    return int("%.0f" % (original_price * discount_rate))
