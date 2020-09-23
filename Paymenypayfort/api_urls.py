from django.urls import path, include

urlpatterns = [
    path('v1/signup/', include('users.users_api.urls')),
    path('v1/payments_info/', include('payments.payments_api.urls')),
]