from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from .models import Role, Module, RolePermissions

HTTP_METHOD_TO_FIELD = {
    "GET": "read_permission",
    "POST": "create_permission",
    "PUT": "update_permission",
    "PATCH": "update_permission",
    "DELETE": "delete_permission",
}

class HasModulePermission(BasePermission):
    def has_permission(self, request, view):
        module_name = getattr(view, "module", None)
        if not module_name:
            return True

        role = None
        user = request.user
        if user and getattr(user, "is_authenticated", False):
            role = getattr(user, "role", None)
        else:
            try:
                role = Role.objects.get(name="guest")
            except Role.DoesNotExist:
                return False

        try:
            module = Module.objects.get(name=module_name)
            rule = RolePermissions.objects.get(role=role, module=module)
        except (Module.DoesNotExist, RolePermissions.DoesNotExist):
            return False

        field = HTTP_METHOD_TO_FIELD.get(request.method)
        if not field:
            return False

        return bool(getattr(rule, field, False))