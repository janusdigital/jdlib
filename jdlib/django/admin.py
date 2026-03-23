from django.contrib import admin


class UUIDModelAdmin(admin.ModelAdmin):
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
