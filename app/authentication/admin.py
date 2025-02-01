from django.contrib import admin
from .models import User

# Register your models here.


@admin.register(User)
class UserAdminPanelModel(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ['username', 'email', 'is_admin',
                    'is_staff', 'is_superuser', 'is_active']
    list_filter = ['is_admin']
    search_fields = ['username', 'mobile_no', 'email']
    search_help_text = 'Search by Username, Email, Phone number'
    ordering = ['created_at', 'updated_at']
    save_as = True
    save_on_top = True

    class Meta:
        model = User
