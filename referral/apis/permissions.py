from rest_framework.permissions import BasePermission

class IsRecruiterOrReadOnly(BasePermission):
    message = 'Access denied: You don\'t have write permissions.'
    def has_object_permission(self,request,view,obj):
        return obj.recruiter == request.user