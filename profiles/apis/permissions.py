from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user

class AccountOwnerOrReadOnly(BasePermission):
    message = 'PermissionDenied.'
    def has_object_permission(self,request,view,obj):
        return obj.username == request.user.username
