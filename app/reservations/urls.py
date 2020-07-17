from django.urls import path

from .views import ReservationCreateView, PaymentCreateView, PaymentCancelView, ReservationDeleteView

urlpatterns = [
    path('', ReservationCreateView.as_view()),
    path('<int:reservation_id>/', ReservationDeleteView.as_view()),
    path('payments/', PaymentCreateView.as_view()),
    path('payments/<int:pk>/cancel/', PaymentCancelView.as_view()),
]
