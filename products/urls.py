from django.urls import path

from products import views

urlpatterns = [
    path('api/products/', views.ProductList.as_view(), name='products'),
    path('api/products/new/', views.ProductCreate.as_view()),
    path('api/products/<int:id>/', views.ProductRetrieveUpdateDestroy.as_view()),
]
