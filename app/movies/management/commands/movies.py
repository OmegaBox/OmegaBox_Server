import datetime
from django.core.management import BaseCommand

from crawling.datas import MOVIE_INFO_NAME_KO, MOVIE_INFO_NAME_ENG, MOVIE_CODE, MOVIE_INFO_SHOWTIME, BOXOFFICE_RANK, \
    ACC_COUNT, SALES_SHARE, MOVIE_OPEN_DATE, MOVIE_INFO_GRADE
from movies.models import Genre, Movie


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 영화 정보 -> 줄거리, 포스터, 예고편영상

        Movie.objects.get_or_create(name_kor=MOVIE_INFO_NAME_KO, name_eng=MOVIE_INFO_NAME_ENG, code=int(MOVIE_CODE),
                                    running_time=datetime.timedelta(minutes=int(MOVIE_INFO_SHOWTIME)),
                                    rank=int(BOXOFFICE_RANK),
                                    acc_audience=int(ACC_COUNT),
                                    reservation_rate=float(SALES_SHARE), open_date=MOVIE_OPEN_DATE,
                                    grade=MOVIE_INFO_GRADE)

        # 감독 (2명 이상일 가능성)
        # directors = movie_info['movieInfoResult']['movieInfo']['directors']
        # movie_info_directors = list()
        # for idx in range(len(directors)):
        #     movie_info_directors.append(directors[idx]['peopleNm'])
        # DIRECTORS.append(movie_info_directors)

        # 배우
        # actors = movie_info['movieInfoResult']['movieInfo']['actors']
        # movie_info_actors = list()
        # for idx in range(len(actors)):
        #     movie_info_actors.append(actors[idx]['peopleNm'])
        # ACTORS.append(movie_info_actors)

        # 장르
        # genres = movie_info['movieInfoResult']['movieInfo']['genres']
        # movie_info_genres = list()
        # for idx in range(len(genres)):
        #     movie_info_genres.append(genres[idx]['genreNm'])

    GENRES = ['드라마', '애니메이션', '어드벤처', '판타지', '범죄', '액션', '미스터리', '뮤지컬', '멜로/로맨스', '스릴러']
    for genre in GENRES:
        Genre.objects.get_or_create(name=genre)

    print('Movie.objects.all() >> ', Movie.objects.all())