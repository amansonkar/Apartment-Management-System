from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm, EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import regForm,regform1
import random,requests,json
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login
from .models import UserProfile
# Create your views here.

def home(request):
    return render(request,'accounts/home.html')

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/account')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'accounts/signup.html',args)

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


def regView(request):
    form = regForm()
    form1 = regform1()
    if request.method == 'POST':
        form = regForm(data=request.POST)
        form1 = regform1(data=request.POST)

        if form.is_valid() and form1.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = form1.save(commit = False)
            profile.user = user
            profile.save()
            return HttpResponse('Register Successfully!!!')

    return render(request,'accounts/registration.html',{'form':form,'form1':form1})

def generate_otp(request):
    otp = random.randint(1000,9999)
    if 'number' in request.GET:
        message = "Here is your OTP {} for registration \n Don't share it with anyone".format(otp)
        number = request.GET['number']
        print(number)
        headers = {'X-Authy-API-Key': 'A1XkYkSm2wkcNiB3LJDMF9imGXsrHFtc',}

        data = {
        'user[email]': 'ffdddbbvhz@sgoogle.com',
        'user[cellphone]': '9129932523',
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
                return HttpResponse(UID,'it works')
        return HttpResponse(0)

    elif 'user' in request.GET:
        username = request.GET['user']
        check = User.objects.filter(username__iexact=username)
        if len(check) is not 0:
            for i in check:
                id = i.id
            getNumber = UserProfile.objects.get(user_id=id)
            number = repr(getNumber.contact)
            #message = "Here is your OTP {} for registration \n Don't share it with anyone".format(otp)
            headers = {'X-Authy-API-Key': 'A1XkYkSm2wkcNiB3LJDMF9imGXsrHFtc',}
            data = {}
            api = requests.post('https://api.authy.com/protected/json/sms/196583372?force=true', headers=headers, params=data)
            strNum =repr(number)
            d = strNum.replace(strNum[:6],'******')
            item1 ='An OTP sent to your {} mobile number \n It may take a minute @'.format(d)
            list = [item1,otp]
            print(list)
            return HttpResponse(list)
        else:
            return HttpResponse('Please Enter Correct Username')

    return HttpResponse(otp)

def loginView(request):
    if request.method == 'GET':
        username = request.POST['un']
        user = User.objects.get(username=username)
        msg = '<h1>Hello {} You are now Logged In</h1>'.format(user.username)
        login(request,user)
        return HttpResponse(msg)
    return render(request,'login.html')


def validate_otp(request):
    if request.method == 'GET':
        OTP=request.GET['number']
        UID=request.GET['p']
        headers = {'X-Authy-API-Key': 'A1XkYkSm2wkcNiB3LJDMF9imGXsrHFtc',}
        data = {}
        print(OTP)
        print(UID)
        response = requests.get('https://api.authy.com/protected/json/verify/'+str(OTP)+'/'+UID, headers=headers, data=data)
        print(response.content)
        if response.status_code==200:
            return HttpResponse(1)
    return HttpResponse(0)


def verify_otp(request):
    if not request.session.get('is_verified'):
        return redirect('phone_verification')
    return render(request, 'verified.html')