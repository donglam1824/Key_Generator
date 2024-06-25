from django.urls import path
from custom_admin import views
from custom_admin.views import AdminLoginView, custom_logout_view

urlpatterns = [
    path('', AdminLoginView.as_view(), name='login'),
    path('generate_key', views.generate_key_byadmin, name='generate_key_byadmin'),  
    path('refresh_key/<int:key_id>/', views.refresh_key, name='refresh_key'),  
    path('delete_key/<int:key_id>/', views.delete_key, name='delete_key'),
    path('register/', views.register, name='register'),
    path('check_key', views.check_key, name='check_key'),
    path('logout/', custom_logout_view, name='logout'),
]
