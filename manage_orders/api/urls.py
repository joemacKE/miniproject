from django.urls import path
from .views import ListOrderAPIView, PostOrderAPIView,UpdateRetrieveOrderView, DeleteAPIView

urlpatterns = [
    path('list/', ListOrderAPIView.as_view(), name='list-orders'),
    path('create/', PostOrderAPIView.as_view(), name='post-order'),
    path('<int:pk>/update/', UpdateRetrieveOrderView.as_view(), name='update-view'),
    path('<int:pk>/delete/', DeleteAPIView.as_view(), name='delete-view'),
]