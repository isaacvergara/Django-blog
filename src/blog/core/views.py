from django.shortcuts import render, get_object_or_404
from django.core.paginator  import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post

# Create your views here.
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'core/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list= object_list, per_page= 3) # Posts per page
    page = request.GET.get('page') # Get the page argument in the GET request (if none then return first page)
    try:
        posts = paginator.page(page) # Retreives objects for the selected page number
    except PageNotAnInteger:
        # If page is not an integer then return the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page number is out of range then return the last page
        posts = paginator.page(paginator.num_pages)
    return render(request, 
                  'core/post/list.html', # Template source 
                  {'posts': posts,
                   'page': page}) # Context (variables given to the template)

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'core/post/detail.html',
                  {'post': post})