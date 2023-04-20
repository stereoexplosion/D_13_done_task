from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    list_display = ('author_post', 'post_create_time', 'post_header', 'post_rating') # оставляем только имя и цену товара
    list_filter = ('author_post', 'post_header')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('post_header', 'post_category__category_name')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscription)
# Register your models here.


