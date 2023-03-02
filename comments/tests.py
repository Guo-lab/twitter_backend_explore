from django.test import TestCase

from rest_framework.test import APIClient 
from django.contrib.auth.models import User
from comments.models import Comment


# Create your tests here.
class CommentModelTests(TestCase):
    
    @property
    def anonynous_cli(self):
        if hasattr(self, '_anonymous_client'):
            return self._anonymous_client
        self._anonymous_client = APIClient()
        return self._anonymous_client
    
    def create_user(self, username, email=None, password=None):
        if password is None:
            password = 'temporary pwd'
        if email is None:
            email = f'{username}@qq.com'
        return User.objects.create_user(username, email, password)
    
    def test_comment(self):
        user = self.create_user('@@BOY')
        # comment = self.create_comment(user)
        content = 'default comment content'
        comment = Comment.objects.create(user=user, content=content)
        self.assertNotEqual(comment.__str__(), None)
        print("\n" + comment.__str__())
        print('Congs! Comment Model TestCase Pass!')