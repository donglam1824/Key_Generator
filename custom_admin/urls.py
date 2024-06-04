from django.urls import path
from custom_admin import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', LoginView.as_view(template_name = 'admin_login.html'), name = "login"),
    path('generate_key', views.generate_key_byadmin, name='generate_key_byadmin'),  
    path('refresh_key/<int:key_id>/', views.refresh_key, name='refresh_key'),  
    path('delete_key/<int:key_id>/', views.delete_key, name='delete_key'),   
]
