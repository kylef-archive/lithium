from django import template
from lithium.blog.models import Post, Category

register = template.Library()

class BaseNode(template.Node):
    #@classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()
        tag_name = tokens.pop(0)
        count = len(tokens)
        if (count % 2) == 0: # The tokens divides by 2 exactly, key, value.
            kwargs = {}
            for i in range(count):
                if not (i % 2): # If odd (key)
                    if tokens[i] == 'as':
                        kwargs['as_varname'] = tokens[i+1]
                    elif tokens[i] == 'for':
                        kwargs['user'] = tokens[i+1]
                    elif tokens[i] == 'limit':
                        kwargs['limit'] = int(tokens[i+1])
            return cls(**kwargs)
        else:
            raise template.TemplateSyntaxError("Incorrect amount of argument in the tag %r" % tag_name)
        
    handle_token = classmethod(handle_token)

class PostNode(BaseNode):
    def __init__(self, as_varname, limit=5, user=None):
        self.as_varname = as_varname
        self.limit = limit
        self.user = user
    
    def render(self, context):
        if self.user:
            posts = Post.on_site.disallow_future().filter(author=self.user)[:self.limit]
        else:
            posts = Post.on_site.disallow_future()[:self.limit]
        if posts and (self.limit == 1):
            context[self.as_varname] = posts[0]
        else:
            context[self.as_varname] = posts
        return ''

class CategoryNode(BaseNode):
    def __init__(self, as_varname, limit=10):
        self.as_varname = as_varname
        self.limit = limit
    
    def render(self, context):
        context[self.as_varname] = Category.objects.filter(favorite=True)[:self.limit]
        return ''

#@register.tag
def get_latest_posts(parser, token):
    """
    This template tag will grab a list of the latest posts and insert them
    into the template context defined after the 'as' clause. Optionally, you
    can pass two other variables, a user, and a limit. The user clause will
    only display posts where the author is that user. The limit will limit the
    amount of posts in the list (the default is 5).
    
    Syntax::
        {% get_latest_posts as [varname] %}
        {% get_latest_posts as [varname] limit [limit] %}
        {% get_latest_posts for [user] as [varname] %}
        {% get_latest_posts for [user] as [varname] limit [limit] %}
    
    Example usage::
        {% get_latest_posts as post_list limit 5 %}
        {% for post in post_list %}
            {{ post.tite }}
        {% endfor %}
    """
    return PostNode.handle_token(parser, token)

#@register.tag
def get_category_list(parser, token):
    """
    To get a list of categories you can use the ``get_category_list`` template
    tag. This tag will return a list of categories in alphabetical order. It
    will also filter the categories and only use categories where "favorite"
    is set. Like ``get_latest_posts``, this tag also has a optional limit
    clause, except the default is 10.
    
    Syntax::
        {% get_category_list as [varname] %}
        {% get_category_list as [varname] limit [limit] %}
    
    Example usage::
        {% get_category_list as category_list  %}
        {% for category in category_list %}
            {{ post.tite }}
        {% endfor %}
    """
    return CategoryNode.handle_token(parser, token)

register.tag(get_latest_posts)
register.tag(get_category_list)
