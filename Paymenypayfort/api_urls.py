from django.urls import path, include

urlpatterns = [
    path('v1/signup/', include('users.users_api.urls')),
    #path('v1/payments/', include('payments.payments_apis.urls')),
]