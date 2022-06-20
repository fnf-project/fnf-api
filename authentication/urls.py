from django.urls import path

from authentication import views

urlpatterns = [
    path('api/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='profile'),
]
