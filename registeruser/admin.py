from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display =('username', 'first_name','last_name', 'email', 'address', 'phone')
    fieldsets = UserAdmin.fieldsets + (
            ('Contact', {'fields': ('address', 'phone',)}),
    )
    # UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Contact Info', {'fields': ('first_name', 'last_name', 'email', 'address', 'phone')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
