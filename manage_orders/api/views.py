from .serializers import OrderSerializer
from rest_framework import generics, status
from manage_orders.models import Order
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from users_app.api.permissions import IsOrderOwnerOrAdmin, IsClient
from django.db.models import Q

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
    permission_classes = [IsAuthenticated, IsClient]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    #ensure only clients have the authority to create orders
    def perform_create(self, serializer):
        if self.request.user.role != 'client':
            raise PermissionDenied("Only clients can post an order")
        
        pages = serializer.validated_data.get('pages', 0)
        amount_per_page = serializer.validated_data.get('amount_per_page', 0)
        total_amount = pages * amount_per_page

        serializer.save(client=self.request.user, total_amount=total_amount)

class UpdateRetrieveOrderView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin, IsClient]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class DeleteAPIView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOrderOwnerOrAdmin, IsClient]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()