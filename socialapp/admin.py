from django.contrib import admin

# Register your models here.
from . models import *

class PostImageInline(admin.StackedInline):
  model = PostImage
  max_num=10
  extra=0

class PostAdmin(admin.ModelAdmin):
  inlines = [PostImageInline,]
  list_display = ('post_name', 'like', 'dislike')

admin.site.register(Post, PostAdmin)
admin.site.register(Category)

