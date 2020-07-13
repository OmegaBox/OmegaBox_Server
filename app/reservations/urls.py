from django.urls import path

from .views import SeatGradeCreateView, PaymentCreateView, PaymentCancelView

urlpatterns = [
    path('', SeatGradeCreateView.as_view()),
    path('payments/', PaymentCreateView.as_view()),
    path('payments/<int:pk>/cancel/', PaymentCancelView.as_view()),
]
