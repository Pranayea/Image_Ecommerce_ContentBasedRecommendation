# from django.contrib.auth.models import User
# from .models import Post,Categories,Review
# import numpy as np
# import pandas as pd
# from rake_nltk import Rake
# from sklearn.metrics.pairwise import cosine_similarity
# from sklearn.feature_extraction.text import CountVectorizer as CV


# products = pd.DataFrame(list(Post.objects.all().values()))
# users = pd.DataFrame(list(User.objects.all().values()))
# categories = pd.DataFrame(list(Categories.objects.all().values()))

# #dropping unwanted columns 
# products = products.drop(['image','date','slug','price'],axis=1)
# users = users.drop(['password','last_login','is_superuser','last_name','email','is_staff','is_active','first_name','date_joined'],axis=1)
# categories = categories.drop(['parent_id'],axis=1)


# #merging dataframes
# post = pd.merge(products,users,left_on="user_id",right_on="id" ,how='left')
# post = pd.merge(post,categories,left_on="category_id",right_on="id" ,how='left')


# #dropping extra columns in final dataframe
# post = post.drop(['id_x','user_id','id_y','id','category_id'],axis=1)

# #keywords extraction with rake
# post['Key-words'] = ""
# rake = Rake()
# for index,row in post.iterrows():
#     description = str(row['description'])
#     rake.extract_keywords_from_text(description)
#     key_words_dict_scores = rake.get_word_degrees()
#     row['Key-words'] = list(key_words_dict_scores.keys())

# #lowercaseing words and removing spaces
# for index,row in post.iterrows():
#     row['name'] = [x.lower().replace(' ','') for x in row['name']]
#     row['username'] = [x.lower().replace(' ','') for x in row['username']]


# post['Bag_of_words'] = ''
# columns = ['name','username','Key-words'] 
# for index,row in post.iterrows():
#     words = ''
#     for col in columns:
#         words += ' '.join(row[col]) + ' '
#     row['Bag_of_words'] = words


# post = post[['title','Bag_of_words']]


# #creating cosine-similarity matrix
# count = CV()
# count_matrix = count.fit_transform(post['Bag_of_words'])
# cosine_sim = cosine_similarity(count_matrix, count_matrix)

# #extracting titles from dataframe
# indices = pd.Series(post['title'])


# def recommend(title, cosine_sim = cosine_sim):
#     recommended_post = []
#     idx = indices[indices == title].index[0]
#     score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
#     top_15_indices = list(score_series.iloc[1:16].index)
    
#     for i in top_15_indices:
#         recommended_post.append(list(post['title'])[i])
        
#     return recommended_post