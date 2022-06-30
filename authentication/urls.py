from django.urls import path

from authentication import views

urlpatterns = [
    path('api/register/', views.RegisterAPIView.as_view(), name='register'),
    path('api/login/', views.LoginAPIView.as_view(), name='login'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='profile'),
]
