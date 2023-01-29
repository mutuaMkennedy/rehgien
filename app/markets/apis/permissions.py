from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = 'Access denied: You are not the creator of this resource.'
    def has_object_permission(self,request,view,obj):
        return obj.job_poster == request.user

class IsProjectOwnerOrReadOnly(BasePermission):
    message = 'Access denied: You are not the creator of this resource.'
    def has_object_permission(self,request,view,obj):
        return obj.owner == request.user

# class IsPro(BasePermission):
#     message = 'Permission denied. Your account is allowed to perfom this action.'
#     def has_object_permission(self,request,view,obj):
#         return self.request.user == 'PRO'
