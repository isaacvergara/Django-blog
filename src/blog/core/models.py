from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
# Managers allow us to customize how we retreive objects.
# This manager would allow us to retreive objects with the filter defined with the syntaxis Post.published.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset()\
                        .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    class Meta:
        ordering = ('-publish',)
        # db_table attr sets the name for the table in the db
    
    def __str__(self):
        return self.title
    
    # Definition of Managers (QuerySets)
    objects = models.Manager() # Default manager
    published = PublishedManager() # Custom manager. Access to objects applying this filter with Post.published.all()

    # Return the absolute url of the object
    # When we call Post.get_absolute_url() it returns a custom url for the object based on the view selected and the given args
    def get_absolute_url(self):
        return reverse("core:post_detail", 
                        args= [self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])
    