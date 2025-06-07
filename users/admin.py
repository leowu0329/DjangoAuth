from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Profile

# 內聯管理 Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['email', 'username', 'age']
    model = CustomUser
    inlines = [ProfileInline]  # 添加內聯
    
    # 重寫get_inline_instances方法，確保在添加使用者時不顯示內聯
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        try:
            if not obj.profile:
                Profile.objects.create(user=obj)
        except Profile.DoesNotExist:
            Profile.objects.create(user=obj)
        return super().get_inline_instances(request, obj)

admin.site.register(CustomUser, CustomUserAdmin)

# 也可以單獨註冊Profile模型
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'work_area']
    search_fields = ['user__username', 'user__email']
