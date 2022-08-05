from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from firebase_admin import messaging

from authentication.models import User
from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer, OrderListSerializer


def fcm_notify(username, title, body):
    try:
        user = User.objects.get(username=username)
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data={
                "title": title,
                "body": body,
            },
            token=user.fcm_token,
            android=messaging.AndroidConfig(
                priority='high',
                notification=messaging.AndroidNotification(
                    click_action="MainActivity")
            )
        )

        messaging.send(message)
    except Exception as e:
        print(e)


class MyOrderList(ListAPIView):
    serializer_class = MyOrderSerializer

    def get_queryset(self):
        """
        This view should return a list of all the orders
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)


class MyOrderRetrieve(RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = MyOrderSerializer

    def get_queryset(self):
        """
        This view should return a single order
        for the currently authenticated user.
        """
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderListCreate(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer

    def create(self, request):
        user = User.objects.get(username=request.user)
        shopkeeper = User.objects.get(is_shopkeeper=True)
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save(user=request.user)

            data = {'detail': 'Your order id is: ' + str(order.id)}
            fcm_notify(shopkeeper.username, "Order Received #" +
                       str(order.id), user.name)

            return Response(data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OrderRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    lookup_field = 'id'
    serializer_class = OrderSerializer

    def patch(self, request, *args, **kwargs):
        instance = super().patch(request, *args, **kwargs)
        if instance:
            data = {'detail': 'Status updated successfully'}
            return Response(data, status=HTTP_200_OK)
