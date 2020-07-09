import datetime
import os

import requests
from django.core.management import BaseCommand

from movies.models import Movie, Director, Actor, Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 일별 박스오피스 1~10위 순위별 정보
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json'
        param = {
            # 필수
            'key': '90aae50e8cd71ff96082a492f0da3918',
            'targetDt': '20200703',
            # 옵션
            'itemPerPage': '',
            'multiMovieYn': '',
            'repNationCd': '',
            'wideAreaCd': '',
        }
        request_url = requests.get(url, params=param)
        boxoffice_info = request_url.json()

        for rank in range(10):
            movie_code = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['movieCd']
            boxoffice_rank = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['rank']
            acc_count = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['audiAcc']
            # 해당일 상영작 매출총액 대비 매출 비율 (예매율 대체)
            sales_share = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['salesShare']

            # 영화 코드별 상세 정보
            url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
            param = {
                # 필수
                'key': '90aae50e8cd71ff96082a492f0da3918',
                'movieCd': f'{movie_code}',
            }
            request_url = requests.get(url, params=param)
            movie_info = request_url.json()

            movie_info_name_ko = movie_info['movieInfoResult']['movieInfo']['movieNm']
            movie_info_name_eng = movie_info['movieInfoResult']['movieInfo']['movieNmEn']
            movie_info_showtime = movie_info['movieInfoResult']['movieInfo']['showTm']

            open_date = movie_info['movieInfoResult']['movieInfo']['openDt']
            open_year, open_month, open_day = int(open_date[:4]), int(open_date[4:6]), int(open_date[6:])
            movie_info_open_date = datetime.date(open_year, open_month, open_day)

            grade = movie_info['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
            movie_info_grade = ''

            if grade == '전체관람가': movie_info_grade = 'all'
            if grade == '12세이상관람가': movie_info_grade = '12+'
            if grade == '15세이상관람가': movie_info_grade = '15+'
            if grade == '청소년관람불가': movie_info_grade = '18+'

            # Movie 객체 생성 (박스오피스 1~10위)
            Movie.objects.get_or_create(name_kor=movie_info_name_ko, name_eng=movie_info_name_eng, code=int(movie_code),
                                        running_time=datetime.timedelta(minutes=int(movie_info_showtime)),
                                        rank=int(boxoffice_rank), acc_audience=int(acc_count),
                                        reservation_rate=float(sales_share), open_date=movie_info_open_date,
                                        grade=movie_info_grade, trailer=f'trailers/{movie_code}.mp4',
                                        poster=f'posters/{movie_code}.jpg'
                                        )
            print('Movie 객체들이 새로 생성되었습니다.')

            # 감독 (2명 이상일 가능성)
            directors = movie_info['movieInfoResult']['movieInfo']['directors']
            for idx in range(len(directors)):
                director = directors[idx]['peopleNm']
                # Director 객체 생성
                Director.objects.get_or_create(name=director)
                m = Movie.objects.get(code=movie_code)
                ds = Director.objects.filter(name=director)
                for d in ds:
                    m.director.add(d)
            print('Director 객체들이 MtoM으로 연결되었습니다.')

            actors = movie_info['movieInfoResult']['movieInfo']['actors']
            for idx in range(len(actors)):
                actor = actors[idx]['peopleNm']
                # Actor 객체 생성
                Actor.objects.get_or_create(name=actor)
                m = Movie.objects.get(code=movie_code)
                acs = Actor.objects.filter(name=actor)
                for ac in acs:
                    m.actor.add(ac)
            print('Actor 객체들이 MtoM으로 연결되었습니다.')

            genres = movie_info['movieInfoResult']['movieInfo']['genres']
            for idx in range(len(genres)):
                genre = genres[idx]['genreNm']
                # Genre 객체 생성
                Genre.objects.get_or_create(name=genre)
                m = Movie.objects.get(code=movie_code)
                gs = Genre.objects.filter(name=genre)
                for g in gs:
                    m.genre.add(g)
            print('Genre 객체들이 MtoM으로 연결되었습니다.')
