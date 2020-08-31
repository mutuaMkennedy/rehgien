from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'Access denied: You are not the creator of this resource.'
    def has_object_permission(self,request,view,obj):
        return obj.owner == request.user
