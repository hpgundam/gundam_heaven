from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        owner_alias = ['owner', 'follower', 'author', 'commenter']
        for name in owner_alias:
            if hasattr(obj, name):
                return getattr(obj, name) == request.user

        return obj == request.user
