from django.urls import path
from .views import ProcessReceiptView, GetPointsView

urlpatterns = [
    path('receipts/process', ProcessReceiptView.as_view()),
    path('receipts/<str:receipt_id>/points', GetPointsView.as_view()),
]