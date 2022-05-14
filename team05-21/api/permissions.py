from rest_framework.permissions import IsAdminUser


class IsAdminOrSelf(IsAdminUser):
    """
    Allow access to admin users or the user himself.
    from https://github.com/sebastibe/django-rest-skeleton/blob/master/api/users/permissions.py
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        elif (request.user and type(obj) == type(request.user) and
              obj == request.user):
            return True
        return False
