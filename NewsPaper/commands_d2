from news.models import *

User.objects.create_user('user1')
User.objects.create_user('user2')

a1 = Author.objects.create(author=User.objects.get(username='user1'))
a2 = Author.objects.create(author=User.objects.get(username='user2'))

c1 = Category.objects.create(news_category='Спорт')
c2 = Category.objects.create(news_category='Политика')
c3 = Category.objects.create(news_category='Наука')
c4 = Category.objects.create(news_category='Экономика')

post_1 = Post.objects.create(author_post=Author.objects.get(id=1), post_type_select='Article',
                             post_heading='Дзюба вытваоряет всякое!', post_text = 'saldfhcbvasohdbvfojqashdvboj')

ca1 = Category.objects.get(id=1)
post_1.post_category.add(ca1)

post_2 = Post.objects.create(author_post=Author.objects.get(id=2), post_type_select='News',
                             post_heading='Яйцо или курица?', post_text = 'qwertyuiop[asdfghjkl;')
ca2 = Category.objects.get(id=2)
post_2.post_category.add(ca2)

post_3 = Post.objects.create(author_post=Author.objects.get(id= 2), post_type_select='Article',
                             post_heading='Какие планы у нового президента по отношению к науке?',
                             post_text = '??????????????????????')
ca3 = Category.objects.get(id=3)
post_3.post_category.add(ca2, ca3)

User.objects.create_user('comm_boy1')
User.objects.create_user('comm_boy2')
User.objects.create_user('comm_boy3')
User.objects.create_user('comm_boy4')

comm_1 = Comment.objects.create(post=Post.objects.get(id=2), author=User.objects.get(username='comm_boy1'),
                                comment_text='Ну Дзюба и хулиган :D')
comm_2 = Comment.objects.create(post=Post.objects.get(id=3), author=User.objects.get(username='comm_boy2'),
                                comment_text='так и не понял, что раньше то было')
comm_3 = Comment.objects.create(post=Post.objects.get(id=4), author=User.objects.get(username='comm_boy3'),
                                comment_text='Президент новый, отношение старое')
comm_4 = Comment.objects.create(post=Post.objects.get(id=2), author=User.objects.get(username='comm_boy4'),
                                comment_text='жеееееесть')

Post.like(Post.objects.get(id=2))
Post.like(Post.objects.get(id=2))
Post.like(Post.objects.get(id=2))

Post.dislike(Post.objects.get(id=3))
Post.dislike(Post.objects.get(id=3))

Post.like(Post.objects.get(id=4))
Post.like(Post.objects.get(id=4))

Comment.like(Comment.objects.get(id=1))
Comment.like(Comment.objects.get(id=1))

Comment.like(Comment.objects.get(id=2))

Comment.dislike(Comment.objects.get(id=3))
Comment.dislike(Comment.objects.get(id=3))

Comment.dislike(Comment.objects.get(id=4))

Author.update_rating(Author.objects.get())

#post = Post.objects.filter(1)
#Author.objects.get(author='user1')
Author.update_rating(Author.objects.filter(id=1))
Author.update_rating(author_id=3)