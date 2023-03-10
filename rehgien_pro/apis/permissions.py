from rest_framework.permissions import BasePermission

class IsAPro(BasePermission):
    message = 'PermissionDenied.'
    
    def has_permission(self, request, view):
        return request.user.user_type == 'PRO'

    def has_object_permission(self,request,view,obj):
        return request.user == obj.pro_contacted

class IsAPro2(BasePermission):
    message = 'PermissionDenied.'
    
    def has_permission(self, request, view):
        return request.user.user_type == 'PRO'

    def has_object_permission(self,request,view,obj):
        return request.user == obj.created_by

class IsOwner(BasePermission):
    message = 'PermissionDenied.'
    
    def has_permission(self, request, view):
        return request.user.user_type == 'PRO'

    def has_object_permission(self,request,view,obj):
        return request.user == obj.portfolio_item.created_by