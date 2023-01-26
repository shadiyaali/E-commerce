from base64 import urlsafe_b64encode
from django.shortcuts import render,redirect
from django.contrib import messages,auth
from .models import Account
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
 

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
  
def register(request):
    if request.method == 'POST':
       form = RegistrationForm(request.POST)
       if form.is_valid():
           first_name = form.cleaned_data['first_name']
           last_name = form.cleaned_data['last_name']
           email = form.cleaned_data['email']
           phone_number = form.cleaned_data['phone_number']
           password = form.cleaned_data['password']
           username = email.split("@")[0]

           user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,username=username, password=password)
           user.phone_number = phone_number
           user.save()

        #    user activation
           current_site = get_current_site(request)
           mail_subject = 'please activate your account'
           message = render_to_string('accounts/account_verification_email.html', {
            'user':user,
            'domain': current_site,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
           })
           to_email = email
           send_email = EmailMessage(mail_subject, message, to=[to_email])
           send_email.send()
           messages.success(request, 'thank you for registering with us. we have sent you a verification email to your email adress.please verify it.')
           return render(request, 'accounts/login.html')
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

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in.')
            return redirect('index')
        

        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')



@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist): 
        user =None

    if user is not None and default_token_generator.check_token(user,token):     
        user.is_active = True
        user.save()
        messages.success(request, 'configuration your account is actived.')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation list')    
        return redirect('register')


        
@login_required(login_url= 'login')        
def user_dashboard(request): 
    
    return render(request, 'accounts/user_dashboard.html')


def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
             
            #  Reset password email
            current_site = get_current_site(request)
            mail_subject = ' Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
              'user':user,
              'domain': current_site,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'password reset email has been sent to your email adress.' )
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')   
            return redirect('forgotpassword') 

    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError,Account.DoesNotExist): 
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid 
        messages.success(request, 'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'this link has been expired')
        return redirect('login')


def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
           uid = request.session.get('uid')
           user = Account.objects.get(pk=uid)
           user.set_password(password)
           user.save()
           messages.success(request, 'password reset successful')
           return redirect('login') 

        else:
            messages.error(request, 'password do not match')   
            return redirect('resetpassword') 
    else:
        messages.success(request, 'password do not match')       
    return render(request, 'accounts/resetpassword.html')

           