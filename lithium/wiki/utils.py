
def title(value):
    """
    Turns 'my_title' into 'My Title'
    """
    from django.template.defaultfilters import title
    return title(value).replace('_', ' ')

def slugify(value):
    """
    Turns 'My Title' into 'My_Title'
    """
    return value.replace(' ', '_')
