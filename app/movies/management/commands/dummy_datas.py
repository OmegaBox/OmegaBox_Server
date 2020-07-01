import requests
from django.core.management import BaseCommand


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

        for rank in range(10):
            # 영화명
            movie_name = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['movieNm']

            # 개봉일
            open_date = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['openDt']

            # 해당일 관객수
            aud_count = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['audiCnt']

            # 누적관객수
            acc_count = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['audiAcc']

            # 해당일 상영작 매출총액 대비 매출 비율 (예매율 대체)
            sales_share = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['salesShare']

            # 해당 영화 상세정보 출력을 위한 영화 코드
            movie_code = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['movieCd']

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

            # 영화명(영문)
            movie_info_name_eng = movie_info['movieInfoResult']['movieInfo']['movieNmEn']

            # 상영시간
            movie_info_showtime = movie_info['movieInfoResult']['movieInfo']['showTm']

            # 개봉일
            movie_info_open_date = movie_info['movieInfoResult']['movieInfo']['openDt']

            # 제작상태
            movie_info_prd_stat = movie_info['movieInfoResult']['movieInfo']['prdtStatNm']

            # 제작국가
            nations = movie_info['movieInfoResult']['movieInfo']['nations']
            movie_info_nations = list()
            for idx in range(len(nations)):
                movie_info_nations.append(nations[idx]['nationNm'])

            # 장르
            genres = movie_info['movieInfoResult']['movieInfo']['genres']
            movie_info_genres = list()
            for idx in range(len(genres)):
                movie_info_genres.append(genres[idx]['genreNm'])

            # 감독 (2명 이상일 가능성)
            directors = movie_info['movieInfoResult']['movieInfo']['directors']
            movie_info_directors = list()
            for idx in range(len(directors)):
                movie_info_directors.append(directors[idx]['peopleNm'])

            # 배우
            actors = movie_info['movieInfoResult']['movieInfo']['actors']
            movie_info_actors = list()
            for idx in range(len(actors)):
                movie_info_actors.append(actors[idx]['peopleNm'])

            print(f'{rank + 1}위')
            print(f'{movie_name} / {open_date} / 일별관객수: {aud_count} (누적: {acc_count}) / {sales_share} / {movie_code}')
            print()
            print(
                f'{movie_info_name_ko}({movie_info_name_eng}) / {movie_info_showtime}분 / {movie_info_open_date} / {movie_info_prd_stat} / 국가: {movie_info_nations} / 장르: {movie_info_genres} / 감독: {movie_info_directors} / 배우: {movie_info_actors}')
            print()
