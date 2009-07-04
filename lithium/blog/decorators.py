from lithium.blog.models import Post

def private_post_decorator(func):
    """
    A view decotator to change the queryset depending on whether
    a user may read private posts.
    """
    
    def view(request, author=None, tag=None, *args, **kwargs):
        if request.user.has_perm('blog.can_read_private'):
            kwargs['queryset'] = Post.on_site.all(allow_private=True)
            kwargs['allow_future'] = True

        if author:
            kwargs['queryset'] = kwargs['queryset'].filter(author__username=author)

        if tag:
            kwargs['queryset'] = kwargs['queryset'].filter(category__slug=tag)
        
        return func(request, *args, **kwargs)
    
    return view
