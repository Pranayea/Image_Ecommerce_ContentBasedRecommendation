# Image Ecommerce Using Django with Recommendation

![Homepage](pictures/loggedin-homepage.png)

## Before you start

> python version 3.8+

### __Installing packages__

first the requirement directory
```
cd Ecommerce/ecommerce

```
then.

```
pip3 install -r requirement.txt

```

for some devices this doesn't help so install the following packages individually.

``` 
pip3 install (the following individually)

* django
* numpy
* pandas
* scikit-learn
* django-cleanup
* django-sass-processor
* django-mptt
* django-libsass
* django-compressor
* django-crispy-forms
* django-allauth
* Pillow


```

---

Here, are some demo pages

SignUp

![SignUp](pictures/registeration.png)

SignIn

![SignIn](pictures/lgon.png)

Homepage

![Homepage](pictures/homepage-logout.png)

Logged In Homepage 

![Logged In Homepage](pictures/loggedin-homepage.png)

Post Detail

![Detail](pictures/detail.png)

Cart

![Cart](pictures/cart.png)

---

## About Recommendation System
### __Content-Based-Recommendation with TF/IDF__

The recommendation uses the description and title from each post, processes TF/IDF and uses it to calculate the cosine-similarity of each post.

The recommendation right now does not start until and unless the user provides a rating/review to the post in question. The rated start should be 3 or above.
