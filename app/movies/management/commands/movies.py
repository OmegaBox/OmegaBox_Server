import datetime

import requests
from django.core.management import BaseCommand

from movies.models import Genre, Movie


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 영화 정보 -> 줄거리, 포스터, 예고편영상

        # 일별 박스오피스 1~10위 순위별 정보
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
        param = {
            # 필수
            'key': '90aae50e8cd71ff96082a492f0da3918',
            'targetDt': '20200630',
            # 옵션
            'itemPerPage': '',
            'multiMovieYn': '',
            'repNationCd': '',
            'wideAreaCd': '',
        }
        request_url = requests.get(url, params=param)
        boxoffice_info = request_url.json()

        NAME_KORS = []
        NAME_ENGS = []
        CODES = []
        RUNNING_TIMES = []
        OPEN_DATES = []
        DIRECTORS = []
        ACTORS = []
        RANKS = []
        ACC_AUDS = []
        RESERVATION_RATES = []
        GRADES = []

        for rank in range(10):
            # 누적관객수
            acc_count = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['audiAcc']
            ACC_AUDS.append(int(acc_count))

            # 해당일 상영작 매출총액 대비 매출 비율 (예매율 대체)
            sales_share = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['salesShare']
            RESERVATION_RATES.append(float(sales_share))

            # 해당 영화 상세정보 출력을 위한 영화 코드
            movie_code = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['movieCd']
            CODES.append(movie_code)

            # 영화 순위
            rank = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['rank']
            RANKS.append(int(rank))

            # 영화 코드별 상세 정보
            url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
            param = {
                # 필수
                'key': '90aae50e8cd71ff96082a492f0da3918',
                'movieCd': f'{movie_code}',
            }
            request_url = requests.get(url, params=param)
            movie_info = request_url.json()

            # 영화명(국문)
            movie_info_name_ko = movie_info['movieInfoResult']['movieInfo']['movieNm']
            NAME_KORS.append(movie_info_name_ko)

            # 영화명(영문)
            movie_info_name_eng = movie_info['movieInfoResult']['movieInfo']['movieNmEn']
            NAME_ENGS.append(movie_info_name_eng)

            # 상영시간
            movie_info_showtime = movie_info['movieInfoResult']['movieInfo']['showTm']
            RUNNING_TIMES.append(datetime.timedelta(minutes=int(movie_info_showtime)))

            # 개봉일
            open_date = movie_info['movieInfoResult']['movieInfo']['openDt']
            open_year, open_month, open_day = int(open_date[:4]), int(open_date[4:6]), int(open_date[6:])
            movie_open_date = datetime.date(open_year, open_month, open_day)
            OPEN_DATES.append(movie_open_date)

            # 관람등급
            movie_info_grade = movie_info['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
            GRADES.append(movie_info_grade)

            # 감독 (2명 이상일 가능성)
            directors = movie_info['movieInfoResult']['movieInfo']['directors']
            movie_info_directors = list()
            for idx in range(len(directors)):
                movie_info_directors.append(directors[idx]['peopleNm'])
            DIRECTORS.append(movie_info_directors)

            # 배우
            actors = movie_info['movieInfoResult']['movieInfo']['actors']
            movie_info_actors = list()
            for idx in range(len(actors)):
                movie_info_actors.append(actors[idx]['peopleNm'])
            ACTORS.append((movie_info_actors))

            # 장르
            genres = movie_info['movieInfoResult']['movieInfo']['genres']
            movie_info_genres = list()
            for idx in range(len(genres)):
                movie_info_genres.append(genres[idx]['genreNm'])

        GENRES = ['드라마', '애니메이션', '어드벤처', '판타지', '범죄', '액션', '미스터리', '뮤지컬', '멜로/로맨스', '스릴러']
        for genre in GENRES:
            Genre.objects.get_or_create(name=genre)

        print('GRADES >> ', GRADES)
        # Movie.objects.get_or_create()
