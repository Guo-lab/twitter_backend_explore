from django.db import models

from django.contrib.auth.models import User


# Create your models here.
#@ https://www.django-rest-framework.org/tutorial/1-serialization/#creating-a-model-to-work-with
class Comment(models.Model):
    """
        ORM (Object Relational Mapping)
    """
    user       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content    = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # ============ add a new field ============= 重新 migrate model 会拖慢速度
    type       = models.TextField(max_length=20, null=True)
    # ==========================================
    #? [Q & A]: <why id turns out to be 'user_id'>
    
    class Meta: #* nested class to add functions or standards
        # === sort by user-created time ===
        index_together = (('user', 'created_at'), )
        # =================================
        ordering       = ['created_at']
        
    def __str__(self):
        """
            return string format expression of the Comment class
        """
        return "[{}] <User {}> proposed: '{}.'".format(
            self.created_at, 
            self.user,
            self.content,
        )
        