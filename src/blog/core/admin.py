from django.contrib import admin

from .models import Post

# Register your models here to administer them via the Django-admin panel
@admin.register(Post) # Registers the class that it decorates
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author') # Filters used for this Model
    search_fields = ('title', 'body') # Search key words in this fields
    prepopulated_fields = {'slug': ('title',)} # Creates "slug" based on "title" field
    raw_id_fields = ('author',) # Allows to look for a specific user by its Id
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')