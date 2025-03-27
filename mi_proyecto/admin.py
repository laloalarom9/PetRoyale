from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Reseña

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("apellido2", "num_tel")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reseña)