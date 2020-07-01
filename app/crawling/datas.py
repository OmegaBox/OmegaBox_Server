import datetime

import requests

# urls_params = [
#     # 주간/주말 박스오피스 (필요?)
#     (
#         'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json',
#         {
#             # 필수
#             'key': '',
#             'targetDt': '20200629',
#             # 옵션
#             'weekGb': '',
#             'itemPerPage': '',
#             'multiMovieYn': '',
#             'repNationCd': '',
#             'wideAreaCd': '',
#         }
#     ),
#
#     # 공통코드 조회 (필요?)
#     (
#         'http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json',
#         {
#             # 필수
#             'key': '',
#             'comCode': '0105000000',
#         }
#     ),
#
#     # 영화목록
#     (
#         'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json',
#         {
#             # 필수
#             'key': '',
#             # 옵션
#             'curPage': '',
#             'itemPerPage': '',
#             'movieNm': '광해, 왕이 된 남자',
#             'directorNm': '',
#             'openStartDt': '',
#             'openEndDt': '',
#             'prdtStartYear': '',
#             'prdtEndYear': '',
#             'repNationCd': '',
#             'movieTypeCd': '',
#         }
#     ),
#
#     # 영화사목록 (필요?)
#     (
#         'http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json',
#         {
#             # 필수
#             'key': '',
#             # 옵션
#             'curPage': '',
#             'itemPerPage': '',
#             'companyNm': '',
#             'ceoNm': '',
#             'companyPartCd': '',
#         }
#     ),
#
#     # 영화사 상세정보 (필요?)
#     (
#         'http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json',
#         {
#             # 필수
#             'key': '',
#             # 옵션
#             'companyCd': '',
#         }
#     ),
#
#     # 영화인목록 (필요?)
#     (
#         'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json',
#         {
#             # 필수
#             'key': '',
#             # 옵션
#             'curPage': '',
#             'itemPerPage': '',
#             'peopleNm': '',
#             'filmoNames': '',
#         }
#     ),
#
#     # 영화인 상세정보 (필요?)
#     (
#         'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json',
#         {
#             # 필수
#             'key': '',
#             'peopleCd': '20164556',
#         }
#     ),
# ]

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
    # 해당 영화 상세정보 출력을 위한 영화 코드
    MOVIE_CODE = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['movieCd']

    # 영화 순위
    BOXOFFICE_RANK = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['rank']

    # 누적관객수
    ACC_COUNT = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['audiAcc']

    # 해당일 상영작 매출총액 대비 매출 비율 (예매율 대체)
    SALES_SHARE = boxoffice_info['boxOfficeResult']['dailyBoxOfficeList'][rank]['salesShare']

    # 영화 코드별 상세 정보
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    param = {
        # 필수
        'key': '90aae50e8cd71ff96082a492f0da3918',
        'movieCd': f'{MOVIE_CODE}',
    }
    request_url = requests.get(url, params=param)
    movie_info = request_url.json()

    # 영화명(국문)
    MOVIE_INFO_NAME_KO = movie_info['movieInfoResult']['movieInfo']['movieNm']

    # 영화명(영문)
    MOVIE_INFO_NAME_ENG = movie_info['movieInfoResult']['movieInfo']['movieNmEn']

    # 상영시간
    MOVIE_INFO_SHOWTIME = movie_info['movieInfoResult']['movieInfo']['showTm']

    # 개봉일
    open_date = movie_info['movieInfoResult']['movieInfo']['openDt']
    open_year, open_month, open_day = int(open_date[:4]), int(open_date[4:6]), int(open_date[6:])
    MOVIE_OPEN_DATE = datetime.date(open_year, open_month, open_day)

    # 관람등급
    MOVIE_INFO_GRADE = movie_info['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
