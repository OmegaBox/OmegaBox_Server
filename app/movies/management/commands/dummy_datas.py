from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 필요 정보
        # 영화 정보 -> 개봉일, 영화 이름(국문), 영화 이름(영문), 영화 코드, 상영시간, 장르, 관람등급, 줄거리, 포스터, 예고
        # 박스오피스 정보 -> 순위, 누적관객수, 예매율
        pass
