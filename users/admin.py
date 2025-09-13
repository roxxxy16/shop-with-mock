from django.contrib import admin

from users.models import Role, Module, RolePermissions, Users, CustomUserManager

admin.site.register(Users)
admin.site.register(Role)
admin.site.register(Module)
admin.site.register(RolePermissions)
