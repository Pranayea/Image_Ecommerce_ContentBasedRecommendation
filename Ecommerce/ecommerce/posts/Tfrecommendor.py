from django.contrib.auth.models import User
from .models import Post,Categories,Review
import numpy as np
import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

products = pd.DataFrame(list(Post.objects.all().values()))
users = pd.DataFrame(list(User.objects.all().values()))
categories = pd.DataFrame(list(Categories.objects.all().values()))

#dropping unwanted columns 
products = products.drop(['image','date','slug','price'],axis=1)
users = users.drop(['password','last_login','is_superuser','last_name','email','is_staff','is_active','first_name','date_joined'],axis=1)
categories = categories.drop(['parent_id'],axis=1)


#merging dataframes
post = pd.merge(products,users,left_on="user_id",right_on="id" ,how='left')
post = pd.merge(post,categories,left_on="category_id",right_on="id" ,how='left')

#dropping extra columns in final dataframe
post = post.drop(['id_x','user_id','id_y','id','category_id'],axis=1)

#creating text column
post['text'] = post['description'].map(str)+" " + post['username'].map(str)+" " +post['name']

#Using Tf-idfVectorizer
tfid = TfidfVectorizer()
tfid_post = tfid.fit_transform(post['text'])

#creating matrix with cosine similarity
cos_sim = cosine_similarity(tfid_post,tfid_post)

#creating indeces
indices = pd.Series(post['title'])

#reommendation function
def recommendTdidf(title, cosine_sim = cos_sim):
    recommended_post = []
    idx = indices[indices == title].index[0]
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
    top_3_indices = list(score_series.iloc[1:4].index)
    
    for i in top_3_indices:
        recommended_post.append(list(post['title'])[i])
        
    return recommended_post