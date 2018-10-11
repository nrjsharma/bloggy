from django.contrib import admin
from .models import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author','status')
    list_filter = ('status','created','updated')
    search_fields = ('title','created','author__username')
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status','slug')
    date_hierarchy = ('created')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dob', 'photo')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'image')


admin.site.register(Post,PostAdmin)
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Images,ImageAdmin)
admin.site.register(Comments)

