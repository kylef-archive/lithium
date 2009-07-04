from django.db import connection, models

class ForumManager(models.Manager):
    def update_position(self, pk, addition=1, increment=True):
        if increment == True:
            increment = '+'
        else:
            increment = '-'
        
        query = 'UPDATE %(table)s SET %(position)s = %(position)s %(increment)s %(addition)s WHERE %(position)s >= %(pk)s' % {
            'table': self.model._meta.db_table,
            'position': self.model._meta.get_field('position').column,
            'increment': increment,
            'addition': addition,
            'pk': pk
        }
        cursor = connection.cursor()
        cursor.execute(query)
