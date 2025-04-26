from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .models import Reseña
from .models import Pedido

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Información adicional", {"fields": ("apellido2", "num_tel")}),
    )
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'numero_pedido', 'estado', 'lat', 'lng')  # 👈 Añadimos lat y lng

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reseña)