from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import UserLoginForm, UserRegisterForm, RequestActivationEmailForm
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage, get_connection
from decouple import config
from custom_login.email_activation import activateEmail, activate
from django.urls import reverse, reverse_lazy

def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('mass:index'))
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect("mass:index")
            else:
                messages.error(request, 'Your account is not active. Please check your email for activation instructions.')
        else:
            messages.error(request, 'Invalid email or password.')
    
    context = {
        'form': form,
    }
    return render(request, "login.html", context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect("mass:index")
    next = request.GET.get('next')
    form = UserRegisterForm(request.POST or None)
    
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        resend_api_key = config('RESEND_API_KEY')
        if resend_api_key and config('USE_EMAIL_ACTIVATION', default=False, cast=bool):
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get("email"))
            messages.success(request, "We have sent you an email. Please confirm your email address to complete registration.")
        else:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Your account has been created.')
            if next:
                return redirect(next)
            return redirect("mass:index")
        
        if next:
            return redirect(next)
        return redirect("mass:index")
    
    context = {
        'form': form,
    }
    return render(request, "register.html", context)

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect("mass:index")

def request_activation_email(request):
    if request.method == 'POST':
        form = RequestActivationEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_model = get_user_model()
            try:
                user = user_model.objects.get(email=email, is_active=False)
                activateEmail(request, user, email)
                messages.success(request, "Activation email will be sent if the email is associated with an existing account.")
            except user_model.DoesNotExist:
                messages.success(request, "Activation email will be sent if the email is associated with an existing account.")
            return redirect('auth:request_activation_email')
    else:
        form = RequestActivationEmailForm()

    return render(request, 'request_activation_email.html', {'form': form})