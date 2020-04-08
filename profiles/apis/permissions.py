from rest_framework.permissions import BasePermission


class IsUserOrReadOnly(BasePermission):
    message = 'Access denied: You are not the owner of this listing.'
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user
