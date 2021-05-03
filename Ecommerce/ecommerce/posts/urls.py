from django.urls import path
from .views import CreatePostView,UpdatePostView,DeletePostView,SearchFunction
from . import views

urlpatterns = [
    path('', views.HomeList, name = "homepage"),
    path('posts/<int:pk>/',views.PostDetail,name = "post-detail"),
    path('posts/new/',CreatePostView.as_view(),name ='post-create'),
    path('posts/<int:pk>/update/',UpdatePostView.as_view(),name = "post-update"),
    path('posts/<int:pk>/delete/',DeletePostView.as_view(),name = "post-delete"),
    path('posts/category/<int:pk>/',views.show_categories,name = 'category'),
    path('posts/user/<int:pk>/',views.userProfile,name = 'profile'),
    path('posts/search/',views.SearchFunction,name='search')
]
