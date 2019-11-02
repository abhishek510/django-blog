from django.shortcuts import render,redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate,login

# Create your views here.


# registering new user
# use password1 for authenticate and aftee that login the user and redirect to homepage
def register(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST['username']
            password=request.POST['password1']
            user=authenticate(request,username=username,password=password)
            login(request,user)
            return redirect('home-page')
    else:
        form=RegistrationForm()
    
    reg_form={'form':form}
    return render(request,'users/register.html',reg_form)
