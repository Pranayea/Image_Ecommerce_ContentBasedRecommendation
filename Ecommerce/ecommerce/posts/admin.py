from django.contrib import admin
from .models import Post,Categories
# Register your models here.
@admin.register(Post)
class AdminPost(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',),}


admin.site.register(Categories)