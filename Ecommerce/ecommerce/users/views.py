from django.shortcuts import render,redirect
from .forms import UserRegisterationForm
from django.contrib import messages

# Create your views here.


def registeration(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Registration Completed for {username}! ')
            return redirect('users:login')
    else:
        form = UserRegisterationForm()

    context = { 
        'title' : 'Registration', 
        'form': form,
        }
    return render(request, 'users/register.html',context)