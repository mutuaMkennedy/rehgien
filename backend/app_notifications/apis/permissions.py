from rest_framework.permissions import BasePermission


class IsRecipient(BasePermission):
    message = 'Permission denied.'
    def has_object_permission(self,request,view,obj):
        return obj.recipient == request.user

class IsUser(BasePermission):
    message = 'Permission denied.'
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user
