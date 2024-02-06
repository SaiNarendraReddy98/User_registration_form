from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


# Create your views here.

def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)

        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail('registration',
            'Thank U ur Registration is successfull',
            'sainarendra62645@gmail.com',
            [MUFDO.email],
            fail_silently=False,
            )

            return HttpResponse('Registartion Is Successfull')
        else:
            return HttpResponse('Invalid Data')

    return render(request,'registration.html',d)



def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')




def user_login(request):
    if request.method == 'POST':
        un = request.POST['un']
        pw = request.POST['pw']
        AUO = authenticate(username=un,password=pw)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username'] = un
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid credentials please try again...')
        
    return render(request,'user_login.html')




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))






@login_required
def profile_display(request):
    un = request.session.get('username')
    UO = User.objects.get(username=un)
    PO = Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'profile_display.html',d)




def reset_password(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['pw']

        LUO = User.objects.filter(username = username)
        if LUO :
            UO = LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('reset password is done')
        return HttpResponse('Username is not in our Database')


    return render(request,'reset_password.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        pw = request.POST['pw']
        username = request.session.get('username')
        UO = User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('<center>Password changed successfully')
    
    return render(request,'change_password.html')