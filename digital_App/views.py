from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from random import randint
import os


# Create your views here.

default_data = {

}


def index1(request):
    return HttpResponse("<h1>Hello World</h1>")
    
def home(request):
    return render(request, "home.html", default_data)

def signup_page(request):
    return render(request, "signup_page.html")

def signin_page(request):
    return render(request, "signin_page.html")

def forgot_pwd_page(request):
    return render(request, "forgot_pwd_page.html")

def updt_profile_update(request):
    return render(request, "updt_profile_update.html")

def society_members(request):
    if 'email' in request.session:
        load_All_Members(request)
        return render(request, 'society_members.html', default_data)
    return render(request, 'society_members.html', default_data)

def society_watchman(request):
    if 'email' in request.session:
        load_watchman_data(request) # Load Watchman data
        return render(request, 'society_watchman.html', default_data)
    return render(request, 'society_watchman.html', default_data)

def notice_page(request):
    if 'email' in request.session:
        view_notice(request) # Load Notice data
        return render(request, "notice_page.html", default_data)
    return render(request, 'notice_page.html')

def event_page(request):
    if 'email' in request.session:
        load_All_Events(request) # Load All Event
        return render(request, "event_page.html", default_data)
    return render(request, "event_page.html", default_data)

def otp_page(request):
    if 'email' in request.session:
        forgot_password(request)
    return render(request, "otp_page.html")


def chairman_profile_page(request):
    if 'email' in request.session:
        profile_data(request,)
        return render(request, 'chairman_profile_page.html', default_data)
    return render(request, "chairman_profile_page.html")

def profile_page(request):
    print(request.session['email'])
    if 'email' in request.session:
        try:
            try:
                profile_data_2(request)
                return redirect(chairman_profile_page)
                
            except:
                profile_data(request,)
                return render(request,'profile_page.html', default_data)

        except Exception as err:
            print("Data not availabe")
    return redirect(signin_page)

def add_event_Notice(request):
    return render(request, 'add_event_Notice.html', default_data)




# Signup Logic
# def signup(request):
#     print(request.POST)
#     password = request.POST['password']

#     if password == request.POST['conform_password']:
#         user = User.objects.create(Email = request.POST['email'], Password = password)
#         Visitor.objects.create(User = user)
#         print("Signup successfully...")

#     else:
#         print('both password should be same...')
#         return redirect(signup_page)

#     return redirect(signin_page)

#signup_functionality
def signup(request):
    print(request.POST)
    password = request.POST['password']
    if password == request.POST['confirm_password']:
        user = User.objects.create(Email = request.POST['email'],Password = password)
        role=Role.objects.create(Role_Type = request.POST['role_type'])
        visitor=Visitor.objects.create(User = user)
        print('Signup successfully.')
        if role.Role_Type == 'chairman':
            print('Chairman')
            Chairman.objects.create(Visitor=visitor)
        else:
            print('member')
            Member.objects.create(Visitor=visitor)
    else:
        print('both password should be same.')
        return redirect(signup_page)

    return redirect(updt_profile_update)


# Signin Logic
def signin(request):
    # print(request.POST)
    try:
        user = User.objects.get(Email = request.POST['email'])
        if user.Password == request.POST['password']:
            request.session['email'] = user.Email
            # return redirect(profile_page)
            return redirect(profile_page)

        else:
            return render(request, 'signin_page.html', {'error': "Password does not match"})

    except User.DoesNotExist as err:
        return render(request, 'signin_page.html', {'error': "User does not Exists Please SignUp"})


# Logout Logic
def logout(request):
    print(request.POST)
    if 'email' in request.session:
        del request.session['email']
        return redirect(signin_page)
    return redirect(home)

# Profile Page Update Logic
def profile_update(request):
    print(request.POST)
    user = User.objects.get(Email = request.session['email'])
    visitor = Visitor.objects.get(User = user)

    visitor.FullName = ' '.join([request.POST['first_name'], request.POST['last_name']])
    visitor.Mobile = request.POST['mobile']
    visitor.Birthday = request.POST['birthdate']
    # visitor.Gender = request.POST['gender']

    visitor.save()

    return redirect(profile_page)


# Profile Page Update Logic Chairman
def profile_update_2(request):
    print(request.POST)
    user = User.objects.get(Email = request.session['email'])
    user_data = Visitor.objects.get(User = user)
    chairman = Chairman.objects.get(Visitor = user_data)

    chairman.Type = request.POST['type']
    user_data.FullName = ' '.join([request.POST['first_name'], request.POST['last_name']])
    user_data.Mobile = request.POST['mobile']
    user_data.Birthday = request.POST['birthdate']
    # visitor.Gender = request.POST['gender']

    user_data.save()
    chairman.save()
    return redirect(profile_page)

# Load Profile data Logic
def profile_data(request):
    print(request.POST)
    user = User.objects.get(Email = request.session['email'])
    visitor = Visitor.objects.get(User = user)

    visitor.first_name = visitor.FullName.split()[0]
    visitor.last_name = visitor.FullName.split()[1]
    visitor.birthday = visitor.Birthday.strftime("%Y-%m-%d") 
    visitor.mobile = visitor.Mobile

    default_data["member_data"]= visitor


# Load Profile data 2 Logic 
def profile_data_2(request):
    print(request.POST)
    user = User.objects.get(Email = request.session['email'])
    visitor = Visitor.objects.get(User = user)
    chairman  = Chairman.objects.get(Visitor = visitor)

    visitor.first_name = visitor.FullName.split()[0]
    visitor.last_name = visitor.FullName.split()[1]
    visitor.mobile = visitor.Mobile
    visitor.birthday = visitor.Birthday.strftime("%Y-%m-%d")
    chairman.type = chairman.Type

    default_data["member_data"]= visitor
    default_data['chairman']=chairman

# forgot password
def forgot_password(request):
    print(request.POST)
    try:
        user = User.objects.get(Email = request.POST['email'])
        request.session['email'] = user.Email
        if user.Email == request.POST['email']:
            print('OTP Sent Successfully')
            otp_creation(request)
            return redirect(otp_page)
        else:
            print("Email Not Register")
            return redirect(signup_page)
    except :
        print("invalid Email")
        return redirect(signin_page)

# OTP Creation
def otp_creation(request):
    otp_number = randint(1000, 9999)
    print("OTP is: ", otp_number)
    request.session['otp'] = otp_number
    return otp_number

#otp send
def otp_send(request):
    if request.session['otp'] == int(request.POST['otp']):
        print('otp match')
        user = User.objects.get(Email = request.session['email'])
        if request.POST['new_password'] == request.POST['confirm_password']:
            user.Password = request.POST['new_password']
            print('password change successfully')
            user.save()
        else:
            print('both password should be same.')
            return redirect(forgot_pwd_page)
    else:
        print('Wrong OTP')
        return redirect(forgot_pwd_page)
    return redirect(signin_page)


def view_notice(request):
    print(request.POST)
#     # notice = Notice.objects.get() 

    noticeview = Notice.objects.all()
    default_data['noticeview'] = noticeview
    
# View Watchman data
def load_watchman_data(request):
    print(request.POST)
 
    watchman = Watchman.objects.all()
    default_data['watchman'] = watchman

# View All Event data
def load_All_Events(request):
    print(request.POST)
 
    event = Event.objects.all()
    default_data['event'] = event

# View All Event data
def load_All_Members(request):
    print(request.POST)
 
    visitor = Visitor.objects.all()
    default_data['visitor'] = visitor


# Add Event Logic
def add_event(request):
    print(request.POST)

    event =Event.objects.create(
        AddEvent=request.POST['event'],
        Date= request.POST['date']
    )
    event.save()
    return redirect(profile_page)


def add_notice(request):
    print(request.POST)
    if 'email' in request.session:
        notice =Notice.objects.create(
            AddNotices=request.POST['notice'],
            Date= request.POST['date']
        )
        notice.save()
        return redirect(profile_page)
    else:
        ('You are not an Chairman')


def delete_account(request):
    print(request.POST)
    user=User.objects.get(Email = request.session['email'])
    user.delete()
    return redirect(signin_page)


def delete_event(request, event):
    print(request.POST)
    events=Event.objects.get(AddEvent = event)
    events.delete()
    return redirect(event_page)


def delete_notice(request, notice):
    print(request.POST)
    notices=Notice.objects.get(AddNotices = notice)
    notices.delete()
    return redirect(notice_page)


