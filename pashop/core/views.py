from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from core.forms import RegistrationForm
from core.models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = get_user_model().objects.create_user(
                name=name,
                email=email,
                password=password,
                is_active=False
            )
            user.save()

            # ACCOUNT ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            mail_body = render_to_string('user/account_verification.html',
                                         {
                                             'user': user,
                                             'domain': current_site,
                                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                             'token': default_token_generator.make_token(user)
                                         }
                                         )
            send_email = EmailMessage(mail_subject, mail_body, to=[email])
            send_email.send()
            return redirect('/user/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {'form': form}
    return render(request, 'user/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return render(request, 'user/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    is_valid_token = default_token_generator.check_token(user, token)
    if user is not None and is_valid_token:
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid verification link')
        return redirect('register')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'user/dashboard.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if get_user_model().objects.filter(email=email).exists():
            user = get_user_model().objects.get(email=email)
            current_site = get_current_site(request)
            mail_subject = 'Password Reset'
            mail_body = render_to_string('user/password_reset_email.html',
                                         {
                                             'user': user,
                                             'domain': current_site,
                                             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                             'token': default_token_generator.make_token(user)
                                         }
                                         )
            send_email = EmailMessage(mail_subject, mail_body, to=[email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'user/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        uid, user = None, None

    is_valid_token = default_token_generator.check_token(user, token)
    if user is not None and is_valid_token:
        request.session['uid'] = uid
        return redirect('password_reset')
    else:
        messages.error(request, 'Invalid password reset link')
        return redirect('login')


def password_reset(request):
    if request.method == 'POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            user = get_user_model().objects.get(pk=request.session.get('uid'))
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('reset_password')

    return render(request, 'user/password_reset.html')
