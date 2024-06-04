from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import render, redirect
import secrets
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LicenseKey
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

# Create your views here.

class admin_login(LoginView):
    template_name = 'admin_login.html' 
    redirect_authenticated_user = True          
    def get_success_url(self):
        if self.request.user.is_superuser:          
            return reverse_lazy('generate_key_byadmin')
        else:
            return '/'
        
def generateKey(length = 25):
    return secrets.token_hex(length)

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def generate_key_byadmin(request):
    license_keys = LicenseKey.objects.all()    #lay danh sach key

    if request.method == "POST":
        key = generateKey()
        license_key = LicenseKey(key = key)
        license_key.save()
        
    return render(request, 'generate_key.html', {'license_keys': license_keys})

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def refresh_key(request, key_id):
    try:
        license_key = LicenseKey.objects.get(pk = key_id)
        license_key.created_time = timezone.now()
        license_key.save()
        messages.success(request, 'Key đã được làm mới.')
    except LicenseKey.DoesNotExist:
        messages.error(request, 'Key không tồn tại.')
    return redirect('generate_key_byadmin')

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def delete_key(request, key_id):
    try:
        license_key = LicenseKey.objects.get(pk = key_id)
        license_key.delete()
        messages.success(request, 'Key đã được xóa.')
    except LicenseKey.DoesNotExist:
        messages.error(request, 'Key không tồn tại.')
    return redirect('generate_key_byadmin')
