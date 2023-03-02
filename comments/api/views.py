from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework import response

from comments import models
from comments.api import serializers
from comments.api.permissions import IsOwner



# =========================================================================
# https://www.django-rest-framework.org/api-guide/viewsets/#genericviewset ---- ! Special ---- No actions 没有实现好 GET 等功能 用 ModelViewSet 提前可视化
# =========================================================================
class CommentViewSet(viewsets.ModelViewSet): # class CommentViewSet(viewsets.GenericViewSet):
    """
        API endpoint that allows <list, create, update, delete>
    """
    # -------- Serializer --------
    serializer_class   = serializers.CommentSerializerForCreate # before request.data
    # ---- self.get_object() -----
    queryset           = models.Comment.objects.all()
    
    # ---------- filter ----------
    filterset_fields = ('user_id', ) # 多个筛选
    
    # ---- permission_classes ----
    def get_permissions(self):
        if self.action == "create":
            if not permissions.IsAuthenticated():
                print("Need Auth")
            return [permissions.IsAuthenticated()] # instance
        
        # Permission Verify for other actions 
        elif self.action in ['update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwner()]
        
        else:
            return [permissions.AllowAny()]
        #//pass
    
    
    # -------- Create comments --------- 
    def create(self, request, *args, **kwargs):
        # ---------------------------
        # https://www.django-rest-framework.org/tutorial/2-requests-and-responses/
        # ---------------------------
        #//print(request.data) 
        #e.g. <QueryDict: {
        #e.g.     'csrfmiddlewaretoken': ['0r0k0Gzyaag0dxmkZKIlxIIToS2QmyJeCoFvi2STjDcpCuM3wOdukTKUnOgcnMPc'], 
        #e.g.     'content': ['ddFe'], 
        #e.g.     'user_id': ['1']}>
        #! In comments/model, user -> user_id
        data = { 
            'user_id': request.data.get('user_id'),
            'content': request.data.get('content'),
            'type'   : request.data.get('type'),  
        }    
        serializer = serializers.CommentSerializerForCreate(data=data) # Comment.objects.create(user_id)
        
        # ---- 输入不合法 ----
        if not serializer.is_valid():
            return response.Response({
                    'message': 'Create Invalid Input',
                    'errors':  serializer.errors, 
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # ---- 成功创建序列器 ----
        comment = serializer.save() # call serializer.create()
        return response.Response(
            serializers.CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )
    
    
    # -------- Update comments ---------
    def update(self, request, *args, **kwargs):
        """ 
            逻辑与 Create 类似
        """
        serializer = serializers.CommentSerializerForUpdate(
            instance = self.get_object(),
            data     = request.data,
        ) # get_object 是 Django RESTFul 包装的一个函数，没有返回404
        
        # ---- 输入不合法 ----
        if not serializer.is_valid():
            return response.Response({
                    'message': 'Update Invalid Input',
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # ---- 成功创建序列器 ----
        comment = serializer.save() # call serializer.update() 根据 instance 是否有参数决定触发 create / update
        return response.Response(
            serializers.CommentSerializer(comment).data,
            status=status.HTTP_200_OK,
        )
        
        
    # ---- Delete comments ----- 重写
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object() #! self
        comment.delete()
        return response.Response( 
            {'success' : True}, 
            status=status.HTTP_200_OK, # default return from destroy = HTTP 204 No Content
        )
    
    
    
    # ----- List comments ----- list 完成后，全局展示在哪里
    def list(self, request, *args, **kwargs):
        if 'user_id' not in request.query_params: # "/api/comments/?user_id=1" [Same Q & A]: id ?-> user_id
            return response.Response(
                {
                    'message' : 'missing user_id in request',
                    'success' : False,  
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        # Filtering Way 1
        user_id_   = request.query_params['user_id']
        comments_1 = models.Comment.objects.filter(user_id = user_id_)
        # Filtering Way 2
        queryset   = self.get_queryset()
        # according to filterset_fields
        comments_2 = self.filter_queryset(queryset).order_by('created_at')
        
        serializer = serializers.CommentSerializer(comments_2, many=True) # many return a list 但是response中更希望是 json hash
        return response.Response(
            {
                'comments' : serializer.data,
            },
            status = status.HTTP_200_OK
        )