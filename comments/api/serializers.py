from rest_framework import serializers
from rest_framework import exceptions

from accounts.api.serializers import UserSerializer
from comments.models import Comment
from django.contrib.auth.models import User





class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer() # Json instead of id
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at'] # comment_id
        
        
class CommentSerializerForCreate(serializers.ModelSerializer):
    user_id = serializers.IntegerField() # convert user(instance) to user_id(the primary key)
    class Meta:
        model = Comment
        fields = ['content', 'user_id', 'type',]
    
    def validate(self, data):
        user_id = data['user_id']
        if not User.objects.filter(id=user_id).exists():
            raise exceptions.ValidationError({'message': 'user does not exist.'})
        print("Data is valid")
        return data

    def create(self, validated_data):
        return Comment.objects.create(
            user_id=validated_data['user_id'],
            content=validated_data['content'], 
            type   =validated_data['type'],
        )
      
        
# 因为不可以让用户接触到其他的更新内容如id，因此功能性 解耦合相当重要
class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content',]

    def update(self, instance, validated_data):
        # 从 request 获取的数据只更新 content 的部分
        instance.content = validated_data['content']
        instance.save()
        return instance