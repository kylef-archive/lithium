from django.db import connection, models, transaction
from django.db.models import Count, Max

# from lithium.forum.models import Thread, Post

class ForumManager(models.Manager):
    def get_query_set(self):
        return super(ForumManager, self).get_query_set().annotate(
                thread_count=Count('thread'))
    
    def update_position(self, position, addition=1, increment=True):
        if isinstance(position, (list, tuple)):
            if position[0] == position[-1]:
                where = '%s == %d' % (self.model._meta.get_field('position').column, position[0])
            else:
                where = '%(position)s >= %(start)d AND %(position)s <= %(end)d' % {
                    'position': self.model._meta.get_field('position').column,
                    'start': position[0],
                    'end': position[-1]
                }
        else:
            where = '%s >= %d' %  (self.model._meta.get_field('position').column, position)
        
        if increment == True:
            increment = '+'
        else:
            increment = '-'
        
        query = 'UPDATE %(table)s SET %(position)s = %(position)s %(increment)s %(addition)d WHERE %(where)s' % {
            'table': self.model._meta.db_table,
            'position': self.model._meta.get_field('position').column,
            'increment': increment,
            'addition': addition,
            'where': where
        }
        cursor = connection.cursor()
        cursor.execute(query)
        transaction.commit_unless_managed()

class ThreadManager(models.Manager):
    def get_query_set(self):
        return super(ThreadManager, self).get_query_set().annotate(
            post_count=Count('post'),
            last_post_date=Max('post__pub_date')
        ).order_by('-is_sticky', '-last_post_date')
