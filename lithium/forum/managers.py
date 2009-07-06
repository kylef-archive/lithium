from django.db import connection, models, transaction

# from lithium.forum.models import Thread, Post

class ForumManager(models.Manager):
    def get_query_set(self):
        qs = super(ForumManager, self).get_query_set()
        
        thread_count_query = 'SELECT COUNT(*) FROM %(thread_table)s WHERE %(thread_table)s.%(thread_forum)s = %(forum_table)s.%(forum_id)s' % {
            # 'thread_table': Thread._meta.db_table,
            # 'thread_forum': Thread._meta.get_field('forum').column,
            'thread_table': 'forum_thread',
            'thread_forum': 'forum_id',
            'forum_table': self.model._meta.db_table,
            'forum_id': self.model._meta.get_field('id').column
        }
        
        return qs.extra(select={
            'thread_count': thread_count_query,
        })
    
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
        qs = super(ThreadManager, self).get_query_set()
        
        post_count_query = 'SELECT COUNT(*) FROM %(post_table)s WHERE %(post_table)s.%(post_thread)s = %(thread_table)s.%(thread_id)s' % {
            # 'post_table': Post._meta.db_table,
            # 'post_thread': Post._meta.get_field('thread').column,
            'post_table': 'forum_post',
            'post_thread': 'thread_id',
            'thread_table': self.model._meta.db_table,
            'thread_id': self.model._meta.get_field('id').column
        }
        
        last_post_time_query = 'SELECT %(post_table)s.%(post_pub_date)s FROM %(post_table)s WHERE %(post_table)s.%(post_thread)s = %(thread_table)s.%(thread_id)s ORDER BY %(post_table)s.%(post_pub_date)s DESC LIMIT 1' % {
            'post_table': 'forum_post',
            'post_thread': 'thread_id',
            'post_pub_date': 'pub_date',
            'thread_table': self.model._meta.db_table,
            'thread_id': self.model._meta.get_field('id').column
        }
        
        return qs.extra(select={
            'post_count': post_count_query,
            'last_post_date': last_post_time_query,
        }, order_by=['-is_sticky', '-last_post_date'])
