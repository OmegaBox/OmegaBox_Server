from drf_yasg import openapi

movies_query_param = openapi.Parameter(
    'movies',
    openapi.IN_QUERY,
    description='검색 할 영화들의 ID (최대 3개) - 예시: 1+2+3',
    type=openapi.TYPE_STRING
)
adults_query_param = openapi.Parameter(
    'adults',
    openapi.IN_QUERY,
    description='어른 좌석의 수',
    type=openapi.TYPE_INTEGER
)
teens_query_param = openapi.Parameter(
    'teens',
    openapi.IN_QUERY,
    description='청소년 좌석의 수',
    type=openapi.TYPE_INTEGER
)
preferentials_query_param = openapi.Parameter(
    'preferentials',
    openapi.IN_QUERY,
    description='우대 좌석의 수',
    type=openapi.TYPE_INTEGER
)
