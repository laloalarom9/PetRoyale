from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mi_proyecto.views import inicio  # Importa la vista correctamente
from mi_proyecto import views  # Importa las vistas correctamente

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path('reseñas/', views.reseñas, name='reseñas'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('Tienda/', views.Tienda, name='Tienda'),
]

# 🔹 Configuración correcta para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
