from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage, get_connection
from django.conf import settings
from decouple import config
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated.')
        return redirect(reverse('auth:login'))
    else:
        messages.error(request, 'The confirmation link was invalid, possibly because it has already been used or expired. Please request a new confirmation link.')

    return redirect(reverse('auth:login'))

def activateEmail(request, user, to_email):
    try:
        with get_connection(
            host=config('RESEND_SMTP_HOST'),
            port=config('RESEND_SMTP_PORT'),
            username=config('RESEND_SMTP_USERNAME'),
            password=config('RESEND_API_KEY'),
            
            use_tls=True,
        ) as connection:
            from_email = config('RESEND_FROM_EMAIL')
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'email': to_email,
                'protocol': 'https' if request.is_secure() else 'http',
            })

            email = EmailMessage(
                subject=subject,
                body=message,
                to=[to_email],
                from_email=from_email,
                connection=connection
            )
            email.content_subtype = 'html'
            email.send()
    except Exception as e:
        messages.error(request, 'Unable to send confirmation email. Please try again later.')

    return redirect(reverse('auth:login'))
