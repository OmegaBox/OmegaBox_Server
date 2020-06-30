import json

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        f = open('crawling/jsons/boxoffice_daily.json', 'r')
        boxoffice_daily_content = json.load(f)

        # 일별박스오피스 랭크 2위인 영화이름 출력
        rank = 2
        print(boxoffice_daily_content['boxOfficeResult']['dailyBoxOfficeList'][rank - 1]['movieNm'])
