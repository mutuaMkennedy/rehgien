from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user

class IsOwnerOrReadOnly(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return obj.created_by == request.user

class AccountOwnerOrReadOnly(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return obj.username == request.user.username

class IsAPro(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return request.user.user_type != 'NormalUser'
