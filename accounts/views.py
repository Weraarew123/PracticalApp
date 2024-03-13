from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from accounts.forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            if User.objects.filter(email=email).first():
                messages.error(request, "Istnieje już użytkownik z podanym mailem")
                return redirect('register')
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            user.is_active = False
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Proszę aktywować konto'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email adress [email]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.get(email=email)
        if user.check_password(password):
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Błędny login lub hasło!")
            return redirect('login')
        
    return render(request, 'accounts/login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('register')
    

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            #RESET PASSWORD EMAIL
            current_site = get_current_site(request)
            mail_subject = 'Please reset you password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Email do resetu hasła został wysłany na podanego maila')
            return redirect('login')
        else:
            messages.error(request, 'Konto nie istnieje!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetPassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Proszę zresetować hasło')
        return redirect('resetPassword')
    else:
        messages.error(request, 'Link już nie działa')
        return redirect('login')
    
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Reset hasła zakończony sukcesem')
            return redirect('login')
        else:
            messages.error(request, 'Hasła się nie zgadzają!')
            return redirect('resetPassword')
    return render(request, 'accounts/resetPassword.html')

@login_required
def change_email(request):
    user = request.user
    if request.method == "POST":
        password = request.POST['password']
        email = user.email
        user_object = User.objects.get(email=email)
        user_exists = user_object.check_password(password)

        if user_exists:
            return redirect('new_email')
        else:
            messages.error(request, 'Błędne hasło!')
            return redirect('change_email')
    return render(request, 'accounts/change_email.html')

def change_email_validation(request, uidb64, token, email):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
        email=email
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email = email
        user.save()
        messages.success(request, 'Zmiana maila zakończona sukcesem')
        return redirect('user_data')
    else:
        messages.error(request, 'Link wygasł. Mail został nie zmieniony')
        return redirect('user_data')
        

def new_email(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST['email']
        confirm_email = request.POST['confirm_email']
        if email == confirm_email:
            current_site = get_current_site(request)
            mail_subject = 'Please Potwierdzić zmianę maila'
            message = render_to_string('accounts/new_email_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'email': email,
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Aby dokończyć zmianę maila, sprawdź pocztę nowego maila')
            return redirect('user_data')
    return render(request, 'accounts/new_email.html')