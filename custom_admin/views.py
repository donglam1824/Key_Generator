from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
import secrets
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LicenseKey
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .serializers import KeySerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
# Create your views here.

class AdminLoginView(LoginView):
    template_name = 'admin_login.html' 
    redirect_authenticated_user = True          

    def get_success_url(self):
        if self.request.user.is_superuser:          
            return reverse_lazy('generate_key_byadmin')
        else:
            return reverse_lazy('check_key')
        
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Form handles password hashing automatically
            return redirect('login')  # Redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})   

def custom_logout_view(request):
    logout(request)
    return redirect('login')  

        
def generateKey(length = 25):
    return secrets.token_hex(length)

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def generate_key_byadmin(request):
    license_keys = LicenseKey.objects.all() 
       #lay danh sach key
    if request.method == "POST" and 'key_file' in request.FILES:
        key_file = request.FILES['key_file']

        if key_file.name.endswith('.txt'):  #Kiem tra dinh dang file
            key_data = key_file.read().decode('utf-8')
            license_key = LicenseKey(key = key_data)
            license_key.save()
            return render(request, 'generate_key.html', {'license_keys': license_keys})
        else:
            return render(request, 'generate_key.html', {'license_keys': license_keys})
    elif request.method == "POST":
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

@user_passes_test(lambda u: u.is_superuser)
@login_required(login_url='login')
def copy_key(request, key_id):
    key = get_object_or_404(LicenseKey, pk=key_id)
    return render(request, 'generate_key.html', {'key': key, 'license_keys': LicenseKey.objects.all()})

def check_key(request):  
    if request.method == 'POST':
        key_value = request.POST.get('key')

        try: 
            license_key = LicenseKey.objects.get(key=key_value)
            if license_key.is_active:
                message = f"The key '{key_value}' is active."
            else:
                message = f"The key '{key_value}' is inactive."
        except LicenseKey.DoesNotExist:
            message = f"The key '{key_value}' does not exist."

        return render(request, 'check_key.html', {'message': message}) 
    return render(request, 'check_key.html')

class LicenseKeyListAPIView(generics.ListCreateAPIView):
    queryset = LicenseKey.objects.all()
    serializer_class = KeySerializer
    permission_classes = [AllowAny]


        

