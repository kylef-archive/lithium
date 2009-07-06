from django.test import TestCase
from lithium.forum.models import Forum, Thread, Post

class ForumTest(TestCase):
    fixtures = ['forum.json']
    
    def testDelete(self):
        forum = Forum.objects.get(pk=3)
        forum.delete()
        self.failUnlessEqual(Forum.objects.all().__str__(), '[<Forum: 1>, <Forum: 1 - 1>, <Forum: 2>, <Forum: 2 - 1>, <Forum: 3>]')
    
    def testInsert(self):
        forum = Forum.objects.get(pk=2)
        Forum.objects.create(parent=forum, title='New Forum', slug='new-forum')
        self.failUnlessEqual(Forum.objects.all().__str__(), '[<Forum: 1>, <Forum: 1 - 1>, <Forum: New Forum>, <Forum: 1 - 2>, <Forum: 1 - 2 - 1>, <Forum: 2>, <Forum: 2 - 1>, <Forum: 3>]')
    
    def testGetPreviousForum(self):
        forum = Forum.objects.get(pk=5)
        self.failUnlessEqual(forum.get_previous_forum().pk, 1)
    
    def testGetNextForum(self):
        forum = Forum.objects.get(pk=1)
        self.failUnlessEqual(forum.get_next_forum().pk, 5)
    
    def testMoveDown(self):
        forum = Forum.objects.get(pk=1)
        forum.move('down')
        self.failUnlessEqual(Forum.objects.all().__str__(), '[<Forum: 2>, <Forum: 2 - 1>, <Forum: 1>, <Forum: 1 - 1>, <Forum: 1 - 2>, <Forum: 1 - 2 - 1>, <Forum: 3>]')
    
    def testMoveUp(self):
        forum = Forum.objects.get(pk=5)
        forum.move('up')
        self.failUnlessEqual(Forum.objects.all().__str__(), '[<Forum: 2>, <Forum: 2 - 1>, <Forum: 1>, <Forum: 1 - 1>, <Forum: 1 - 2>, <Forum: 1 - 2 - 1>, <Forum: 3>]')

class ThreadTest(TestCase):
    fixtures = ['forum.json']
    
    def testOrdering(self):
        thread = Thread.objects.get(pk=1)
        Post.objects.create(thread=thread, content='Hello')
        self.failUnlessEqual(Thread.objects.all().__str__(), '[<Thread: Hello, World!>, <Thread: It works!>]')
    
    def testPostCount(self):
        self.failUnlessEqual(Thread.objects.all()[0].post_count, 1)
