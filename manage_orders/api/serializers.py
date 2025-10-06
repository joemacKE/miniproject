from rest_framework import serializers
from manage_orders.models import Order, Revision
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from decimal import Decimal

class OrderSerializer(serializers.ModelSerializer):
    total_amount = serializers.SerializerMethodField(read_only=True)
    client = serializers.StringRelatedField(read_only=True)
    assigned_writer = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['assigned_writer', 'total_amount', 'created_at', 'updated_at', 'uploaded_at']
    
    def get_total_amount(self, obj):

        return obj.pages * obj.amount_per_page
    

   