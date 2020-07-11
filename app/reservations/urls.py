from django.urls import path

from .views import SeatGradeCreateView, PaymentCreateView

urlpatterns = [
    path('', SeatGradeCreateView.as_view()),
    path('payment/', PaymentCreateView.as_view()),
]
