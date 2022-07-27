from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from .models import Order
from .serializers import OrderSerializer, MyOrderSerializer


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
    serializer_class = OrderSerializer

    def create(self, request):
        print(request.data)
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            order = serializer.save(user=request.user)

            data = {'detail': 'Your order id is: ' + str(order.id)}

            return Response(data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class OrderRetrieveUpdate(RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    lookup_field = 'id'
    serializer_class = OrderSerializer
