from lithium.blog.models import Post

def decorator(request, view, author=None, tag=None, *args, **kwargs):
    """
    A view decotator to change the queryset depending on whether
    a user may read private posts.
    """
    
    if request.user.has_perm('blog.can_read_private'):
        kwargs['queryset'] = Post.on_site.all(allow_private=True)
    
    if author:
        kwargs['queryset'] = kwargs['queryset'].filter(author__username=author)
    
    if tag:
        kwargs['queryset'] = kwargs['queryset'].filter(category__slug=tag)
    
    return view(request, *args, **kwargs)
