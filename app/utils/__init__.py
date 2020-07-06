from django.utils.duration import _get_duration_components


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
