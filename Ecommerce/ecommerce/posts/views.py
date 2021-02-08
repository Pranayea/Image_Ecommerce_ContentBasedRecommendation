from django.shortcuts import render

# Create your views here.
def homepage(request):
    context = {
        'title' : 'Homepage'
    }
    return render(request,'posts/homepage.html',context)