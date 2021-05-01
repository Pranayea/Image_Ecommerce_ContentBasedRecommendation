from django.urls import path
from . import views
 

urlpatterns = [
    path(r'^add-to-cart/(?P<item_id>[-\w]+)/$', views.add_to_cart,name="add-to-cart"),
    path(r'^order-summary/$', views.order_details,name="order-summary"),
    path(r'^success/$', views.success,name="p-success"),
    path(r'^item/delete/(?P<item_id>[-\w]+)/$', views.delete_from_cart,name="delete-from-cart"),
    path(r'^checkout/$', views.checkout,name="checkout"),
    path(r'^update-transaction-records/(?P<order_id>[-\w]+)/$', views.update_transaction_records,name="update-records"),
    path(r'^payment/(?P<order_id>[-\W+])/$', views.checkout_process,name="checkout-process"),   
]
