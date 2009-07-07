import copy
import itertools

from django import template

register = template.Library()

def previous_current_next(items):
    """
    From http://www.wordaligned.org/articles/zippy-triples-served-with-python

    Creates an iterator which returns (previous, current, next) triples,
    with ``None`` filling in when there is no previous or next
    available.
    """
    extend = itertools.chain([None], items, [None])
    previous, current, next = itertools.tee(extend, 3)
    try:
        current.next()
        next.next()
        next.next()
    except StopIteration:
        pass
    return itertools.izip(previous, current, next)

#@register.filter
def tree_structure(forums):
    structure = {}
    for previous, current, next in previous_current_next(forums):
        if previous:
            structure['new_level'] = previous.level < current.level
        else:
            structure['new_level'] = True
        if next:
            structure['closed_levels'] = range(current.level, next.level, -1)
        else:
            structure['closed_levels'] = range(current.level, -1, -1)
        
        yield current, copy.deepcopy(structure)
register.filter(tree_structure)

#@register.inclusion_tag('forum/render_forum_list.html')
def render_forum_list(forum_list):
    return {'forum_list': forum_list}
register.inclusion_tag('forum/render_forum_list.html')(render_forum_list)

#@register.inclusion_tag('forum/render_reply_form.html')
def render_reply_form(thread, form):
    return {'thread': thread, 'form': form}
register.inclusion_tag('forum/render_reply_form.html')(render_reply_form)

#@register.inclusion_tag('forum/render_parent_list.html')
def render_parent_list(parent_list):
    return {'parent_list': parent_list}
register.inclusion_tag('forum/render_parent_list.html')(render_parent_list)
