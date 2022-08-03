from rest_framework import serializers

from .models import Order, OrderItem
from authentication.serializers import ProfileSerializer
from products.serializers import ProductSerializer


class MyOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
        )

class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "total",
            "discount",
            "subTotal",
            "status",
            "items"
        )


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "product",
            "quantity",
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    # user = ProfileSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "total",
            "discount",
            "subTotal",
            "items",
            # "user"
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class OrderListSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)
    user = ProfileSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "total",
            "discount",
            "subTotal",
            "items",
            "user"
        )
