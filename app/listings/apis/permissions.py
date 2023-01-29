from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'Access denied: You are not the owner of this listing.'
    def has_object_permission(self,request,view,obj):
        return obj.owner == request.user

class IsUserOrReadOnly(BasePermission):
    message = 'Access denied: You don\'t have edit permissions for this object.'
    def has_object_permission(self,request,view,obj):
        return obj.user == request.user

class IsHomeOwnerOrReadOnly(BasePermission):
    message = 'Access denied: You are not the owner of this listing.'
    def has_object_permission(self,request,view,obj):
        return obj.home.owner == request.user
