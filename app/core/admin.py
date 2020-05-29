from core import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# For translating purposes. It will automatically support other languages.
from django.utils.translation import gettext as _


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    # List admins by id, email, name
    ordering = ['id']
    list_display = ['email', 'name']

    # Customize Admin Fields to support our Custom Module instead of default.
    # Each () is a section. 1st=title, 2nd=Info, 3rd=Permissions, 4th=Dates
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Information'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser',)}
        ),

        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

#
# # Register the admin.
# admin.site.register(models.User, UserAdmin)
