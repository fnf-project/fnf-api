from django.urls import path

from orders import views

urlpatterns = [
    path('api/orders/new/', views.OrderCreate.as_view()),
    path('api/orders/<int:id>/', views.OrderRetrieveUpdate.as_view()),
    path('api/orders/', views.OrderList.as_view()),
    path('api/myorders/', views.MyOrderList.as_view()),
    path('api/myorder/<int:id>/', views.MyOrderRetrieve.as_view()),
]
