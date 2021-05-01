from django.shortcuts import render,reverse,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Post
from users.models import Profile
from .models import OrderItem,Order

import random
import string
from datetime import date
import datetime

# Create your views here.
def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def add_to_cart(request,**kwargs):
    #getting user profile of current user
    user_profile = get_object_or_404(Profile, user=request.user)

    #filtering products by id
    product = Post.objects.filter(id=kwargs.get('item_id')).first()

    #checking if user owns the product
    if product in request.user.profile.product.all():
        messages.info(request,'You already own this product')
        return redirect(reverse('posts:homepage'))

    #create orederItem of the product
    order_item, status = OrderItem.objects.get_or_create(product=product)

    #create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile,is_ordered=False)
    user_order.items.add(order_item)

    if status:
        #generating order_code

        user_order.order_code = generate_order_id()
        user_order.save()

    messages.info(request,'item added to cart')
    return redirect(reverse('posts:homepage')) 


def generate_order_id():
    str_date =  date.today().strftime('%Y%m%d')[2:] +str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return str_date + rand_str


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('cart:order-summary'))


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'cart/order_summary.html', context)

@login_required()
def checkout(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'cart/checkout.html', context)


@login_required()
def update_transaction_records(request, order_id):
    # get the order being processed
    order_to_purchase = Order.objects.filter(pk=order_id).first()

    # update the placed order
    order_to_purchase.is_ordered=True
    order_to_purchase.date_ordered=datetime.datetime.now()
    order_to_purchase.save()
    
    # get all items in the order - generates a queryset
    order_items = order_to_purchase.items.all()

    # update order items
    order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

    # Add products to user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # get the products from the items
    order_products = [item.product for item in order_items]
    user_profile.product.add(*order_products)
    user_profile.save()

    # send an email to the customer
    # look at tutorial on how to send emails with sendgrid
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect(reverse('posts:homepage'))


@login_required()
def checkout_process(request,order_id):

    return redirect(reverse('cart:update-records',
                    kwargs={
                        'order_id': order_id
                    }))



def success(request, **kwargs):
    # a view signifying the transcation was successful
    return render(request, 'shopping_cart/purchase_success.html', {})