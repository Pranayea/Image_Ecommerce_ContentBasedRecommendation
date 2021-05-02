from django.test import TestCase
from posts.models import Post,Review,Categories
from users.models import Profile
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from . import views
from datetime import datetime
from .models import Order,OrderItem
# Create your tests here.


class TestCart(TestCase):

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

       self.orderItems = OrderItem.objects.create(product=self.post,is_ordered=True)
       instance = OrderItem.objects.filter(product=self.orderItems.product.id)
       self.order = Order.objects.create(order_code="1234test")
       self.order.items.add(*instance)

    # def test_order_total(self):
    #     order1 = Order.objects.get(order_code="123test")
    #     self.assertEqual(order1.get_cart_total,1400)