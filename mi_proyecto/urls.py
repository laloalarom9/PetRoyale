from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mi_proyecto.views import inicio  # Importa la vista correctamente

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
]

# 🔹 Configuración correcta para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
