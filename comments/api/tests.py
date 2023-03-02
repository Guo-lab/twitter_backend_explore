from rest_framework.test import APIClient
from django.test import TestCase
from comments.tests import CommentModelTests

from django.contrib.auth.models import User
from comments.models import Comment


COMMENT_URL = '/api/comments/' # Important Path router

class CommentAPITests(TestCase):
    
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
    
    # ================ Specific ================
    def setUp(self):
        self.default_user = self.create_user('Alpha')
        # https://docs.djangoproject.com/en/4.1/topics/testing/tools/#the-test-client
        self.default_cli  = APIClient()
        self.default_cli.force_authenticate(user=self.default_user)
        
    def test_create(self):
        # Just some simple cases
        # Anonynous clients cannot comment
        response = self.anonynous_cli.post(COMMENT_URL)
        self.assertEqual(response.status_code, 403)
        
        # content has limits
        response = self.default_cli.post(
            COMMENT_URL,
            {'content': '1' * 105}
        )
        self.assertEqual(response.status_code, 400)
        print("*********** Content limitation is verified! ***********")
        
        # region====================================
        # ============= Valid Input ================
        # ==========================================
        response = self.default_cli.post(
            COMMENT_URL,
            {   
                'user_id': '1', # default new user is just added
                'content': 'abcdefg',
            }
        )
        # If the input is valid:
        #// print(response.data) 
        # e.g. {'id': 1, 
        # e.g.  'user': OrderedDict([('id', 1), ('username', 'Alpha'), ('email', 'Alpha@qq.com'), ('groups', [])]), 
        # e.g.  'content': 'abcdefg', 
        # e.g.  'created_at': '2023-03-02T14:28:47.724307Z', 
        # e.g.  'updated_at': '2023-03-02T14:28:47.724337Z'
        # e.g. }
        self.assertEqual(response.status_code, 201)
        # --- User-instance, user has id ---
        self.assertEqual(response.data['user']['id'], self.default_user.id) 
        self.assertEqual(response.data['content'], 'abcdefg')
        # ===========================================
        # endregion==================================
        print('*********** Two comment-created cases pass! ***********')
        