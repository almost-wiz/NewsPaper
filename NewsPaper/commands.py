from django.contrib.auth.models import User
from NewsPaperApp.models import Author, Category, Post, Comment


# users
user1 = User.objects.create_user(username='user1', email='user1@gmail.com', password='user1')
user2 = User.objects.create_user(username='user2', email='user2@gmail.com', password='user2')


# authors
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)


# categories
sport_categ = Category.objects.create(position='Sport')
news_categ = Category.objects.create(position='News')
IT_categ = Category.objects.create(position='IT')
education_categ = Category.objects.create(position='Education')


# Posts
article1 = Post.objects.create(author=author1, title='Article1', text='Article1 text')
article2 = Post.objects.create(author=author2, title='Article2', text='Article2 text')
news = Post.objects.create(author=author1, title='News', text='News text')


# Categories for post
article1.categories.add(education_categ, IT_categ)
article2.categories.add(sport_categ, education_categ)
news.categories.add(sport_categ, news_categ)


# Comments
comment1 = Comment.objects.create(post=article1, user=user2, text='♦ Great post ♦')
comment2 = Comment.objects.create(post=article1, user=user1, text='Comment')
comment3 = Comment.objects.create(post=article2, user=user2, text='♦ Great post ♦')
comment4 = Comment.objects.create(post=news, user=user2, text='It\'s fake')


# Likes / dislikes
article1.like()
article1.like()
article1.dislike()
article1.dislike()
article1.like()
article1.dislike()
article1.like()
article1.dislike()
article1.like()
article1.like()
article1.dislike()
article1.dislike()
article1.like()
article1.like()

article2.dislike()
article2.like()
article2.like()
article2.like()
article2.like()

news.dislike()
news.dislike()
news.like()
news.like()
news.dislike()
news.like()
news.like()
news.like()
news.like()

comment1.like()
comment1.like()
comment1.like()
comment1.dislike()
comment1.dislike()
comment1.like()
comment1.dislike()
comment1.like()
comment1.like()

comment2.like()
comment2.like()
comment2.like()
comment2.dislike()
comment2.like()

comment3.dislike()
comment3.like()
comment3.like()
comment3.like()
comment3.like()
comment3.like()
comment3.dislike()
comment3.like()

comment4.dislike()
comment4.like()
comment4.dislike()
comment4.like()
comment4.like()
comment4.like()


# Update users rating
author1.update_rating()
author2.update_rating()


# Return data
print(Author.objects.all().order_by('-rating').values('user__username', 'rating')[0])

post = Post.objects.all().order_by('-rating')
post_data = post.values('date', 'author__user__username', 'rating', 'title')[0]
post_data.update({'preview': post[0].preview()})
print(post_data)

print(Comment.objects.filter(post=post[0].id).values('date', 'user', 'rating', 'text'))
