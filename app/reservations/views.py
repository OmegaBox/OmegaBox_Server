from django.core.signals import request_finished
from django.dispatch import receiver
from django.shortcuts import render

# urls로 요청이 정상적으로 되면 print 출력 (나중에 url 추가하면 테스트)
@receiver(request_finished)
def post_request_receiver(sender, **kwargs):
    print('request finished!')
