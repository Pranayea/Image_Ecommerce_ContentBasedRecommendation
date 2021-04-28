from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post,Categories,Review
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CreatePost, ReviewForm
from django.utils.text import slugify 
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg,Q
# Create your views here.

#homepage
class HomeListView(ListView):
    model = Post
    template_name = "posts/homepage.html"
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 3

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Categories.objects.all()
        context['title'] = 'Homepage'
        return context

#DetailViews For each products
# class PostDetail(DetailView):
#     model = Post

def PostDetail(request,pk):
    # for the detail view of posts/products
    post = get_object_or_404(Post, pk=pk)
    template = "posts/post_detail.html"
    form = ReviewForm(request.POST)
    postRatings = Review.objects.filter(post=pk).order_by('-date')
    avgRate = postRatings.aggregate(Avg('rating')).get('rating_avg')

    # for review management
    if request.is_ajax():
        if form.is_valid():
            rating = Review()
            rating.user = request.user
            rating.post = Post.objects.get(pk=pk)
            rating.review = form.cleaned_data['review']
            rating.rating = form.cleaned_data['rating']
            rating.save()
            return JsonResponse({
                'msg':'Success'
            })
    context = {
        'post': post,
        'postRatings': postRatings,
        'avgRate': avgRate,
        'template': template,
    }

    return render(request,template,context)


class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class = CreatePost

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.cleaned_data.get("category"))
        return super().form_valid(form)

class UpdatePostView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    form_class = CreatePost

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.instance.slug = slugify(form.cleaned_data.get("categories"))
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


class DeletePostView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


def userProfile(request,pk):
    user = get_object_or_404(User,pk=pk)
    posts = Post.objects.filter(user=pk)

    paginator = Paginator(posts,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'user': user,
        'posts': posts,
        'page_obj': page_obj
    }

    return render(request,'posts/user_profile.html',context)


#showing categories
def show_categories(request,pk):
    categories = get_object_or_404(Categories,pk=pk)
    posts = Post.objects.filter(category=pk)
    context = {'categories':categories,'posts':posts}
    return render(request,'posts/categories.html',context)



def SearchFunction(request):
    query = request.GET['q']
    results = []
    if query == "":
        messages.warning(request,"Please Enter A Search Field")
    else:
        if len(query)>30:
            results = Post.objects.none()
        else:
            results = Post.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query) | Q(user__username__icontains=query) | Q(category__name__icontains=query)
            )
 
    context={
        'results':results,
        'query':query
    }
    template = 'posts/search_results.html'

    return render(request,template,context)

        
