from django.shortcuts import render, redirect
from accounts.forms import SignupForm, RegistrationForm, ContactForm
#from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
#from .forms import regForm,regform1
import random,requests,json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login
from .models import UserProfile, OTP
from .utils import regex_phone
from . import send_email
from django.conf import settings
User = settings.AUTH_USER_MODEL
# Create your views here.

def home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ContactForm()
        args = {'form': form}
        return render(request,'accounts/home.html',args)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            args =form.clean()
            print(args,' aejgojga')
            try:
                print('inside')
                otp_check = OTP.objects.filter(contact=args.get('mobile_number'))
                print(otp_check.exists(), ' is val')
                if otp_check.exists():
                    print('double inside')
                    otp_verified= OTP.objects.last().is_otp_verified
                    print('below')
                    if not otp_verified:
                        return HttpResponse('OTP not verified',status=400)
                    else:
                        details =  send_email.send_mail(args.get('email_id'))
                        print(details,' are the detsils')
                        if details is None:
                            return HttpResponse(status=400)
                        else:
                            # mobile_number = args.get('mobile_number')
                            # email = args.get('email')
                            # door_no = args.get('door_number')
                            print(args.get('email'))
                            print(type(args.get('mobile_number')))
                            print(type(args.get('door_number')))
                            user = UserProfile.objects.create(
                            email=args.get('email_id'),
                            contact=args.get('mobile_number'),
                            door_number=args.get('door_number'))
                            return HttpResponse('mail sent please check your inbox', status=200)
                else:
                    return HttpResponse('no mobile number exists with this information', status=400)
            except:
                return HttpResponse('bad request',status=400)
            
            # print(args)
            # return redirect('/register',args)
    else:
        form = SignupForm()
        args = {'form': form}
        return render(request,'accounts/signup.html',args)

def register(request, email_id):
    print(email_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        print('is the form')
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            args=form.clean()
            print(args)
            try:
                user = UserProfile.objects.filter(email=email_id)
                if(user.exists()):
                    user = user.first()
                    user.username=args.get('username')
                    user.password  = args.get('password1')
                    user.save() 
            # form.save()
                    return redirect('/login')
                return HttpResponse('hello ...', status=400)
            except:
                return HttpResponse('error occured while registering', status=400)
        else:
            return HttpResponse("Invalid Ferm", status=400)
    else:
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'accounts/register.html',args)

@login_required
def user_home(request):
    args = {'user': request.user}
    return render(request, 'accounts/user_home.html',args)

@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html',args)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('/user/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}
        return render(request, 'accounts/edit_profile.html',args)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/user/profile')
        else:
            return redirect('/user/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html',args)

# def regView(request):
#     form = regForm()
#     form1 = regform1()
#     if request.method == 'POST':
#         form = regForm(data=request.POST)
#         form1 = regform1(data=request.POST)

#         if form.is_valid() and form1.is_valid():
#             user = form.save()
#             user.set_password(user.password)
#             user.save()

#             profile = form1.save(commit = False)
#             profile.user = user
#             profile.save()
#             return HttpResponse('Register Successfully!!!')

#     return render(request,'accounts/registration.html',{'form':form,'form1':form1})

def generate_otp(request):
    if request.method == 'GET':
        mobile_number = request.GET['mobile_number']
        email = 'amans@gmail.com'
        print(mobile_number)
        headers = {'X-Authy-API-Key': 'b1nV9bl94GpFPggznR4UqKehe8gbRih9',}
        data = {
        'user[email]': email,
        'user[cellphone]': mobile_number,
        'user[country_code]': '91'
        }
        response = requests.post('https://api.authy.com/protected/json/users/new', headers=headers, data=data)
        print(response.content)
        if response.status_code == 200:
            UID=json.loads(response.text)
            UID=UID["user"]["id"]
            res=requests.get('https://api.authy.com/protected/json/sms/'+str(UID)+'?force=true', headers=headers, data={})
            print(res.content)
            if res.status_code==200:
                content = {
                    'uid': UID,
                    'contact': mobile_number
                }
                print(content)
                return JsonResponse(content)
            else:
                return HttpResponse(0)
        return HttpResponse(0)
    return HttpResponse(0)

# def loginView(request):
#     if request.method == 'GET':
#         username = request.POST['un']
#         user = User.objects.get(username=username)
#         msg = '<h1>Hello {} You are now Logged In</h1>'.format(user.username)
#         login(request,user)
#         return HttpResponse(msg)
#     return render(request,'login.html')


def validate_otp(request):
    if request.method == 'GET':
        OTP=request.GET['otp']
        UID=request.GET['uid']
        headers = {'X-Authy-API-Key': 'b1nV9bl94GpFPggznR4UqKehe8gbRih9',}
        data = {}
        print(OTP)
        print(UID)
        response = requests.get('https://api.authy.com/protected/json/verify/'+str(OTP)+'/'+UID, headers=headers, data=data)
        print(response.content)
        if response.status_code==200:
            return HttpResponse(1)
    return HttpResponse(0)

def otp_update(request):
    if request.method == 'POST':
        contact = request.POST['contact']
        print(contact)
        is_otp_verified = request.POST['is_verified']=='true'

        try:
            otp= OTP.objects.create(
                contact=contact,
                is_otp_verified = is_otp_verified
            )
            return HttpResponse(otp.id, status=200)
        except:
            return HttpResponse(status=400)
    return HttpResponse(status=400)




# ------------------------------------------------------

def flat_owner_home(request):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)

def user_profile(request,name):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)

def tenants(request):
    args = {'user': request.user}
    return render(request, 'dashboard/tenants.html',args)

def add_new_tenant(request):
    args = {'user': request.user}
    return render(request, 'dashboard/tenant_new.html',args)

def charges(request):
    args = {'user': request.user}
    return render(request, 'dashboard/charges.html',args)

def expenditure(request):
    args = {'user': request.user}
    return render(request, 'dashboard/expenditure.html',args)

def president_home(request):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)

def secretary_home(request):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)

def treasurer_home(request):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)

def office_bearer_home(request):
    args = {'user': request.user}
    return render(request, 'dashboard/profile.html',args)
