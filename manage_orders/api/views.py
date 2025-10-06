from .serializers import OrderSerializer
from rest_framework import generics, status
from manage_orders.models import Order
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class ListOrderAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(user, 'role', None) == 'client':
            return Order.objects.filter(client=user)
        
        if getattr(user, 'role', None) == 'writer':
            return Order.objects.filter(
                Q(status='available')
            ).distinct()
        if user.is_staff or getattr(user, 'role', None) == 'admin':
            return Order.objects.all()
        return Order.objects.none()

class PostOrderAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer