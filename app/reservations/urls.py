from django.urls import path

from .views import ReservationCreateView, PaymentCreateView, PaymentCancelView

urlpatterns = [
    path('', ReservationCreateView.as_view()),
    path('payments/', PaymentCreateView.as_view()),
    path('payments/<int:pk>/cancel/', PaymentCancelView.as_view()),
]
