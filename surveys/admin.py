from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, Survey

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role')}
        ),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not change:
            # Handle additional logic if needed for new user creation
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

    def save_form(self, request, form, change):
        if 'password' in form.cleaned_data:
            form.instance.set_password(form.cleaned_data['password'])
        return super().save_form(request, form, change)

class SurveyAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time', 'owner', 'status')
    search_fields = ('name', 'owner__username')
    list_filter = ('status', 'date_time')
    ordering = ('date_time',)

    def save_model(self, request, obj, form, change):
        if not change and not obj.owner_id:
            obj.owner = request.user  # Assign the current user if not already assigned
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.unregister(Group)
