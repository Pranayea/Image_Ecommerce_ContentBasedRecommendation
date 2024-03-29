from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserRegisterationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from posts.models import Post
from cart.models import Order
from django.core.paginator import Paginator

# Create your views here.


def registration(request):
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


@login_required
def user_profile(request):
    posts = Post.objects.filter(user=request.user).order_by('-date')
    all_posts = Post.objects.all()
    #for edit forms 
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save() 
            messages.success(request, f'Your Profile Has Been Updated ')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    paginator = Paginator(posts,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title':'Profile',
        'u_form': u_form,
        'p_form': p_form,
        'posts':posts,
        'all_posts':all_posts,
        'page_obj': page_obj
    }
    return render(request,'users/profile.html',context)