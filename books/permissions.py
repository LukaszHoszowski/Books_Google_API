from rest_framework import permissions


class NotPostman(permissions.BasePermission):
    message = 'Postman not allowed'

    def has_permission(self, request, view):
        user_agent = request.META['HTTP_USER_AGENT']
        return 'Postman' not in user_agent
