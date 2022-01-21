from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .models import Post,Categories,Review
from django.contrib.auth.models import User
from users.models import Profile
from cart.models import Order
from django.contrib import messages
from .forms import CreatePost, ReviewForm
from django.utils.text import slugify 
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg,Q
# from .BOWrecommend import recommend
from .Tfrecommendor import recommendTdidf
# Create your views here.

#homepage
def HomeList(request):
    posts = Post.objects.all().order_by('-date')
    categories = Categories.objects.all()
    current_order_products = []
    post_list = []
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        #for recommendation
        user = request.user
        review_from_user = Review.objects.filter(user=user).first()
        title_for_user = review_from_user.post.title
        recommendations = recommendTdidf(title_for_user)
        count = len(recommendations)
        post_list = []
        for r in recommendations:
            posts_title = Post.objects.get(title=r)
            post_list.append(posts_title)

        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

    paginator = Paginator(posts,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'posts':posts,
        'categories':categories,
        'current_order_products': current_order_products,
        'title':'Homepage',
        'page_obj': page_obj,
        'post_list': post_list
    }

    return render(request,"posts/homepage.html",context)

#DetailViews For each products    
def PostDetail(request,pk):
    # for the detail view of posts/products
    post = get_object_or_404(Post, pk=pk)
    template = "posts/post_detail.html"
    form = ReviewForm(request.POST)
    postRatings = Review.objects.filter(post=pk).order_by('-date')
    avgRate = postRatings.aggregate(Avg('rating')).get('rating__avg')

    #for checking if the product is owned by user or not
    # for review management
    if request.method == "POST":
        reviews = ReviewForm(request.POST)

        if form.is_valid():
            obj = reviews.save(commit=False)
            obj.user = request.user
            obj.post = Post.objects.get(pk=pk)
            obj.review = form.cleaned_data['review']
            obj.rating = form.cleaned_data['rating']
            obj.save()
            return redirect('posts:post-detail',pk=post.pk)
        else:
            reviews = ReviewForm()
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

    paginator = Paginator(posts,12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'categories':categories,'posts':posts,'page_obj':page_obj}
    return render(request,'posts/categories.html',context)



def SearchFunction(request):
    query = request.GET['q']
    results = Post.objects.none()
    sorting = request.GET.get('sorting','-date')

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
        'results':results.order_by(sorting),
        'query':query,
        'sorting':sorting
    }
    template = 'posts/search_results.html'

    return render(request,template,context)

        
def recommend_page(request):
    user = request.user
    review_from_user = Review.objects.filter(user=user).first()
    title_for_user = review_from_user.post.title
    recommendations = recommendTdidf(title_for_user)
    count = len(recommendations)
    posts = Post.objects.all()
    post_list = []
    for r in recommendations:
        posts_title = Post.objects.get(title=r)
        post_list.append(posts_title)

    current_order_products = []
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

    context = {
        'title': title_for_user,
        'post_list': post_list,
        'count':count,
        'posts' : posts,
        'current_order_products': current_order_products
    }
    return render(request,"posts/recommendation.html",context)