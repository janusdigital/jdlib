from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


class ModelAdmin(admin.ModelAdmin):
    readonly_fields = ('uuid',)

    def get_readonly_fields(self, request, obj=None):
        """Return readonly fields, including timestamps if present."""
        fields = tuple(super().get_readonly_fields(request, obj))
        return fields + tuple(field for field in ('created_at', 'updated_at') if hasattr(self.model, field))

    def get_fields(self, request, obj=None):
        """Return fields with uuid moved to the first position."""
        fields = list(super().get_fields(request, obj))
        fields.remove('uuid')
        fields.insert(0, 'uuid')
        return fields
    

class PersonalInfoMixin:
    readonly_fields = ('uuid',)

    personal_info_fields = ()

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        fieldsets = list(super().get_fieldsets(request, obj))
        fieldsets[0] = (None, {
            'fields': ('uuid',) + tuple(f for f in fieldsets[0][1]['fields'])
        })
        fieldsets[1] = (fieldsets[1][0], {
            'fields': fieldsets[1][1]['fields'] + tuple(
                f for f in self.personal_info_fields if f not in fieldsets[1][1]['fields']
            )
        })
        return fieldsets


class UserAdmin(PersonalInfoMixin, BaseUserAdmin):
    pass


class EmailUserAdmin(PersonalInfoMixin, BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'usable_password', 'password1', 'password2'),
        }),
    )
