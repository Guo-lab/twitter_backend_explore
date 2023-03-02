from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework import response

from comments import models
from comments.api import serializers


# =========================================================================
# https://www.django-rest-framework.org/api-guide/viewsets/#genericviewset ---- ! Special ---- No actions
# =========================================================================
class CommentViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows <list, create, update, delete>
    """
    # -------- Serializer --------
    serializer_class   = serializers.CommentSerializerForCreate # before request.data
    # ---- self.get_object() -----
    queryset           = models.Comment.objects.all()
    # ---- permission_classes ----
    def get_permissions(self):
        if self.action == "create":
            if not permissions.IsAuthenticated():
                print("Need Auth")
            return [permissions.IsAuthenticated()] # instance
        return [permissions.AllowAny()]
        #//pass
    
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
                    'message': 'Invalid Input',
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
    