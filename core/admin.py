from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


from core.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'sex')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    exclude = ('password', )
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        ('Personal Info', {
            'fields': ('username', 'email', 'first_name', 'last_name', 'sex')
        }),
        ('Status', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password:
            obj.set_password(password)
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)