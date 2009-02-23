from lithium.views.date_based import archive_index

def author_index(request, author, *args, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].filter(author__username=author)
    return archive_index(request, *args, **kwargs)

def tag_index(request, tag, *args, **kwargs):
    kwargs['queryset'] = kwargs['queryset'].filter(category__slug=tag)
    return archive_index(request, *args, **kwargs)