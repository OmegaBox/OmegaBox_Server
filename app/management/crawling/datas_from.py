urls_params = [
    # 주간/주말 박스오피스 (필요?)
    (
        'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json',
        {
            # 필수
            'key': '',
            'targetDt': '20200629',
            # 옵션
            'weekGb': '',
            'itemPerPage': '',
            'multiMovieYn': '',
            'repNationCd': '',
            'wideAreaCd': '',
        }
    ),

    # 공통코드 조회 (필요?)
    (
        'http://www.kobis.or.kr/kobisopenapi/webservice/rest/code/searchCodeList.json',
        {
            # 필수
            'key': '',
            'comCode': '0105000000',
        }
    ),

    # 영화목록
    (
        'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json',
        {
            # 필수
            'key': '',
            # 옵션
            'curPage': '',
            'itemPerPage': '',
            'movieNm': '광해, 왕이 된 남자',
            'directorNm': '',
            'openStartDt': '',
            'openEndDt': '',
            'prdtStartYear': '',
            'prdtEndYear': '',
            'repNationCd': '',
            'movieTypeCd': '',
        }
    ),

    # 영화사목록 (필요?)
    (
        'http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyList.json',
        {
            # 필수
            'key': '',
            # 옵션
            'curPage': '',
            'itemPerPage': '',
            'companyNm': '',
            'ceoNm': '',
            'companyPartCd': '',
        }
    ),

    # 영화사 상세정보 (필요?)
    (
        'http://kobis.or.kr/kobisopenapi/webservice/rest/company/searchCompanyInfo.json',
        {
            # 필수
            'key': '',
            # 옵션
            'companyCd': '',
        }
    ),

    # 영화인목록 (필요?)
    (
        'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json',
        {
            # 필수
            'key': '',
            # 옵션
            'curPage': '',
            'itemPerPage': '',
            'peopleNm': '',
            'filmoNames': '',
        }
    ),

    # 영화인 상세정보 (필요?)
    (
        'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.json',
        {
            # 필수
            'key': '',
            'peopleCd': '20164556',
        }
    ),
]
