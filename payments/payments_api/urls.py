from django.urls import path
from . import views

urlpatterns = [
    path('customer_id/', views.customer_id_api, name='customer_id'),
    path('transaction_info/', views.transaction_api, name='transaction_info'),
]