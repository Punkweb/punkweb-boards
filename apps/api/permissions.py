from rest_framework import permissions


class IsTargetUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_banned:
            return False
        if request.method == 'GET':
            return True
        if request.method in ['PUT', 'PATCH']:
            return request.user == obj
