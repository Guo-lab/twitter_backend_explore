from rest_framework.test import APIClient
from django.test import TestCase
from django.utils import timezone
from comments.tests import CommentModelTests

from django.contrib.auth.models import User
from comments.models import Comment




COMMENT_URL    = '/api/comments/' # Important Path router
COMMENT_URL_ID = '/api/comments/{}/' 

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
        
        
    # =============== Function TestCases =============    
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
        
    def test_destroy(self):
        content = 'content to be deleted'
        comment = Comment.objects.create(user=self.default_user, content=content)
        _delete = COMMENT_URL_ID.format(comment.id) # comment_id
        
        response = self.anonynous_cli.delete(_delete) 
        self.assertEqual(response.status_code, 403) 
        
        self.another_user = self.create_user('Beta')
        self.another_cli  = APIClient()
        self.another_cli.force_authenticate(user=self.another_user)
        response = self.another_cli.delete(_delete)
        self.assertEqual(response.status_code, 403) 
          
        client_comment_cnt = Comment.objects.count()
        response = self.default_cli.delete(_delete)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(Comment.objects.count(), client_comment_cnt - 1) 
        print("\n********** Three comment-deleted cases pass! **********")
        
    def test_update(self):
        content = 'content to be updated'
        comment = Comment.objects.create(user=self.default_user, content=content)        
        _update = COMMENT_URL_ID.format(comment.id) 
        
        # update --> put
        response = self.anonynous_cli.put(_update, {'content': 'new'}) 
        self.assertEqual(response.status_code, 403) 
        # 非本人不能更新 验证跳过
        
        # 确保刷新数据库之后 content 确实没有被修改
        comment.refresh_from_db()
        self.assertNotEqual(comment.content, 'new')
        
        # 除了 content 都不能被修改
        prev_created_time, prev_updated_time = comment.created_at, comment.updated_at
        response = self.default_cli.put(_update, 
            {
                'content'   : 'new',
                'user_id'   : self.default_user, # self.another_user can also not be updated
                'created_at': timezone.now(), 
            }
        )
        self.assertEqual(response.status_code, 200) 
        comment.refresh_from_db()
        self.assertEqual(comment.created_at, prev_created_time)
        self.assertNotEqual(comment.updated_at, prev_updated_time)
        print("\n********** Three comment-updated cases pass! **********")
        
        