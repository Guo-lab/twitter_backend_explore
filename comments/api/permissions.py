from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
        Check Object.user ?= request.user
        -- action detail = False: only check has_permission
        -- action detail = True : check has_permission and has_object_permission 
    """
    message = "No access to this Comment !!!"
    
    def has_permission(self, request, view):  # same as permissons.BasePermissions 
        """ 
            e.g. create, list
        """
        return True
    
    def has_object_permission(self, request, view, obj): # obj from queryset get()
        return request.user == obj.user
    