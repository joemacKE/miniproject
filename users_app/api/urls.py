from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserProfileAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name="registration-view"),
    path('login/', LoginAPIView.as_view(), name='login-view'),
]