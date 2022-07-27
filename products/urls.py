from django.urls import path

from products import views

urlpatterns = [
    path('api/categories/', views.CategoryListCreate.as_view()),
    path('api/categories/<slug:category_slug>/', views.CategoryDetail.as_view()),
    path('api/products/', views.ProductListCreate.as_view(), name='products'),
    path('api/products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('api/products/<int:id>/', views.ProductRetrieveUpdateDestroy.as_view()),
]
