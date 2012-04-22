
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

def user_permission_level(user):
    if user.is_staff:
        return 3

    if user.is_superuser:
        return 4

    if user.is_anonymous():
        return 1

    return 2

