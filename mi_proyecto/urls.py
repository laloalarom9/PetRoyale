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
    path('faq/', views.faq, name='faq'),
    path('login/', views.login, name='login'),
    path('perfil/', views.perfil, name='perfil'),
    path('registro/', views.registro, name='registro'),
    path('password_reset/', views.password_reset, name='password_reset'),
]

# 🔹 Configuración correcta para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
