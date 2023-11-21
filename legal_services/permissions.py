from rest_framework import permissions

class ObjectGetUpdateDeletePermission(permissions.BasePermission):
    message = "Read or Update or Delete Data Operation Can Be Done by the Owner"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user 