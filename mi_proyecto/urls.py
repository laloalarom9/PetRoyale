from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mi_proyecto.views import inicio  # Importa la vista correctamente
from mi_proyecto import views  # Importa las vistas correctamente
from django.contrib.auth import views as auth_views  # Importar vistas de autenticación

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", inicio, name="inicio"),
    path("reseñas/", views.reseñas, name="reseñas"),
    path("pedidos/", views.pedidos, name="pedidos"),
    path("Tienda/", views.Tienda, name="Tienda"),
    path("faq/", views.faq, name="faq"),
    
    #  Corrección: Cambia "views.login" por "views.login_view"
    path("login/", views.login_view, name="login"),  
    path("logout/", views.logout_view, name="logout"),  # Agrega logout

    path("perfil/", views.perfil, name="perfil"),
    path("registro/", views.registro_view, name="registro"),  # Cambia "views.registro" por "views.registro_view"
    
    #  Usar vista de Django para recuperación de contraseña
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
]

#  Configuración correcta para servir archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
