from django.contrib import admin
from .models import CustomUser, Resume, Vacancy, Favorite
from django.contrib.auth.admin import UserAdmin


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 0


class VacancyInline(admin.TabularInline):
    model = Vacancy
    extra = 0


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role',)
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )
    inlines = [ResumeInline, VacancyInline]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Resume)
admin.site.register(Vacancy)
admin.site.register(Favorite)
