from rest_framework import permissions


class IsTargetUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.profile.is_banned:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj


class BelongsToUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.profile.is_banned:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.profile.is_banned:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == obj.user
