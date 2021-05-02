from django.test import TestCase,SimpleTestCase
from .models import Post,Review,Categories
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from . import views
from datetime import datetime
# Create your tests here.

class TestPostUrls(SimpleTestCase):

    def test_homepage_url_is_resolved(self):
        url = reverse("posts:homepage")
        self.assertEqual(resolve(url).func.view_class,views.HomeListView)

    def test_createPost_url_is_resolved(self):
        url = reverse("posts:post-create")
        self.assertEqual(resolve(url).func.view_class,views.CreatePostView)

    def test_search_url_is_resolved(self):
        url = reverse("posts:search")
        self.assertEqual(resolve(url).func,views.SearchFunction)

    def test_user_profile_url_is_resolved(self):
        url = reverse("posts:profile",args=[1])
        self.assertEqual(resolve(url).func,views.userProfile)

    def test_editPost_url_is_resolved(self):
        url = reverse("posts:post-update",args=[1])
        self.assertEqual(resolve(url).func.view_class,views.UpdatePostView)

    def test_deletePost_url_is_resolved(self):
        url = reverse("posts:post-delete",args=[1])
        self.assertEqual(resolve(url).func.view_class,views.DeletePostView)

    def test_category_url_is_resolved(self):
        url = reverse("posts:category",args=[1])
        self.assertEqual(resolve(url).func,views.show_categories)

    def test_post_detail_url_is_resolved(self):
        url = reverse("posts:post-detail",args=[1])
        self.assertEqual(resolve(url).func,views.PostDetail)


class TestPost(TestCase):

    def setUp(self):
    #creating instances of objects in User
       self.user1 = User.objects.create(username="PmPranaya",email="Pmpranaya@gmail.com")
       self.category = Categories.objects.create(name="Arts")
       self.post = Post.objects.create(
            user=self.user1,
            title="Test Title",
            description="This is Test Description",
            date=datetime.now(),
            category=self.category,
            price = 1400)
       self.review = Review.objects.create(
           user=self.user1,
           date=datetime.now(),
           post=self.post,
           review="This is Test Review",
           rating=5
       )    
    
    def test_post_data(self):
        post1 = Post.objects.get(title="Test Title")
        self.assertEqual(post1.description,"This is Test Description")
        self.assertEqual(post1.price,1400)
        self.assertEqual(post1.user.username,"PmPranaya")
        self.assertEqual(post1.category.name,"Arts")

    def test_review_data(self):
        review1 = Review.objects.get(review="This is Test Review")
        self.assertEqual(review1.user.username,"PmPranaya")
        self.assertEqual(review1.post.title,"Test Title")