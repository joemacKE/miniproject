from django.urls import path
from .views import ListOrderAPIView, PostOrderAPIView

urlpatterns = [
    path('list/', ListOrderAPIView.as_view(), name='list-orders'),
    path('create/', PostOrderAPIView.as_view(), name='post-order'),
]